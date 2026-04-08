// ---------------------------------------------------------------
// Dormire Phase 0 prototype: 20 項目算出ロジック（ピュア関数）
//
// MediaPipe Pose Landmarker が返す landmarks 配列を入力として、
// 既存 Django アプリ (measure/models.py) で定義されている
// 20 項目を算出する。
//
// ⚠️ 注意:
//   - neck_base / neck_width / head_width は Face Landmarker 併用が
//     必要なため、Phase 0 では簡易近似（ears / nose 位置から推定）。
//   - 値の絶対スケールは画像座標の正規化値 [0,1] ベース。
//     Apple Vision との比較にはキャリブレーション必須（計画書 L344）。
// ---------------------------------------------------------------

// MediaPipe Pose の 33 ランドマーク index（主要部位のみ）
export const POSE = Object.freeze({
  NOSE: 0,
  LEFT_EYE_INNER: 1,
  LEFT_EYE: 2,
  LEFT_EYE_OUTER: 3,
  RIGHT_EYE_INNER: 4,
  RIGHT_EYE: 5,
  RIGHT_EYE_OUTER: 6,
  LEFT_EAR: 7,
  RIGHT_EAR: 8,
  MOUTH_LEFT: 9,
  MOUTH_RIGHT: 10,
  LEFT_SHOULDER: 11,
  RIGHT_SHOULDER: 12,
  LEFT_ELBOW: 13,
  RIGHT_ELBOW: 14,
  LEFT_WRIST: 15,
  RIGHT_WRIST: 16,
  LEFT_HIP: 23,
  RIGHT_HIP: 24,
  LEFT_KNEE: 25,
  RIGHT_KNEE: 26,
  LEFT_ANKLE: 27,
  RIGHT_ANKLE: 28,
});

// ---- ベクトル/幾何ユーティリティ ------------------------------
/** ユークリッド距離 (2D) */
export function distance2D(a, b) {
  const dx = a.x - b.x;
  const dy = a.y - b.y;
  return Math.sqrt(dx * dx + dy * dy);
}

/** ユークリッド距離 (3D, z を含む) */
export function distance3D(a, b) {
  const dx = a.x - b.x;
  const dy = a.y - b.y;
  const dz = (a.z ?? 0) - (b.z ?? 0);
  return Math.sqrt(dx * dx + dy * dy + dz * dz);
}

/** 2 点の中点 */
export function midpoint(a, b) {
  return {
    x: (a.x + b.x) / 2,
    y: (a.y + b.y) / 2,
    z: ((a.z ?? 0) + (b.z ?? 0)) / 2,
  };
}

/**
 * 水平軸（+x 方向）からの角度（度）
 * 返り値は [-90, 90] の範囲、上向き負・下向き正（画像座標系 y は下向きが正）
 */
export function angleFromHorizontal(a, b) {
  const dx = b.x - a.x;
  const dy = b.y - a.y;
  const rad = Math.atan2(dy, dx);
  // ±180° を ±90° の範囲に正規化（線の傾きは向き反転しても同じ）
  let deg = (rad * 180) / Math.PI;
  if (deg > 90) deg -= 180;
  if (deg < -90) deg += 180;
  return deg;
}

/**
 * 鉛直軸（+y 方向 = 画像では下向き）からの角度（度、常に非負）
 * back_angle: 肩中点→腰中点のベクトルが鉛直からどれだけ傾いているか。
 */
export function angleFromVertical(a, b) {
  const dx = b.x - a.x;
  const dy = b.y - a.y;
  // 鉛直下向きベクトル (0, 1) との角度
  const rad = Math.atan2(Math.abs(dx), Math.abs(dy));
  return (rad * 180) / Math.PI;
}

/** 絶対水平距離（x 軸方向のみ） */
export function horizontalDistance(a, b) {
  return Math.abs(a.x - b.x);
}

/** 絶対垂直距離（y 軸方向のみ） */
export function verticalDistance(a, b) {
  return Math.abs(a.y - b.y);
}

// ---- 姿勢分類 --------------------------------------------------
/**
 * 背中の曲線から 4 分類 (N/U/W/丸)
 * ⚠️ Phase 0 では仮実装。実機データで閾値調整が必要。
 *
 * - N: 背中がまっすぐ（理想姿勢）
 * - 丸: 猫背（前傾）
 * - U: 反り腰（腰が前に）
 * - W: 強い S 字カーブ
 */
export function classifyPosture(backAngleDeg, headAngleDeg) {
  // 仮の閾値。Phase 0 検証時に実機データで要調整。
  if (backAngleDeg < 5) return "N";
  if (backAngleDeg >= 5 && backAngleDeg < 12) {
    return headAngleDeg > 15 ? "丸" : "U";
  }
  return "W";
}

// ---- メイン関数 ------------------------------------------------
/**
 * MediaPipe Pose の landmarks から 20 項目を算出する。
 *
 * @param {Array<{x:number,y:number,z?:number,visibility?:number}>} landmarks
 *        33 要素の配列（MediaPipe Pose Landmarker 出力）
 * @returns {Object} 20 項目の計測値 + posture 文字列
 */
export function calculateAll(landmarks) {
  if (!Array.isArray(landmarks) || landmarks.length < 29) {
    throw new Error(
      `landmarks must have >=29 entries, got ${landmarks?.length ?? "null"}`
    );
  }

  const ls = landmarks[POSE.LEFT_SHOULDER];
  const rs = landmarks[POSE.RIGHT_SHOULDER];
  const le = landmarks[POSE.LEFT_ELBOW];
  const re = landmarks[POSE.RIGHT_ELBOW];
  const lw = landmarks[POSE.LEFT_WRIST];
  const rw = landmarks[POSE.RIGHT_WRIST];
  const lh = landmarks[POSE.LEFT_HIP];
  const rh = landmarks[POSE.RIGHT_HIP];
  const lk = landmarks[POSE.LEFT_KNEE];
  const rk = landmarks[POSE.RIGHT_KNEE];
  const la = landmarks[POSE.LEFT_ANKLE];
  const ra = landmarks[POSE.RIGHT_ANKLE];
  const lear = landmarks[POSE.LEFT_EAR];
  const rear = landmarks[POSE.RIGHT_EAR];
  const nose = landmarks[POSE.NOSE];

  const shoulderMid = midpoint(ls, rs);
  const hipMid = midpoint(lh, rh);

  // --- 腕 ----------------------------------------------------
  const right_arm_length = distance3D(rs, re) + distance3D(re, rw);
  const left_arm_length = distance3D(ls, le) + distance3D(le, lw);

  // --- 脚 ----------------------------------------------------
  const right_leg_length = distance3D(rh, rk) + distance3D(rk, ra);
  const left_leg_length = distance3D(lh, lk) + distance3D(lk, la);

  // 膝→足首（左右平均）
  const knee_ankle = (distance3D(rk, ra) + distance3D(lk, la)) / 2;

  // --- 体幹 --------------------------------------------------
  const back_length = distance3D(shoulderMid, hipMid);
  const back_angle = angleFromVertical(shoulderMid, hipMid);

  // 頭の傾き: 鼻 → 肩中点のベクトルの鉛直からの角度
  const head_angle = angleFromVertical(nose, shoulderMid);

  // --- 左右の傾き（水平からの角度）---------------------------
  const shoulder_angle = Math.abs(angleFromHorizontal(ls, rs));
  const hip_angle = Math.abs(angleFromHorizontal(lh, rh));

  // --- サポートパッド用 --------------------------------------
  const neck_hip = back_length; // 改修方針では同一扱い
  const hip_knee = (distance3D(rh, rk) + distance3D(lh, lk)) / 2;

  // --- 枕用（肩幅・耳-肩）------------------------------------
  const right_shoulder_width = horizontalDistance(rear, rs);
  const left_shoulder_width = horizontalDistance(lear, ls);
  const right_ear_shoulder = verticalDistance(rear, rs);
  const left_ear_shoulder = verticalDistance(lear, ls);

  // --- 首・頭（Face Landmarker 未統合のため近似）--------------
  // ⚠️ Phase 0 では Pose の耳ランドマークから簡易近似。
  //    精度要件を満たさない場合は Phase 1 で Face Landmarker を追加。
  const head_width = distance2D(lear, rear);
  const neck_base = distance2D(shoulderMid, midpoint(lear, rear)) * 0.35; // 近似
  const neck_width = head_width * 0.6; // 近似

  // --- 姿勢診断 ----------------------------------------------
  const posture = classifyPosture(back_angle, head_angle);

  return {
    right_arm_length,
    left_arm_length,
    right_leg_length,
    left_leg_length,
    knee_ankle,
    back_length,
    back_angle,
    head_angle,
    shoulder_angle,
    hip_angle,
    neck_base,
    neck_width,
    head_width,
    posture,
    neck_hip,
    hip_knee,
    right_shoulder_width,
    left_shoulder_width,
    right_ear_shoulder,
    left_ear_shoulder,
  };
}

/**
 * 20 項目の表示ラベル（日本語）
 * [measure/models.py:31-52](../ソースコード/measure/models.py#L31-L52) と対応。
 */
export const LABELS = Object.freeze({
  right_arm_length: "右腕の長さ",
  left_arm_length: "左腕の長さ",
  right_leg_length: "右足の長さ",
  left_leg_length: "左足の長さ",
  knee_ankle: "膝→足首",
  back_length: "背中の長さ",
  back_angle: "背中の角度 (°)",
  head_angle: "頭の傾き (°)",
  shoulder_angle: "肩の角度 (°)",
  hip_angle: "骨盤の角度 (°)",
  neck_base: "首の付け根 (近似)",
  neck_width: "首の幅 (近似)",
  head_width: "頭の幅 (近似)",
  posture: "姿勢診断",
  neck_hip: "首→骨盤中央",
  hip_knee: "骨盤中央→膝",
  right_shoulder_width: "右半身の肩幅",
  left_shoulder_width: "左半身の肩幅",
  right_ear_shoulder: "右 耳→肩 (垂直)",
  left_ear_shoulder: "左 耳→肩 (垂直)",
});

/** 単位 [0,1] の距離値を見やすく整形（3 桁小数）*/
export function fmt(v) {
  if (typeof v !== "number") return String(v);
  return v.toFixed(3);
}
