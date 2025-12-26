import time
from typing import Callable

from archon.ui.render import render_layout


MENU = [
    "[1] Observe",
    "[2] Ask",
    "[3] Remain Silent",
    "[4] Leave",
]


def idle_loop(status_supplier: Callable[[], str]):
    try:
        while True:
            render_layout(status_supplier(), MENU)
            time.sleep(2)
    except KeyboardInterrupt:
        return
