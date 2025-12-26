from rich.panel import Panel


def _bar(percent: float, width: int = 20) -> str:
    filled = int(width * min(max(percent, 0), 100) / 100)
    return "█" * filled + "░" * (width - filled)


def build_snapshot_view(complexity: float, effective_complexity: float, disk_usage: dict) -> Panel:
    percent = disk_usage.get("percent", 0)
    bar = _bar(percent)
    body = (
        f"Storage {bar} {percent:.0f}%\n"
        f"Complexity {complexity:.2f}  (f(x)={effective_complexity:.4f})"
    )
    return Panel(body, title="ARCHON :: SYSTEM STATUS")
