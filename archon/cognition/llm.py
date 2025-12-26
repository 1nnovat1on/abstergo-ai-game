import json
import urllib.error
import urllib.request


DEEPSEEK_ENDPOINT = "https://ollama.com/library/deepseek-r1:latest"


def call_archon(prompt, snapshot):
    payload = json.dumps({
        "prompt": json.dumps({
            "system": prompt,
            "snapshot": snapshot
        })
    }).encode("utf-8")

    request = urllib.request.Request(
        DEEPSEEK_ENDPOINT,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"DeepSeek endpoint returned HTTP {exc.code}: {exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed to reach DeepSeek endpoint: {exc.reason}") from exc

    return json.loads(body)
