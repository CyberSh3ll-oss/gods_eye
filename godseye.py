#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║         G O D ' S   E Y E  —  OSINT Suite                ║
║         Developed by: Vaishnav Rajeev                    ║
║         Contributors: Rishabh Gurnani, Puneeth Sai       ║
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
    "wapiti":       ("wapiti3",       "wapiti"),
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
    print(f"                   Developed by: {RED}VAISHNAV{CYAN}")
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


def best_terminal() -> str:
    """Return the first available graphical terminal emulator."""
    for term in ("gnome-terminal", "xfce4-terminal", "konsole", "xterm"):
        if is_installed(term):
            return term
    return "xterm"


def open_in_terminal(tool_display: str, script_path: str):
    """Open a shell script in a new terminal window, non-blocking."""
    term = best_terminal()
    title = f"GOD'S EYE | {tool_display.upper()}"

    cmd_map = {
        "gnome-terminal": ["gnome-terminal", "--title", title, "--", "bash", script_path],
        "xfce4-terminal": ["xfce4-terminal", "--title", title, "-e", f"bash {script_path}"],
        "konsole":        ["konsole", "--title", title, "-e", f"bash {script_path}"],
        "xterm":          ["xterm", "-title", title, "-e", f"bash {script_path}"],
    }
    cmd = cmd_map.get(term, ["xterm", "-e", f"bash {script_path}"])
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def install_tool_interactive(apt_package: str):
    """Install an apt package in a new terminal so the user sees progress."""
    script_path = f"/tmp/godseye_install_{apt_package}.sh"
    with open(script_path, "w") as f:
        f.write(
            f"#!/bin/bash\n"
            f"echo '[*] Installing {apt_package}...'\n"
            f"sudo apt-get install -y {apt_package}\n"
            f"echo '[✓] Done.'\n"
            f"read -p 'Press ENTER to close...' _\n"
        )
    os.chmod(script_path, 0o755)
    term = best_terminal()
    if term == "gnome-terminal":
        subprocess.Popen(["gnome-terminal", "--", "bash", script_path]).wait()
    else:
        subprocess.Popen([term, "-e", f"bash {script_path}"]).wait()


def launch_tool(display_name: str):
    """
    Look up a tool by display name, check if installed,
    optionally install it, then open it in a new terminal.
    """
    if display_name not in TOOL_MAP:
        print(f"{RED}  [!] Unknown tool: {display_name}{RESET}")
        pause()
        return

    binary, apt_pkg = TOOL_MAP[display_name]
    clear_screen()
    header()

    if not is_installed(binary):
        ans = input(
            f"  {YELLOW}[!] '{binary}' not found. Install via apt? [y/N]: {RESET}"
        ).strip().lower()
        if ans == "y":
            install_tool_interactive(apt_pkg)
        else:
            print(f"  {RED}[✗] Skipping launch.{RESET}")
            pause()
            return

    # Re-check after attempted install
    if not is_installed(binary):
        print(f"  {RED}[✗] Installation failed or was cancelled.{RESET}")
        pause()
        return

    script_path = f"/tmp/godseye_{display_name.replace(' ', '_')}.sh"
    with open(script_path, "w") as f:
        f.write(
            f"#!/bin/bash\n"
            f"clear\n"
            f"echo '  [*] {display_name} — interactive session'\n"
            f"echo '  Type your command below (e.g.  {binary} --help)'\n"
            f"echo ''\n"
            f"exec bash\n"
        )
    os.chmod(script_path, 0o755)
    open_in_terminal(display_name, script_path)

    print(f"  {GREEN}[✓] '{display_name}' launched in new terminal.{RESET}")
    pause()


# ── Anonymity Utilities ───────────────────────────────────

def get_current_ip(iface: str) -> str:
    try:
        cmd = (
            f"ip -4 addr show {iface} "
            f"| awk '/inet /{{print $2}}' | cut -d/ -f1"
        )
        ip = subprocess.check_output(
            cmd, shell=True, stderr=subprocess.DEVNULL
        ).decode().strip()
        return ip or "none assigned"
    except Exception:
        return "error"


def mac_changer():
    clear_screen()
    header()
    iface = input(
        f"  {BOLD}Enter interface [default: eth0]: {RESET}"
    ).strip() or "eth0"

    if not is_installed("macchanger"):
        print(f"  {YELLOW}[!] macchanger not found. Installing...{RESET}")
        install_tool_interactive("macchanger")

    print(f"  {CYAN}[*] Randomising MAC on {iface}...{RESET}")
    result = subprocess.run(
        ["sudo", "macchanger", "-r", iface],
        capture_output=True, text=True
    )
    print(result.stdout or result.stderr)
    pause()


def ip_changer():
    clear_screen()
    header()
    iface = input(
        f"  {BOLD}Enter interface [default: eth0]: {RESET}"
    ).strip() or "eth0"

    prev_ip = get_current_ip(iface)
    print(f"\n  {CYAN}[*] Previous IP : {prev_ip}{RESET}")
    print(f"  {CYAN}[*] Cycling MAC and requesting new DHCP lease...{RESET}\n")

    cmds = [
        f"sudo ip link set {iface} down",
        f"sudo macchanger -r {iface}",
        f"sudo ip link set {iface} up",
        "sudo systemctl restart NetworkManager",
    ]
    for c in cmds:
        subprocess.run(c, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"  {YELLOW}[*] Waiting for lease...{RESET}", end="", flush=True)
    for _ in range(8):
        time.sleep(1)
        print(".", end="", flush=True)
    print()

    new_ip = get_current_ip(iface)
    print(f"\n  {GREEN}[✓] Current IP  : {new_ip}{RESET}")
    pause()


def gods_fix():
    """Restore original MAC and verify connectivity — runs ping in a background thread."""
    clear_screen()
    header()
    print(f"  {YELLOW}[*] Rolling back network to original MAC...{RESET}\n")

    restore_cmds = [
        "sudo ip link set eth0 down",
        "sudo macchanger -p eth0",
        "sudo ip link set eth0 up",
        "sudo systemctl restart NetworkManager",
    ]
    for c in restore_cmds:
        subprocess.run(c, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def run_ping():
        print(f"  {CYAN}[*] Testing connectivity (4 packets to 8.8.8.8)...{RESET}\n")
        result = subprocess.run(
            ["ping", "-c", "4", "8.8.8.8"],
            capture_output=True, text=True
        )
        print(result.stdout)
        if "0% packet loss" in result.stdout:
            print(f"  {GREEN}[✓] Network stable.{RESET}")
        else:
            print(f"  {RED}[!] Packet loss detected — check your connection.{RESET}")

    t = threading.Thread(target=run_ping, daemon=True)
    t.start()
    t.join()
    pause()


# ── Browser Launchers ─────────────────────────────────────

def open_url(url: str, label: str):
    clear_screen()
    header()
    print(f"  {CYAN}[*] Opening {label}...{RESET}")
    print(f"  {CYAN}[*] URL: {url}{RESET}\n")
    subprocess.Popen(
        ["xdg-open", url],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print(f"  {GREEN}[✓] Browser process detached.{RESET}")
    pause()


def clone_and_run(label: str, repo_url: str, run_cmd: str):
    """Clone a git repo into /tmp and launch it in a new terminal."""
    clear_screen()
    header()
    folder = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    dest = f"/tmp/{folder}"
    script_path = f"/tmp/godseye_run_{folder}.sh"

    with open(script_path, "w") as f:
        f.write(
            f"#!/bin/bash\n"
            f"echo '[*] Cloning {label}...'\n"
            f"[ -d '{dest}' ] && echo '[*] Already cloned, skipping.' "
            f"|| git clone --depth=1 {repo_url} {dest}\n"
            f"cd {dest}\n"
            f"echo '[*] Launching {label}...'\n"
            f"{run_cmd}\n"
            f"exec bash\n"
        )
    os.chmod(script_path, 0o755)
    open_in_terminal(label, script_path)
    print(f"  {GREEN}[✓] '{label}' launched in new terminal.{RESET}")
    pause()


# ── Sub-menus ─────────────────────────────────────────────

def host_menu():
    options = {
        "1": ("amass",        "Subdomain enumeration"),
        "2": ("nmap",         "Port / service scanning"),
        "3": ("theHarvester", "Email & host harvesting"),
    }
    while True:
        clear_screen()
        header()
        print(f"  {YELLOW}[ Host OSINT ]{RESET}\n")
        for k, (name, desc) in options.items():
            print(f"  {GREEN}[{k}]{RESET} {name:<16} {CYAN}→{RESET} {desc}")
        print(f"\n  {RED}[0]{RESET} Back\n")
        c = input(f"  {BOLD}Vector: {RESET}").strip()
        if c in options:
            launch_tool(options[c][0])
        elif c == "0":
            break


def network_menu():
    options = {
        "1": ("dnsenum",  "DNS record enumeration"),
        "2": ("dnsrecon", "DNS zone & record recon"),
    }
    while True:
        clear_screen()
        header()
        print(f"  {YELLOW}[ DNS Recon ]{RESET}\n")
        for k, (name, desc) in options.items():
            print(f"  {GREEN}[{k}]{RESET} {name:<16} {CYAN}→{RESET} {desc}")
        print(f"\n  {RED}[0]{RESET} Back\n")
        c = input(f"  {BOLD}Vector: {RESET}").strip()
        if c in options:
            launch_tool(options[c][0])
        elif c == "0":
            break


def web_scan_menu():
    options = {
        "1": ("dirb",     "Directory brute-force (wordlist)"),
        "2": ("gobuster", "Directory / DNS brute-force"),
        "3": ("ffuf",     "Fast web fuzzer"),
    }
    while True:
        clear_screen()
        header()
        print(f"  {YELLOW}[ Web Scan ]{RESET}\n")
        for k, (name, desc) in options.items():
            print(f"  {GREEN}[{k}]{RESET} {name:<16} {CYAN}→{RESET} {desc}")
        print(f"\n  {RED}[0]{RESET} Back\n")
        c = input(f"  {BOLD}Vector: {RESET}").strip()
        if c in options:
            launch_tool(options[c][0])
        elif c == "0":
            break


def web_vuln_menu():
    options = {
        "1": ("wapiti",  "Web application vulnerability scanner"),
        "2": ("wpscan",  "WordPress security scanner"),
    }
    while True:
        clear_screen()
        header()
        print(f"  {YELLOW}[ Web Vulnerability Scan ]{RESET}\n")
        for k, (name, desc) in options.items():
            print(f"  {GREEN}[{k}]{RESET} {name:<16} {CYAN}→{RESET} {desc}")
        print(f"\n  {RED}[0]{RESET} Back\n")
        c = input(f"  {BOLD}Vector: {RESET}").strip()
        if c in options:
            launch_tool(options[c][0])
        elif c == "0":
            break


def wireless_menu():
    options = {
        "1": ("aircrack-ng", "WPA/WEP handshake analysis"),
        "2": ("wifite",      "Automated wireless auditing"),
    }
    while True:
        clear_screen()
        header()
        print(f"  {YELLOW}[ Wireless Audit ]{RESET}\n")
        for k, (name, desc) in options.items():
            print(f"  {GREEN}[{k}]{RESET} {name:<16} {CYAN}→{RESET} {desc}")
        print(f"\n  {RED}[0]{RESET} Back\n")
        c = input(f"  {BOLD}Vector: {RESET}").strip()
        if c in options:
            launch_tool(options[c][0])
        elif c == "0":
            break


def integrations_menu():
    while True:
        clear_screen()
        header()
        print(f"  {YELLOW}[ Integrations & External Tools ]{RESET}\n")
        print(f"  {GREEN}[1]{RESET} Aegis Cyber Gateway     {CYAN}→{RESET} Open Aegis portfolio in browser")
        print(f"  {GREEN}[2]{RESET} OSINT Framework          {CYAN}→{RESET} Open osintframework.com")
        print(f"  {GREEN}[3]{RESET} Shannon AI (LLM)         {CYAN}→{RESET} Clone & run Keygraph Shannon")
        print(f"\n  {RED}[0]{RESET} Back\n")
        c = input(f"  {BOLD}Vector: {RESET}").strip()
        if c == "1":
            open_url("https://aegiscybercomms.netlify.app/", "Aegis Cyber Gateway")
        elif c == "2":
            open_url("https://osintframework.com/", "OSINT Framework")
        elif c == "3":
            clone_and_run(
                "Shannon AI",
                "https://github.com/KeygraphHQ/shannon.git",
                "python3 shannon.py 2>/dev/null || python3 main.py 2>/dev/null || bash"
            )
        elif c == "0":
            break


def about():
    clear_screen()
    header()
    print(f"""  {CYAN}{"─"*56}
  [!] PROJECT GOD'S EYE — CREDENTIALS REPORT
  {"─"*56}{RESET}

  {BOLD}Lead Architect{RESET}
  Vaishnav Rajeev — B.Tech Cyber Security
  Specialisation: OSINT, digital forensics, network analysis

  {BOLD}Core Contributors{RESET}
  Rishabh Gurnani -B.Tech Cyber Security
  Puneeth Sai - B.tech Cyber Security 

  {CYAN}{"─"*56}
  Mission
  {"─"*56}{RESET}
  God's Eye consolidates industry-standard reconnaissance
  and OSINT tools into a single, accessible framework for
  ethical hackers, security researchers, and defenders.

  All activities must be performed on systems you own or
  have explicit written authorisation to test.

  {CYAN}{"─"*56}{RESET}
  {MAGENTA}Contact: vaishnav.cvv240888@cvv.ac.in{RESET}
  {CYAN}{"─"*56}{RESET}
""")
    pause()


# ── Main Menu ─────────────────────────────────────────────

def main_menu():
    while True:
        clear_screen()
        header()

        if not check_internet():
            print(f"  {RED}[!] No internet connection detected.{RESET}\n")

        print(f"  {YELLOW}[ Reconnaissance ]{RESET}")
        print(f"  {GREEN}[1]{RESET} Host OSINT        {GREEN}[2]{RESET} DNS Recon")
        print(f"  {GREEN}[3]{RESET} Web Scan          {GREEN}[4]{RESET} Web Vuln")
        print(f"  {GREEN}[5]{RESET} Wireless Audit")

        print(f"\n  {YELLOW}[ Anonymity ]{RESET}")
        print(f"  {GREEN}[6]{RESET} MAC Changer       {GREEN}[7]{RESET} IP Changer")
        print(f"  {GREEN}[8]{RESET} GOD'S FIX")

        print(f"\n  {YELLOW}[ Integrations ]{RESET}")
        print(f"  {GREEN}[9]{RESET} External Tools & Integrations")

        print(f"\n  {YELLOW}[ Info ]{RESET}")
        print(f"  {GREEN}[10]{RESET} About / Authors")
        print(f"\n  {RED}[0]{RESET} Exit\n")

        c = input(f"  {BOLD}Vector: {RESET}").strip()

        routes = {
            "1":  host_menu,
            "2":  network_menu,
            "3":  web_scan_menu,
            "4":  web_vuln_menu,
            "5":  wireless_menu,
            "6":  mac_changer,
            "7":  ip_changer,
            "8":  gods_fix,
            "9":  integrations_menu,
            "10": about,
        }

        if c in routes:
            routes[c]()
        elif c == "0":
            print(f"\n  {CYAN}[*] Session closed. Stay ethical.{RESET}\n")
            sys.exit(0)


# ── Entry Point ───────────────────────────────────────────

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}[!] Interrupted. Exiting cleanly.{RESET}\n")
        sys.exit(0)
