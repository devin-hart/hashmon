#!/usr/bin/env python3
import os
import requests
import time
import sys
import select
import termios
import tty
from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.align import Align
from dotenv import load_dotenv
load_dotenv()

XLA_ADDRESS = os.getenv("HASHMON_XLA_ADDRESS", "")
SALV_ADDRESS = os.getenv("HASHMON_SALV_ADDRESS", "")
XLA_URL = f"https://fastpool.xyz/api-xla/stats_address?address={XLA_ADDRESS}"
SALV_URL = f"https://fastpool.xyz/api-sal/stats_address?address={SALV_ADDRESS}"

REFRESH_INTERVAL = 30  # seconds
console = Console()

def fetch_stats_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def fetch_all_stats():
    return {
        "xla": fetch_stats_from_url(XLA_URL),
        "salv": fetch_stats_from_url(SALV_URL)
    }

def build_dashboard(data, countdown):
    if "xla" not in data or "salv" not in data:
        return Panel("[red]Error loading stats[/red]")

    panels = []
    for label, dataset in data.items():
        if "error" in dataset:
            panels.append(Panel(f"[red]{label.upper()} error:[/red] {dataset['error']}", border_style="red", padding=(0,1)))
            continue

        stats = dataset.get("stats", {})
        workers = dataset.get("workers", [])
        total_hashrate = stats.get("hashrate", 0)
        active_workers = len([w for w in workers if w.get("hashrate", 0) > 0])

        table = Table(title=f"{label.upper()} Worker Breakdown", show_edge=False, box=None, padding=(0,0))
        table.add_column("Worker", justify="left", no_wrap=True)
        table.add_column("Hashrate (H/s)", justify="right")

        sorted_workers = sorted(
            [w for w in workers if w.get("hashrate", 0) > 0],
            key=lambda w: w.get("name", "").lower()
        )
        top_hashrate = max((w.get("hashrate", 0) for w in sorted_workers), default=0)

        for worker in sorted_workers:
            is_best = worker.get("hashrate", 0) == top_hashrate
            name = worker.get("name") or "(unnamed)"
            rate = f"{worker.get('hashrate', 0):.2f}"

            bold_name = f"[bold yellow]{name}[/bold yellow]" if is_best else f"[bold]{name}[/bold]"
            bold_rate = f"[bold yellow]{rate}[/bold yellow]" if is_best else rate

            table.add_row(bold_name, bold_rate)


        header = f"[green]{label.upper()}[/green]"
        stats_block = f"[bold][green]Total Hashrate:[/green][/bold] {total_hashrate:.2f} H/s   [bold][green]Active Workers:[/green][/bold] {active_workers}\n"

        layout = Align.center(Panel(f"{header}\n\n{stats_block}", border_style="cyan", padding=(0,1)))
        panels.append(Panel.fit(Align.center(Group(layout, table)), border_style="white", padding=(0,1)))

    filled = countdown
    bar = "█" * filled + "░" * (REFRESH_INTERVAL - filled)
    seconds_left = REFRESH_INTERVAL - filled

    countdown_panel = Panel(
        f"[dim]Next update in:[/dim] [{bar}] {seconds_left:2}s",
        border_style="cyan",
        padding=(0, 1)
    )

    quit_note = Align.center("[dim]Press [bold]q[/bold] to quit[/dim]")
    # Wrap all panels (and countdown, quit note) in an outer panel with no forced width
    full_layout = Group(*panels, countdown_panel, quit_note)
    return Align.center(Panel(full_layout, border_style="cyan", padding=(0,1)), width=80)

def key_pressed():
    """Check if a key was pressed (non-blocking, Unix only)"""
    dr, _, _ = select.select([sys.stdin], [], [], 0)
    if dr:
        return sys.stdin.read(1)
    return None

def run_tui():
    countdown = 0
    data = fetch_all_stats()

    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())

    try:
        with Live(build_dashboard(data, countdown), refresh_per_second=1, screen=True) as live:
            while True:
                for countdown in range(REFRESH_INTERVAL):
                    key = key_pressed()
                    if key == "q":
                        raise KeyboardInterrupt
                    live.update(build_dashboard(data, countdown))
                    time.sleep(1)
                data = fetch_all_stats()
    except KeyboardInterrupt:
        console.clear()
        console.print("\n[bold yellow]Exited Scala Hashrate Monitor[/bold yellow]")
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

if __name__ == "__main__":
    run_tui()
