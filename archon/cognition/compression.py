import json
from typing import Any, Dict


def compress_snapshot(snapshot: Dict[str, Any]) -> str:
    return json.dumps(snapshot, separators=(',', ':'))
