"""Cliente OpenAI-compatible mínimo con stdlib (sin requests)."""
import json
import urllib.request
import urllib.error


class LLMError(Exception):
    pass


def _post(url, payload, timeout=180):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise LLMError(f"HTTP {e.code}: {body[:400]}") from e


def chat(base_url, model, messages, **kwargs):
    data = {"model": model, "messages": messages, **kwargs}
    return _post(base_url.rstrip("/") + "/chat/completions", data)


def extract_text(resp):
    return resp["choices"][0]["message"]["content"]


def stream_chat(base_url, model, messages, **kwargs):
    """Itera tokens de una respuesta SSE."""
    data = {"model": model, "messages": messages, "stream": True, **kwargs}
    req = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        buf = ""
        for raw in r:
            buf += raw.decode(errors="replace")
            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                line = line.strip()
                if not line.startswith("data:"):
                    continue
                payload = line[5:].strip()
                if payload == "[DONE]":
                    return
                try:
                    chunk = json.loads(payload)
                    delta = chunk["choices"][0]["delta"].get("content")
                    if delta:
                        yield delta
                except (KeyError, json.JSONDecodeError):
                    pass


def health(base_url, timeout=3):
    base = base_url.rstrip("/")
    if base.endswith("/v1"):
        base = base[:-3]
    try:
        with urllib.request.urlopen(base + "/health", timeout=timeout) as r:
            return r.status == 200
    except Exception:
        return False