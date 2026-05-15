const CORS_HEADERS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "POST, OPTIONS",
  "access-control-allow-headers": "content-type",
  "access-control-max-age": "86400",
};

export default async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: CORS_HEADERS });
  }
  if (req.method !== "POST") {
    return json({ error: "POST only" }, 405);
  }

  const webhookUrl = process.env.SHEETS_WEBHOOK_URL;
  if (!webhookUrl) {
    return json({ error: "SHEETS_WEBHOOK_URL が未設定です" }, 500);
  }

  let body;
  try {
    body = await req.json();
  } catch {
    return json({ error: "リクエストJSONが不正です" }, 400);
  }

  let upstream;
  try {
    upstream = await fetch(webhookUrl, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(body),
    });
  } catch (e) {
    return json({ error: `スプレッドシート接続失敗: ${e.message || e}` }, 502);
  }

  const text = await upstream.text().catch(() => "");
  if (!upstream.ok) {
    return json(
      {
        error: "スプレッドシート保存エラー",
        status: upstream.status,
        detail: text.slice(0, 500),
      },
      502
    );
  }

  return json({ ok: true }, 200);
};

function json(obj, status) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      ...CORS_HEADERS,
    },
  });
}
