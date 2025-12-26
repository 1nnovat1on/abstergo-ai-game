from dataclasses import dataclass
from typing import Optional


@dataclass
class RuntimeState:
    session_id: str
    last_snapshot: dict
    last_response: Optional[dict] = None
