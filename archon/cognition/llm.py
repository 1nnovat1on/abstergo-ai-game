import json
import subprocess


def call_archon(prompt, snapshot):
    payload = {
        "prompt": json.dumps({
            "system": prompt,
            "snapshot": snapshot
        })
    }

    result = subprocess.run(
        ["ollama", "run", "deepseek-r1"],
        input=json.dumps(payload),
        text=True,
        capture_output=True
    )

    return json.loads(result.stdout)
