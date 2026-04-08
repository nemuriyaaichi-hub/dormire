# Dormire Phase 0 計測プロトタイプ

[デプロイ計画書.md](../デプロイ計画書.md) Phase 0（事前検証）のためのスタンドアロンプロトタイプ。

**目的:** MediaPipe Pose がスマートフォンブラウザで動き、既存 Django 版の 20 項目を算出できるかを検証して **Go/No-Go を判定する**。

---

## 🏗️ 構成

ビルドツール不使用の純粋な静的サイト。Netlify にそのまま publish できる。

```
web-prototype/
├── index.html    # 説明ランディングページ（カメラ要求なし）
├── measure.html  # 計測ページ（カメラ許可は同意後）
├── test.html     # calc.js のユニットテスト（合成ランドマーク）
├── app.js        # MediaPipe Pose 統合 + UI
├── calc.js       # 20項目算出の純関数モジュール
├── style.css     # モバイルファースト CSS
├── favicon.svg   # ファビコン
├── netlify.toml  # Netlify 設定（CSP + セキュリティヘッダ）
└── README.md     # このファイル
```

外部依存は CDN 経由で読み込む MediaPipe Tasks Vision (`@mediapipe/tasks-vision@0.10.14`) のみ。`node_modules` もビルド成果物もない。

### 2段階構成の理由

初回訪問時にいきなり `getUserMedia` を呼び出すとブラウザのセーフブラウジングに **フィッシング/マルウェア疑い** として誤検知されやすいため、ページを 2 段階に分けている:

| ページ | 役割 | カメラ権限 |
|---|---|---|
| `index.html` | 説明・プライバシー・同意 | 要求しない |
| `measure.html` | 実際の計測 | ユーザーがボタンで明示的に許可 |

---

## 🚀 ローカルで動かす

カメラ API (`getUserMedia`) は **HTTPS または `localhost`** でしか動かない。

```bash
cd web-prototype
python3 -m http.server 8080
# → http://localhost:8080/ を PC ブラウザで開く
```

スマホ実機で試す場合は後述の Netlify デプロイを使う。

### ユニットテスト

ブラウザで [`test.html`](./test.html) を開くと、合成ランドマークに対する `calc.js` の検算結果が表示される（カメラ不要）。

---

## ☁️ Netlify にデプロイ

### 方法 A: Netlify CLI（最短）

```bash
npm install -g netlify-cli
cd web-prototype
netlify deploy --dir=. --prod
```

初回はブラウザで Netlify にログインを求められる。デプロイ後、`https://xxxxx.netlify.app` の URL がスマホから開ける。

### 方法 B: GitHub 連携

1. このリポジトリを GitHub に push
2. Netlify ダッシュボードで "Import from Git"
3. **Base directory** を `web-prototype` に設定
4. **Publish directory** を `.`（空または `web-prototype`）に
5. Build command は空

---

## 🛡️ Chrome の「危険なサイト」警告が出るとき

Chrome の **Safe Browsing** は、新規ドメインかつカメラなどの権限を要求するページを高確率でフィッシング候補として誤検知する。`netlify.app` サブドメインは **他の利用者の悪用により共有評価が下がっている** ことが多く、同じドメインを使っているだけで警告が出る場合もある。

### 本リポジトリ側で実施済みの対策

- **2段階ページ構成** — 初回訪問時は `index.html`（説明のみ）、計測は `measure.html` に分離。いきなり権限要求しない
- **プライバシー明示** — データをサーバーに送らないこと、ログインや決済がないことを本文で記述
- **favicon と完全な meta タグ** — `description` / `theme-color` / `robots` / `apple-mobile-web-app-*`
- **noindex** — プロトタイプを検索エンジンに晒さない
- **強力な Content-Security-Policy** — 許可ドメインを `jsdelivr` と `storage.googleapis.com` に限定
- **その他セキュリティヘッダ** — HSTS / X-Frame-Options / Referrer-Policy / Permissions-Policy / COOP / CORP

### それでも警告が出る場合の運用側対処

**① Netlify サブドメイン名を変える**

Netlify ダッシュボード → `Site configuration` → `Site details` → `Change site name` で、推測されにくい名前に変更する。例: `dormire-proto-7f3k2` のようにランダム要素を含めると共有評価の影響を受けにくい。

**② Google Safe Browsing に誤検知申告する**

1. Chrome の警告画面で [詳細] → [この安全でないサイトに関するフィードバックを送信] を開く
2. あるいは https://safebrowsing.google.com/safebrowsing/report_error/?hl=ja を直接開く
3. URL と「誤検知です」の説明を送信
4. 通常 24〜72 時間で再評価される

**③ カスタムドメインを使う（最も確実）**

`dormire.co.jp` などのサブドメイン（例: `proto.dormire.co.jp`）を Netlify に紐付ける。独自ドメインは共有評価の影響を受けず、信頼度が大幅に上がる。手順は https://docs.netlify.com/domains-https/custom-domains/ を参照。

**④ Chrome の「保護強化機能」を無効にして個別確認する（一時的）**

設定 → セキュリティ → セーフブラウジング → 「標準の保護機能」に切り替えると、警告が出なくなる場合がある。ただし検証作業者の端末だけでの暫定対応。

---

## 📱 スマホ実機での検証手順

1. スマホブラウザ（iOS Safari / Android Chrome）で Netlify の URL を開く
2. `📷 カメラ起動` をタップ → カメラ権限を許可
3. 背面カメラで人物の全身を映す（3〜4m 離れる）
4. 画面上にランドマークが描画され FPS が表示されたらトラッキング成功
5. `📸 計測` で 20 項目の数値テーブルが表示される

### 想定される落とし穴

| 症状 | 原因 / 対処 |
|---|---|
| `カメラ起動失敗` と出る | HTTPS でない、または `localhost` 以外の生 HTTP |
| iOS Safari で動かない | 最新 iOS 16.4+ が必要。ユーザーアクション（タップ）経由で起動すること |
| FPS が 5 以下 | 低スペック端末。Pose Landmarker の `pose_landmarker_lite` は最軽量版 |
| ランドマークが出ない | フレームに全身が入っていない。照明不足 |

---

## ✅ Go/No-Go 判定チェックリスト

Phase 1 に進む前に以下を **全項目確認** すること。

### 🔴 必須クリア（1つでも NG → 計画変更）

- [ ] **A-1**: iPhone (iOS Safari 最新) 実機でカメラが起動する
- [ ] **A-2**: Android (Chrome 最新) 実機でカメラが起動する
- [ ] **A-3**: MediaPipe Pose のランドマーク描画が表示される
- [ ] **A-4**: FPS が 15 以上出ている（快適な UX の下限）
- [ ] **A-5**: `📸 計測` ボタンで 20 項目すべてに数値が入る
- [ ] **A-6**: Netlify Functions の 10 秒タイムアウト以内でバックエンド処理が完結可能か確信がある（アルゴリズムは数 ms 想定）

### 🟡 精度検証（Phase 1 前に実施）

- [ ] **B-1**: 既存の iOS ネイティブ版で計測した値を記録
- [ ] **B-2**: 同一人物・同一条件でこの Web 版を計測
- [ ] **B-3**: 両者の比率 / 差分をスプレッドシートで比較
- [ ] **B-4**: [recommends/serializers.py:811](../ソースコード/recommends/serializers.py#L811) 等の閾値（例: `shoulder_angle >= 27`）と整合するかを確認
- [ ] **B-5**: 整合しない場合、**キャリブレーション係数**を決めるか、閾値を再調整する方針を決める

### 🟢 保留事項（Phase 1 着手時に再検討）

- `neck_base` / `neck_width` / `head_width` は現状 Pose の耳ランドマークから **近似** している。精度が不足する場合は Face Landmarker を追加統合する必要あり（[calc.js:192](./calc.js#L192) 周辺を差し替え）。
- `classifyPosture()` の閾値は仮実装。Phase 1 で実データと照合して調整する。
- カメラのズーム倍率 / 被写体までの距離によってスケールが変動する。Phase 1 では「距離補正用マーカー」や「基準物体」を導入する選択肢がある。

---

## 📐 20 項目の算出ロジック

[`calc.js`](./calc.js) の `calculateAll(landmarks)` が唯一の入口。

| 項目 | 算出方法 |
|---|---|
| `right_arm_length` | 右肩(12) → 右肘(14) → 右手首(16) の 3D 距離和 |
| `left_arm_length` | 左肩(11) → 左肘(13) → 左手首(15) の 3D 距離和 |
| `right_leg_length` | 右腰(24) → 右膝(26) → 右足首(28) の 3D 距離和 |
| `left_leg_length` | 左腰(23) → 左膝(25) → 左足首(27) の 3D 距離和 |
| `knee_ankle` | 膝→足首距離の左右平均 |
| `back_length` | 肩中点 → 腰中点の 3D 距離 |
| `back_angle` | 同ベクトルの鉛直軸からの角度 (°) |
| `head_angle` | 鼻(0) → 肩中点の鉛直軸からの角度 (°) |
| `shoulder_angle` | 左肩-右肩 を結ぶ線の水平からの角度 (°) |
| `hip_angle` | 左腰-右腰 を結ぶ線の水平からの角度 (°) |
| `right/left_shoulder_width` | 耳 → 肩 の水平距離 |
| `right/left_ear_shoulder` | 耳 → 肩 の垂直距離 |
| `neck_hip` | 肩中点 → 腰中点（= `back_length`） |
| `hip_knee` | 腰 → 膝 の左右平均 |
| `neck_base` / `neck_width` / `head_width` | 耳・鼻からの **近似**（Phase 1 で Face Landmarker に差し替え候補） |
| `posture` | `back_angle` / `head_angle` から "N"/"U"/"W"/"丸" に分類（仮閾値） |

単位は **画像座標の正規化値 [0, 1]**。絶対長（cm）への換算は Phase 1 で基準物体 or キャリブレーションにより対応する。

---

## 🗺️ この後（Phase 1 以降）

Phase 0 の Go/No-Go が **Go** なら:

1. Next.js 15 プロジェクトに移植（`calc.js` は共通ロジックとして流用可能）
2. [recommends/serializers.py](../ソースコード/recommends/serializers.py) 1000 行アルゴリズムを TypeScript に移植（`decimal.js` で `Decimal` 再現）
3. Supabase プロジェクト作成 + スキーマ移植
4. Netlify Functions で `/api/recommends` `/api/orders` `/api/measure` 実装
5. PWA 化 + 10 問ヒアリング UI + 注文フォーム

計画詳細は [../デプロイ計画書.md](../デプロイ計画書.md) の Phase 1〜4 を参照。
