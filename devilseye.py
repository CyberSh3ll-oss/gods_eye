#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║         G O D ' S   E Y E  —  OSINT Suite                ║
║         Developed by: Vaishnav Rajeev                    ║
║         Contributors: Rishabh Gurnani                    ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import sys
import subprocess
import threading
import socket
import time

# ── ANSI Colours ─────────────────────────────────────────
BLUE    = "\033[1;34m"
GREEN   = "\033[1;32m"
CYAN    = "\033[1;36m"
YELLOW  = "\033[1;33m"
RED     = "\033[1;31m"
MAGENTA = "\033[1;35m"
BOLD    = "\033[1m"
RESET   = "\033[0m"

# ── Tool name → actual binary mapping ────────────────────
# Keys are display names; values are (binary, apt_package)
TOOL_MAP = {
    "amass":        ("amass",         "amass"),
    "nmap":         ("nmap",          "nmap"),
    "theHarvester": ("theHarvester",  "theharvester"),
    "dnsenum":      ("dnsenum",       "dnsenum"),
    "dnsrecon":     ("dnsrecon",      "dnsrecon"),
    "dirb":         ("dirb",          "dirb"),
    "gobuster":     ("gobuster",      "gobuster"),
    "ffuf":         ("ffuf",          "ffuf"),
    "wapiti":       ("wapiti",        "wapiti"),
    "wpscan":       ("wpscan",        "wpscan"),
    "aircrack-ng":  ("aircrack-ng",   "aircrack-ng"),
    "wifite":       ("wifite",        "wifite"),
}

# ── Helpers ───────────────────────────────────────────────

def clear_screen():
    os.system("clear")


def header():
    print(f"{RED}{BOLD}")
    print("        ◈  ◈  ◈   G O D ' S   E Y E   ◈  ◈  ◈")
    print(f"{CYAN}  " + "═" * 56)
    print(f"            ⚡  O S I N T   S U I T E   ⚡")
    print(f"               Developed by: {RED}VAISHNAV{CYAN}")
    print(f"  " + "═" * 56 + f"{RESET}\n")


def pause():
    input(f"\n{BOLD}{CYAN}  [✓] Done. Press {GREEN}ENTER{CYAN} to return to menu...{RESET}")


def check_internet() -> bool:
    try:
        socket.setdefaulttimeout(3)
        s = socket.create_connection(("8.8.8.8", 53))
        s.close()
        return True
    except OSError:
        return False


def is_installed(binary: str) -> bool:
    return (
        subprocess.call(
            ["which", binary],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        == 0
    )


def best_terminal():
    """Return an installed graphical terminal emulator, or None."""
    if not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")):
        return None

    for term in (
        "qterminal",
        "xfce4-terminal",
        "gnome-terminal",
        "mate-terminal",
        "konsole",
        "terminator",
        "lxterminal",
        "x-terminal-emulator",
        "xterm",
    ):
        if is_installed(term):
