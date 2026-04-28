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

// ---- State -----------------------------------------------------
let poseLandmarker = null;
let rafId = 0;
let streaming = false;
let lastLandmarks = null; // 最新の検出結果（カメラ起動中のみ更新）
let lastFrameTime = 0;
let fpsEMA = 0;
let videoTrack = null;
let trackCapabilities = null;

// ---- Status helpers --------------------------------------------
function setStatus(msg, level = "") {
  if (!statusEl) return;
  statusEl.textContent = msg;
  statusEl.className = "status" + (level ? " " + level : "");
}

// ---- MediaPipe 初期化 ------------------------------------------
async function initLandmarker() {
  setStatus("MediaPipe モデル読込中…");
  const vision = await FilesetResolver.forVisionTasks(
    "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/wasm"
  );
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

// ---- キャプチャ処理 --------------------------------------------
function capture() {
  if (!lastLandmarks) {
    setStatus("まだランドマークを検出できていません", "error");
    return;
  }
  try {
    const values = calculateAll(lastLandmarks);
    renderResults(values);
    setStatus("計測完了", "ok");
  } catch (e) {
    console.error(e);
    setStatus(`計算エラー: ${e.message || e}`, "error");
  }
}

function renderResults(values) {
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
  ];
  resultsBody.innerHTML = order
    .map((k) => {
      const v = values[k];
      const cls = k === "posture" ? ' class="highlight"' : "";
      return `<tr${cls}><th>${LABELS[k]}</th><td>${fmt(v)}</td></tr>`;
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
  setStatus("リセット完了");
  // リセット後は自動でカメラを再起動して計測を続行できるようにする
  startCamera();
}

// ---- イベント結線 ----------------------------------------------
btnCapture.addEventListener("click", capture);
btnReset.addEventListener("click", reset);

// getUserMedia 非対応の早期通知
if (!navigator.mediaDevices?.getUserMedia) {
  setStatus("このブラウザはカメラ API に対応していません", "error");
} else {
  // ページ表示と同時にカメラを自動起動
  startCamera();
}
