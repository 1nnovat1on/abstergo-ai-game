from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def render_status(message: str):
    console.print(Panel(message, title="ARCHON :: SYSTEM STATUS"))


def render_thoughts(json_text: str):
    console.print(Panel(json_text, title="ARCHON THOUGHTS"))


def render_layout(status_block: str, options):
    console.print(status_block)
    table = Table.grid(padding=1)
    for opt in options:
        table.add_row(opt)
    console.print(Panel(table, title="OPTIONS"))
