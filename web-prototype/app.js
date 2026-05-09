// ---------------------------------------------------------------
// Dormire Phase 0 prototype — メインアプリロジック
//
// - getUserMedia でスマホカメラを起動
// - MediaPipe Tasks Vision の PoseLandmarker でリアルタイム検出
// - キャプチャボタンで 1 フレーム確定 → calc.js で 20 項目算出
// - 結果表を描画
//
// 参考: https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker/web_js
// ---------------------------------------------------------------

import {
  PoseLandmarker,
  ImageSegmenter,
  FilesetResolver,
  DrawingUtils,
} from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/vision_bundle.mjs";

import { calculateAll, LABELS, fmt, POSE } from "./calc.js";

// ---- DOM refs --------------------------------------------------
const $ = (id) => document.getElementById(id);
const video = $("video");
const overlay = $("overlay");
const stage = $("stage");
const ctx = overlay.getContext("2d");
const btnCapture = $("btnCapture");
const btnReset = $("btnReset");
const statusEl = $("status");
const resultsCard = $("resultsCard");
const resultsBody = $("resultsBody");
const fpsEl = $("fps");
const stepText = $("stepText");
const dotFront = $("dotFront");
const dotSide = $("dotSide");
const thumbs = $("thumbs");
const thumbFront = $("thumbFront");
const thumbSide = $("thumbSide");
const materialCard = $("materialCard");
const materialSelected = $("materialSelected");
const materialRadios = document.querySelectorAll(
  'input[name="pillowMaterial"]'
);
const sideGuide = $("sideGuide");
const sideTips = $("sideTips");
const heightCard = $("heightCard");
const heightInput = $("heightInput");
const aiCard = $("aiCard");
const aiBaseline = $("aiBaseline");
const aiLoading = $("aiLoading");
const aiContent = $("aiContent");
const aiHeadline = $("aiHeadline");
const aiComment = $("aiComment");
const aiTags = $("aiTags");
const aiAdvice = $("aiAdvice");
const aiError = $("aiError");

const POSTURE_LABELS = {
  N: "N（理想姿勢）",
  U: "U（反り腰）",
  丸: "丸（猫背）",
  W: "W（強いS字カーブ）",
};
const AI_ENDPOINT = "/.netlify/functions/posture-ai";
const ANGLE_KEYS = new Set([
  "back_angle",
  "head_angle",
  "shoulder_angle",
  "hip_angle",
  "cva",
  "head_pitch",
  "neck_tilt",
]);
// 画像幅で正規化されている指標（cm 換算時は画像幅cmを掛ける）
const WIDTH_NORM_KEYS = new Set([
  "cervical_depth",
  "cervical_depth_skin",
  "occipital_protrusion",
  "forward_head",
  "hair_thickness_avg",
]);
// 文字列値（cm換算しない）
const STR_KEYS = new Set(["posture", "side_facing"]);

// ---- State -----------------------------------------------------
let poseLandmarker = null;
let imageSegmenter = null;
let visionFileset = null;
let rafId = 0;
let streaming = false;
let lastLandmarks = null; // 最新の検出結果（カメラ起動中のみ更新）
let lastFrameTime = 0;
let fpsEMA = 0;
let videoTrack = null;
let trackCapabilities = null;

// 2段階キャプチャ: 1枚目=正面, 2枚目=横
const STEPS = ["front", "side"];
const STEP_LABELS = { front: "正面", side: "横から" };
let currentStep = "front";
const captures = { front: null, side: null }; // { landmarks, image, values }
let pillowMaterial = null;
let userHeightCm = null;
let aiResult = null; // 1セッション1回キャッシュ
let aiErrorMsg = null;
let aiInFlight = false;
let aiAbortCtrl = null;
let aiCardShown = false; // 素材選択でカード表示済みフラグ

// ---- Status helpers --------------------------------------------
function setStatus(msg, level = "") {
  if (!statusEl) return;
  statusEl.textContent = msg;
  statusEl.className = "status" + (level ? " " + level : "");
}

// ---- MediaPipe 初期化 ------------------------------------------
async function getVision() {
  if (!visionFileset) {
    visionFileset = await FilesetResolver.forVisionTasks(
      "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/wasm"
    );
  }
  return visionFileset;
}

async function initLandmarker() {
  setStatus("MediaPipe モデル読込中…");
  const vision = await getVision();
  poseLandmarker = await PoseLandmarker.createFromOptions(vision, {
    baseOptions: {
      modelAssetPath:
        "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task",
      delegate: "GPU",
    },
    runningMode: "VIDEO",
    numPoses: 1,
    minPoseDetectionConfidence: 0.5,
    minPosePresenceConfidence: 0.5,
    minTrackingConfidence: 0.5,
    outputSegmentationMasks: false,
  });
  setStatus("モデル読込完了");
}

async function initSegmenter() {
  if (imageSegmenter) return imageSegmenter;
  const vision = await getVision();
  // multiclass: 0=背景, 1=髪, 2=体の肌, 3=顔の肌, 4=服, 5=その他
  imageSegmenter = await ImageSegmenter.createFromOptions(vision, {
    baseOptions: {
      modelAssetPath:
        "https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite",
      delegate: "GPU",
    },
    runningMode: "IMAGE",
    outputCategoryMask: true,
    outputConfidenceMasks: false,
  });
  return imageSegmenter;
}

// ---- カメラ起動 ------------------------------------------------
async function startCamera() {
  try {
    if (!poseLandmarker) await initLandmarker();

    setStatus("カメラへのアクセスを求めています…");
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: "environment", // 背面カメラ優先
        width: { ideal: 1920 },
        height: { ideal: 1080 },
      },
      audio: false,
    });
    video.srcObject = stream;
    await video.play();
    streaming = true;
    btnCapture.disabled = false;
    setStatus("検出中 — 全身がフレームに収まるように立ってください", "ok");
    resizeOverlay();

    videoTrack = stream.getVideoTracks()[0] || null;
    await resetZoomToWidest();

    rafId = requestAnimationFrame(loop);
  } catch (e) {
    console.error(e);
    setStatus(
      `カメラ起動失敗: ${e.message || e} — HTTPS または localhost が必要です`,
      "error"
    );
  }
}

// ---- Overlay サイズ同期 ----------------------------------------
function resizeOverlay() {
  const w = video.videoWidth || 720;
  const h = video.videoHeight || 960;
  overlay.width = w;
  overlay.height = h;
  if (stage) {
    stage.style.aspectRatio = `${w} / ${h}`;
    stage.style.height = "";
  }
}

window.addEventListener("resize", resizeOverlay);

// ---- ズーム解除 ------------------------------------------------
async function resetZoomToWidest() {
  if (!videoTrack || typeof videoTrack.getCapabilities !== "function") return;
  try {
    trackCapabilities = videoTrack.getCapabilities();
  } catch {
    trackCapabilities = null;
    return;
  }
  if (trackCapabilities && "zoom" in trackCapabilities) {
    const minZoom = trackCapabilities.zoom.min ?? 1;
    try {
      await videoTrack.applyConstraints({ advanced: [{ zoom: minZoom }] });
    } catch (e) {
      console.warn("zoom 解除に失敗:", e);
    }
  }
}

// ---- 描画ループ ------------------------------------------------
async function loop(ts) {
  if (!streaming || !poseLandmarker) return;
  if (video.readyState >= 2 && video.videoWidth > 0) {
    if (overlay.width !== video.videoWidth) resizeOverlay();

    const result = poseLandmarker.detectForVideo(video, ts);
    ctx.clearRect(0, 0, overlay.width, overlay.height);
    if (result.landmarks && result.landmarks.length > 0) {
      lastLandmarks = result.landmarks[0];
      drawLandmarks(lastLandmarks);
    } else {
      lastLandmarks = null;
    }

    updateSideGuide();

    // FPS
    if (lastFrameTime) {
      const dt = ts - lastFrameTime;
      const fps = 1000 / dt;
      fpsEMA = fpsEMA ? fpsEMA * 0.9 + fps * 0.1 : fps;
      fpsEl.textContent = `FPS: ${fpsEMA.toFixed(1)}`;
    }
    lastFrameTime = ts;
  }
  rafId = requestAnimationFrame(loop);
}

// ---- 真横ガイド ------------------------------------------------
// 側面ステップ時、両肩のx距離が近いほど真横と判定する
function updateSideGuide() {
  if (!sideGuide) return;
  if (sideTips) sideTips.hidden = currentStep !== "side";
  if (currentStep !== "side") {
    sideGuide.hidden = true;
    return;
  }
  if (!lastLandmarks) {
    sideGuide.hidden = false;
    sideGuide.textContent = "✗ 全身が写るように";
    sideGuide.className = "side-guide error";
    return;
  }
  const ls = lastLandmarks[POSE.LEFT_SHOULDER];
  const rs = lastLandmarks[POSE.RIGHT_SHOULDER];
  if (!ls || !rs) {
    sideGuide.hidden = true;
    return;
  }
  const dx = Math.abs(ls.x - rs.x);
  sideGuide.hidden = false;
  if (dx < 0.04) {
    sideGuide.textContent = "✓ 真横OK";
    sideGuide.className = "side-guide ok";
  } else if (dx < 0.08) {
    sideGuide.textContent = "△ あと少し横向きに";
    sideGuide.className = "side-guide warn";
  } else {
    sideGuide.textContent = "✗ 真横に向いてください";
    sideGuide.className = "side-guide error";
  }
}

// ---- ランドマーク描画 ------------------------------------------
const CONNECTIONS = [
  [POSE.LEFT_SHOULDER, POSE.RIGHT_SHOULDER],
  [POSE.LEFT_SHOULDER, POSE.LEFT_ELBOW],
  [POSE.LEFT_ELBOW, POSE.LEFT_WRIST],
  [POSE.RIGHT_SHOULDER, POSE.RIGHT_ELBOW],
  [POSE.RIGHT_ELBOW, POSE.RIGHT_WRIST],
  [POSE.LEFT_SHOULDER, POSE.LEFT_HIP],
  [POSE.RIGHT_SHOULDER, POSE.RIGHT_HIP],
  [POSE.LEFT_HIP, POSE.RIGHT_HIP],
  [POSE.LEFT_HIP, POSE.LEFT_KNEE],
  [POSE.LEFT_KNEE, POSE.LEFT_ANKLE],
  [POSE.RIGHT_HIP, POSE.RIGHT_KNEE],
  [POSE.RIGHT_KNEE, POSE.RIGHT_ANKLE],
  [POSE.NOSE, POSE.LEFT_EAR],
  [POSE.NOSE, POSE.RIGHT_EAR],
];

function drawLandmarks(landmarks) {
  const W = overlay.width;
  const H = overlay.height;
  ctx.strokeStyle = "#4ea3ff";
  ctx.lineWidth = Math.max(2, W / 400);
  ctx.fillStyle = "#ffeb3b";

  // lines
  ctx.beginPath();
  for (const [a, b] of CONNECTIONS) {
    const la = landmarks[a];
    const lb = landmarks[b];
    if (!la || !lb) continue;
    ctx.moveTo(la.x * W, la.y * H);
    ctx.lineTo(lb.x * W, lb.y * H);
  }
  ctx.stroke();

  // points
  const r = Math.max(3, W / 200);
  for (let i = 0; i < landmarks.length; i++) {
    const l = landmarks[i];
    ctx.beginPath();
    ctx.arc(l.x * W, l.y * H, r, 0, Math.PI * 2);
    ctx.fill();
  }
}

// ---- 後頭部突出量（ImageSegmenter で側面シルエットから推定）-----
function loadImage(dataUrl) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = reject;
    img.src = dataUrl;
  });
}

async function computeCervicalProfile(imageDataUrl, landmarks) {
  const segmenter = await initSegmenter();
  const img = await loadImage(imageDataUrl);

  const result = await new Promise((resolve) => {
    segmenter.segment(img, (res) => resolve(res));
  });

  const mask = result.categoryMask;
  if (!mask) return null;
  const w = mask.width;
  const h = mask.height;
  const data = mask.getAsUint8Array();

  // multiclass: 0=背景, 1=髪, 2=体の肌, 3=顔の肌, 4=服, 5=その他
  const isPerson = (v) => v !== 0;
  const isHair = (v) => v === 1;
  const isSkin = (v) => v === 2 || v === 3;

  // visibility が高い側の耳/肩を採用（カメラ向き面）
  const lear = landmarks[POSE.LEFT_EAR];
  const rear = landmarks[POSE.RIGHT_EAR];
  const useLeft = (lear.visibility ?? 0) >= (rear.visibility ?? 0);
  const ear = useLeft ? lear : rear;
  const shoulder = useLeft
    ? landmarks[POSE.LEFT_SHOULDER]
    : landmarks[POSE.RIGHT_SHOULDER];
  const nose = landmarks[POSE.NOSE];

  // 顔の向き: 鼻のx > 耳のx → 右向き（後頭部は画像左側）
  const facingRight = nose.x > ear.x;

  // 行 y で predicate にマッチする「後ろ側」エッジ x を返す
  const backEdge = (y, pred) => {
    if (y < 0 || y >= h) return -1;
    const rowOff = y * w;
    if (facingRight) {
      for (let x = 0; x < w; x++) {
        if (pred(data[rowOff + x])) return x;
      }
    } else {
      for (let x = w - 1; x >= 0; x--) {
        if (pred(data[rowOff + x])) return x;
      }
    }
    return -1;
  };

  const earY = Math.floor(ear.y * h);
  const earX = Math.floor(ear.x * w);
  const shoulderY = Math.floor(shoulder.y * h);

  // ① 後頭部点（髪含む = person 輪郭）
  let occiputHairX = earX;
  let occiputHairY = earY;
  const occRowStart = Math.max(0, earY - Math.floor(h * 0.06));
  const occRowEnd = Math.min(h, earY + Math.floor(h * 0.04));
  for (let y = occRowStart; y < occRowEnd; y++) {
    const x = backEdge(y, isPerson);
    if (x === -1) continue;
    if (facingRight ? x < occiputHairX : x > occiputHairX) {
      occiputHairX = x;
      occiputHairY = y;
    }
  }

  // ② 髪厚の推定（耳より上の頭部領域で「髪エッジ」と「肌エッジ」の差を集計）
  //    顔肌/体の肌の方が髪より前方にあるはずなので、その差が髪の厚み
  const hairSamples = [];
  const headRowStart = Math.max(0, earY - Math.floor(h * 0.18));
  const headRowEnd = Math.max(0, earY - Math.floor(h * 0.02));
  for (let y = headRowStart; y < headRowEnd; y++) {
    const hairX = backEdge(y, isHair);
    const skinX = backEdge(y, isSkin);
    if (hairX === -1 || skinX === -1) continue;
    const diff = facingRight ? skinX - hairX : hairX - skinX;
    if (diff > 0 && diff < w * 0.15) hairSamples.push(diff);
  }
  let hairThicknessPx = 0;
  if (hairSamples.length > 0) {
    hairSamples.sort((a, b) => a - b);
    hairThicknessPx = hairSamples[Math.floor(hairSamples.length / 2)]; // 中央値
  }

  // ③ 髪除外の occiput 推定 = occiput_hair から髪厚分を体内側に補正
  const occiputSkinX = facingRight
    ? occiputHairX + hairThicknessPx
    : occiputHairX - hairThicknessPx;
  const occiputSkinY = occiputHairY;

  // ④ 首の付け根: 肩高さの肌エッジ → 無ければ person で代替
  const napeY = Math.max(0, Math.min(h - 1, shoulderY));
  let napeX = backEdge(napeY, isSkin);
  const napeFromSkin = napeX !== -1;
  if (napeX === -1) napeX = backEdge(napeY, isPerson);
  if (napeX === -1) {
    mask.close();
    return null;
  }
  // person フォールバックの場合は髪厚補正
  const napeSkinX = napeFromSkin
    ? napeX
    : facingRight
    ? napeX + hairThicknessPx
    : napeX - hairThicknessPx;

  // ⑤ 接線→最凹点 の深さ計算（共通関数）
  const concSign = facingRight ? -1 : 1;
  const computeDepth = (oX, oY, nX, nY, contourFn) => {
    const dx = nX - oX;
    const dy = nY - oY;
    const lineLen = Math.hypot(dx, dy);
    if (lineLen === 0) return { depthPx: 0, deepX: oX, deepY: oY };
    let maxDepth = 0;
    let dX = oX;
    let dY = oY;
    for (let y = oY + 1; y < nY; y++) {
      const bx = contourFn(y);
      if (bx === -1) continue;
      const cross = dx * (y - oY) - dy * (bx - oX);
      const signed = (cross / lineLen) * concSign;
      if (signed > maxDepth) {
        maxDepth = signed;
        dX = bx;
        dY = y;
      }
    }
    return { depthPx: maxDepth, deepX: dX, deepY: dY };
  };

  // 髪含み: person 輪郭をそのまま使用
  const hairContour = (y) => backEdge(y, isPerson);
  // 肌のみ: 肌エッジ優先、無ければ person − 髪厚
  const skinContour = (y) => {
    const sx = backEdge(y, isSkin);
    if (sx !== -1) return sx;
    const px = backEdge(y, isPerson);
    if (px === -1) return -1;
    return facingRight ? px + hairThicknessPx : px - hairThicknessPx;
  };

  const depthHair = computeDepth(
    occiputHairX,
    occiputHairY,
    napeX,
    napeY,
    hairContour
  );
  const depthSkin = computeDepth(
    occiputSkinX,
    occiputSkinY,
    napeSkinX,
    napeY,
    skinContour
  );

  mask.close();

  return {
    occipital_protrusion: Math.abs(occiputHairX - earX) / w,
    cervical_depth: depthHair.depthPx / w,
    cervical_depth_skin: depthSkin.depthPx / w,
    hair_thickness_avg: hairThicknessPx / w,
    occiput: { x: occiputHairX / w, y: occiputHairY / h },
    occiput_skin: { x: occiputSkinX / w, y: occiputSkinY / h },
    nape: { x: napeX / w, y: napeY / h, fromSkin: napeFromSkin },
    deepest: { x: depthHair.deepX / w, y: depthHair.deepY / h },
    deepest_skin: { x: depthSkin.deepX / w, y: depthSkin.deepY / h },
    facing: facingRight ? "R" : "L",
  };
}

// ---- キャプチャ処理 --------------------------------------------
function snapshotVideoToDataURL() {
  const w = video.videoWidth;
  const h = video.videoHeight;
  if (!w || !h) return "";
  const c = document.createElement("canvas");
  c.width = w;
  c.height = h;
  const cctx = c.getContext("2d");
  cctx.drawImage(video, 0, 0, w, h);
  return c.toDataURL("image/jpeg", 0.85);
}

function capture() {
  if (!lastLandmarks) {
    setStatus("まだランドマークを検出できていません", "error");
    return;
  }
  try {
    const landmarks = lastLandmarks.map((p) => ({ ...p }));
    const image = snapshotVideoToDataURL();
    const values = calculateAll(landmarks);
    const imgW = video.videoWidth || 0;
    const imgH = video.videoHeight || 0;
    captures[currentStep] = { landmarks, image, values, imgW, imgH };

    // サムネイル更新
    if (currentStep === "front" && image) thumbFront.src = image;
    if (currentStep === "side" && image) thumbSide.src = image;
    if (captures.front || captures.side) thumbs.hidden = false;

    if (currentStep === "front") {
      currentStep = "side";
      dotFront.classList.remove("active");
      dotFront.classList.add("done");
      dotSide.classList.add("active");
      stepText.textContent = "② 横から";
      btnCapture.textContent = "横から測定";
      setStatus("正面 OK — 続けて横向きに立って測定してください", "ok");
    } else {
      dotSide.classList.remove("active");
      dotSide.classList.add("done");
      stepText.textContent = "完了";
      btnCapture.disabled = true;
      btnCapture.textContent = "測定完了";
      renderResults();
      if (heightCard) heightCard.hidden = false;
      materialCard.hidden = false;
      sideGuide.hidden = true;
      if (sideTips) sideTips.hidden = true;
      setStatus("計測完了 — 後頭部解析中…", "ok");
      computeCervicalProfile(image, landmarks)
        .then((res) => {
          if (res && captures.side) {
            captures.side.values.occipital_protrusion = res.occipital_protrusion;
            captures.side.values.cervical_depth = res.cervical_depth;
            captures.side.values.cervical_depth_skin = res.cervical_depth_skin;
            captures.side.values.hair_thickness_avg = res.hair_thickness_avg;
            captures.side.cervicalProfile = res;
            renderResults();
          }
          setStatus("計測完了 — 枕の素材を選択してください", "ok");
        })
        .catch((err) => {
          console.warn("cervical profile failed:", err);
          setStatus("計測完了 — 枕の素材を選択してください", "ok");
        })
        .finally(() => {
          // ★ プリフェッチ: 素材選択を待たず裏でAI診断を開始
          //    素材選択時にはほぼ手元に結果がある状態にする
          kickoffAiFetch();
        });
    }
  } catch (e) {
    console.error(e);
    setStatus(`計算エラー: ${e.message || e}`, "error");
  }
}

// 身長と正面ランドマークから cm 換算スケールを算出
// 解剖学的目安: 肩高 ≈ 0.818 × 身長 / 足首高 ≈ 0.039 × 身長
//             肩-足首 距離 ≈ 0.779 × 身長
function getCmScale() {
  if (!userHeightCm || userHeightCm < 50 || userHeightCm > 250) return null;
  const front = captures.front;
  if (!front?.landmarks) return null;
  const lm = front.landmarks;
  const ls = lm[POSE.LEFT_SHOULDER];
  const rs = lm[POSE.RIGHT_SHOULDER];
  const la = lm[POSE.LEFT_ANKLE];
  const ra = lm[POSE.RIGHT_ANKLE];
  if (!ls || !rs || !la || !ra) return null;
  const shoulderY = (ls.y + rs.y) / 2;
  const ankleY = (la.y + ra.y) / 2;
  const norm = ankleY - shoulderY;
  if (norm <= 0.05) return null;
  const cmPerNormY = (userHeightCm * 0.779) / norm;
  // 横方向は画像幅 cm を別途。正面と側面でアスペクトが違う可能性があるので各々で持つ
  const aspectFront =
    front.imgW && front.imgH ? front.imgW / front.imgH : 9 / 16;
  const aspectSide =
    captures.side?.imgW && captures.side?.imgH
      ? captures.side.imgW / captures.side.imgH
      : aspectFront;
  return {
    cmPerNormY,
    cmPerNormX_front: cmPerNormY * aspectFront,
    cmPerNormX_side: cmPerNormY * aspectSide,
  };
}

function fmtValue(key, val, scale, view) {
  if (val === undefined || val === null) return "—";
  if (STR_KEYS.has(key)) return String(val);
  if (typeof val !== "number") return String(val);
  if (ANGLE_KEYS.has(key)) return val.toFixed(1) + "°";
  const normStr = val.toFixed(3);
  if (!scale) return normStr;
  let cm;
  if (WIDTH_NORM_KEYS.has(key)) {
    cm =
      val *
      (view === "side" ? scale.cmPerNormX_side : scale.cmPerNormX_front);
  } else {
    // body 距離は y 主体で近似
    cm = val * scale.cmPerNormY;
  }
  return `${normStr} (${cm.toFixed(1)} cm)`;
}

function renderResults() {
  resultsCard.hidden = false;
  const order = [
    "right_arm_length",
    "left_arm_length",
    "right_leg_length",
    "left_leg_length",
    "knee_ankle",
    "back_length",
    "back_angle",
    "head_angle",
    "shoulder_angle",
    "hip_angle",
    "neck_hip",
    "hip_knee",
    "right_shoulder_width",
    "left_shoulder_width",
    "right_ear_shoulder",
    "left_ear_shoulder",
    "neck_base",
    "neck_width",
    "head_width",
    "posture",
    "cva",
    "forward_head",
    "head_pitch",
    "neck_tilt",
    "occipital_protrusion",
    "cervical_depth",
    "cervical_depth_skin",
    "hair_thickness_avg",
  ];
  const front = captures.front?.values || {};
  const side = captures.side?.values || {};
  const scale = getCmScale();
  resultsBody.innerHTML = order
    .map((k) => {
      const cls = k === "posture" ? ' class="highlight"' : "";
      const fv = k in front ? fmtValue(k, front[k], scale, "front") : "—";
      const sv = k in side ? fmtValue(k, side[k], scale, "side") : "—";
      return `<tr${cls}><th>${LABELS[k]}</th><td>${fv}</td><td>${sv}</td></tr>`;
    })
    .join("");
}

// ---- リセット --------------------------------------------------
function reset() {
  if (rafId) cancelAnimationFrame(rafId);
  streaming = false;
  lastLandmarks = null;
  if (video.srcObject) {
    for (const t of video.srcObject.getTracks()) t.stop();
    video.srcObject = null;
  }
  videoTrack = null;
  trackCapabilities = null;
  ctx.clearRect(0, 0, overlay.width, overlay.height);
  resultsCard.hidden = true;
  resultsBody.innerHTML = "";
  btnCapture.disabled = true;
  fpsEl.textContent = "FPS: --";

  // 2段階状態を初期化
  currentStep = "front";
  captures.front = null;
  captures.side = null;
  thumbs.hidden = true;
  thumbFront.removeAttribute("src");
  thumbSide.removeAttribute("src");
  dotFront.classList.add("active");
  dotFront.classList.remove("done");
  dotSide.classList.remove("active", "done");
  stepText.textContent = "① 正面";
  btnCapture.textContent = "正面を測定";

  // 枕素材選択を初期化
  pillowMaterial = null;
  materialCard.hidden = true;
  materialSelected.hidden = true;
  materialSelected.textContent = "";
  for (const r of materialRadios) r.checked = false;

  // 身長入力を初期化
  userHeightCm = null;
  if (heightCard) heightCard.hidden = true;
  if (heightInput) heightInput.value = "";

  // AI診断状態を初期化
  if (aiAbortCtrl) {
    aiAbortCtrl.abort();
    aiAbortCtrl = null;
  }
  aiResult = null;
  aiErrorMsg = null;
  aiInFlight = false;
  aiCardShown = false;
  aiCard.hidden = true;
  aiContent.hidden = true;
  aiLoading.hidden = true;
  aiError.hidden = true;
  aiBaseline.textContent = "";
  aiHeadline.textContent = "";
  aiComment.textContent = "";
  aiAdvice.textContent = "";
  aiTags.innerHTML = "";

  // 真横ガイドを初期化
  if (sideGuide) {
    sideGuide.hidden = true;
    sideGuide.textContent = "";
    sideGuide.className = "side-guide";
  }
  if (sideTips) sideTips.hidden = true;

  setStatus("リセット完了");
  // リセット後は自動でカメラを再起動して計測を続行できるようにする
  startCamera();
}

// ---- イベント結線 ----------------------------------------------
btnCapture.addEventListener("click", capture);
btnReset.addEventListener("click", reset);

if (heightInput) {
  heightInput.addEventListener("input", (e) => {
    const v = parseFloat(e.target.value);
    userHeightCm = Number.isFinite(v) && v > 0 ? v : null;
    if (captures.front || captures.side) renderResults();
  });
}

for (const r of materialRadios) {
  r.addEventListener("change", (e) => {
    pillowMaterial = e.target.value;
    materialSelected.hidden = false;
    materialSelected.textContent = `選択中: ${pillowMaterial}`;
    // 素材選択でAIカードを公開（プリフェッチ済みなら即表示）
    revealAiCard();
  });
}

// ---- AI 姿勢診断（Gemini API via Netlify Functions）-------------
function formatMetricsForAI(front, side) {
  const merged = { ...front, ...side };
  const out = {};
  for (const [key, label] of Object.entries(LABELS)) {
    if (key === "posture") continue;
    if (!(key in merged)) continue;
    const v = merged[key];
    if (typeof v !== "number" || !Number.isFinite(v)) continue;
    out[label] = ANGLE_KEYS.has(key)
      ? `${v.toFixed(1)}°`
      : `${v.toFixed(3)}（正規化）`;
  }
  return out;
}

// AI送信用に画像を縮小・圧縮（長辺768px / quality 0.72）
// 元画像の1/5〜1/10サイズになり、アップロードと Gemini 処理が大幅に高速化
async function prepareImageForAI(dataUrl, maxEdge = 768, quality = 0.72) {
  if (!dataUrl) return null;
  const img = await new Promise((resolve, reject) => {
    const i = new Image();
    i.onload = () => resolve(i);
    i.onerror = reject;
    i.src = dataUrl;
  });
  const w = img.naturalWidth;
  const h = img.naturalHeight;
  if (!w || !h) return dataUrl;
  const scale = Math.min(1, maxEdge / Math.max(w, h));
  const tw = Math.round(w * scale);
  const th = Math.round(h * scale);
  const c = document.createElement("canvas");
  c.width = tw;
  c.height = th;
  const cctx = c.getContext("2d");
  cctx.drawImage(img, 0, 0, tw, th);
  return c.toDataURL("image/jpeg", quality);
}

function setAiBaseline(classification) {
  aiBaseline.textContent = `既存ロジック分類: ${
    POSTURE_LABELS[classification] || classification
  }`;
}

function renderAiResult(data) {
  aiHeadline.textContent = data.headline || "";
  aiComment.textContent = data.comment || "";
  aiAdvice.textContent = data.sleep_advice || "";
  aiTags.innerHTML = "";
  for (const tag of data.tags || []) {
    const span = document.createElement("span");
    span.className = "ai-tag";
    span.textContent = tag;
    aiTags.appendChild(span);
  }
  aiLoading.hidden = true;
  aiError.hidden = true;
  aiContent.hidden = false;
}

function renderAiError(msg) {
  aiError.textContent = msg;
  aiError.hidden = false;
  aiLoading.hidden = true;
  aiContent.hidden = true;
}

// 素材選択時にAIカードを公開し、現状のステートを反映する
function revealAiCard() {
  aiCardShown = true;
  const classification =
    captures.side?.values?.posture || captures.front?.values?.posture;
  if (classification) setAiBaseline(classification);
  aiCard.hidden = false;
  aiCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
  if (aiResult) {
    renderAiResult(aiResult);
  } else if (aiErrorMsg) {
    renderAiError(aiErrorMsg);
  } else {
    aiLoading.hidden = false;
    aiContent.hidden = true;
    aiError.hidden = true;
  }
}

// 横撮影完了直後に裏で実行されるプリフェッチ。UIは触らない。
async function kickoffAiFetch() {
  if (aiResult || aiInFlight) return;
  const front = captures.front?.values || {};
  const side = captures.side?.values || {};
  const classification = side.posture || front.posture;
  const rawFront = captures.front?.image;
  const rawSide = captures.side?.image;
  if (!classification || !rawSide) {
    aiErrorMsg = "計測データが不足しています";
    if (aiCardShown) renderAiError(aiErrorMsg);
    return;
  }

  aiInFlight = true;
  aiErrorMsg = null;
  if (aiAbortCtrl) aiAbortCtrl.abort();
  aiAbortCtrl = new AbortController();

  try {
    const [imageFront, imageSide] = await Promise.all([
      rawFront ? prepareImageForAI(rawFront) : Promise.resolve(null),
      prepareImageForAI(rawSide),
    ]);

    const res = await fetch(AI_ENDPOINT, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        classification,
        metrics: formatMetricsForAI(front, side),
        imageFront,
        imageSide,
      }),
      signal: aiAbortCtrl.signal,
    });
    const json = await res.json().catch(() => null);
    if (!res.ok) {
      const detail = json?.error || `HTTP ${res.status}`;
      throw new Error(detail);
    }
    aiResult = json;
    if (aiCardShown) renderAiResult(json);
  } catch (e) {
    if (e.name === "AbortError") return;
    console.warn("AI診断失敗:", e);
    aiErrorMsg = `AI診断に失敗しました: ${e.message || e}`;
    if (aiCardShown) renderAiError(aiErrorMsg);
  } finally {
    aiInFlight = false;
  }
}

// getUserMedia 非対応の早期通知
if (!navigator.mediaDevices?.getUserMedia) {
  setStatus("このブラウザはカメラ API に対応していません", "error");
} else {
  // ページ表示と同時にカメラを自動起動
  startCamera();
}
