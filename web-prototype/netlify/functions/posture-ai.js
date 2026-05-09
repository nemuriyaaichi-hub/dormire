// ---------------------------------------------------------------
// posture-ai — Gemini API プロキシ（Netlify Functions / V2 構文）
//
// 入力: POST { classification, metrics, imageFront, imageSide }
// 出力:       { headline, comment, tags[], sleep_advice }
//
// 環境変数:
//   GEMINI_API_KEY (必須) — Netlify Site settings に登録
//   GEMINI_MODEL   (任意) — デフォルト: gemini-3.1-flash-preview
// ---------------------------------------------------------------

const DEFAULT_MODEL = "gemini-3.1-flash-preview";

const RESPONSE_SCHEMA = {
  type: "object",
  properties: {
    headline: {
      type: "string",
      description: "1行サマリー（25文字以内）",
    },
    comment: {
      type: "string",
      description: "姿勢解説（100〜140文字、敬語、ですます調）",
    },
    tags: {
      type: "array",
      items: { type: "string" },
      description: "副所見タグ（例: 巻き肩 / 頭部前方変位 / 骨盤後傾）3〜4個",
    },
    sleep_advice: {
      type: "string",
      description: "枕・寝姿勢のアドバイス（70〜100文字）",
    },
  },
  required: ["headline", "comment", "tags", "sleep_advice"],
};

function stripDataUrlPrefix(b64) {
  if (typeof b64 !== "string") return "";
  const idx = b64.indexOf("base64,");
  return idx >= 0 ? b64.slice(idx + "base64,".length) : b64;
}

function buildPromptText({ classification, metrics }) {
  const metricsText = Object.entries(metrics || {})
    .map(([k, v]) => `  - ${k}: ${v}`)
    .join("\n");

  return [
    "あなたは寝具メーカー向けの姿勢分析アシスタントです。",
    "以下の計測データと写真（1枚目=正面、2枚目=横）を統合して、ユーザー向け解説を生成してください。",
    "",
    `【既存ロジックの分類結果】 ${classification}`,
    "  (N=理想姿勢 / 丸=猫背 / U=反り腰 / W=強いS字カーブ)",
    "",
    "【20項目の計測値（整形済み）】",
    metricsText,
    "",
    "【ルール】",
    "  - 既存の分類を否定せず、補強する形で書く",
    "  - comment は「あなた」を主語にした敬語",
    "  - tags は短いキーワードで重複なく3〜5個",
    "  - sleep_advice は枕の高さ・横向き/仰向け推奨など具体的に",
    "  - 医療診断のような断定は避け、寝具選定の参考所見として書く",
  ].join("\n");
}

export default async (req) => {
  if (req.method !== "POST") {
    return json({ error: "POST only" }, 405);
  }

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    return json(
      { error: "GEMINI_API_KEY が未設定です（Netlify環境変数を確認）" },
      500
    );
  }

  let body;
  try {
    body = await req.json();
  } catch {
    return json({ error: "リクエストJSONが不正です" }, 400);
  }

  const { classification, metrics, imageFront, imageSide } = body || {};
  if (!classification || !imageSide) {
    return json(
      { error: "classification と imageSide は必須です" },
      400
    );
  }

  const parts = [{ text: buildPromptText({ classification, metrics }) }];
  if (imageFront) {
    parts.push({
      inline_data: {
        mime_type: "image/jpeg",
        data: stripDataUrlPrefix(imageFront),
      },
    });
  }
  parts.push({
    inline_data: {
      mime_type: "image/jpeg",
      data: stripDataUrlPrefix(imageSide),
    },
  });

  const model = process.env.GEMINI_MODEL || DEFAULT_MODEL;
  const url =
    `https://generativelanguage.googleapis.com/v1beta/models/` +
    `${encodeURIComponent(model)}:generateContent?key=${encodeURIComponent(apiKey)}`;

  const payload = {
    contents: [{ role: "user", parts }],
    generationConfig: {
      response_mime_type: "application/json",
      response_schema: RESPONSE_SCHEMA,
      temperature: 0.4,
    },
  };

  let upstream;
  try {
    upstream = await fetch(url, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(payload),
    });
  } catch (e) {
    return json({ error: `Gemini接続失敗: ${e.message || e}` }, 502);
  }

  const upstreamJson = await upstream.json().catch(() => null);
  if (!upstream.ok) {
    return json(
      {
        error: "Gemini APIエラー",
        status: upstream.status,
        detail: upstreamJson,
      },
      502
    );
  }

  const text =
    upstreamJson?.candidates?.[0]?.content?.parts?.[0]?.text ?? "";
  let parsed;
  try {
    parsed = JSON.parse(text);
  } catch {
    return json({ error: "Gemini出力がJSONとして解釈できません", raw: text }, 502);
  }

  return json(parsed, 200);
};

function json(obj, status) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "content-type": "application/json; charset=utf-8" },
  });
}
