#!/usr/bin/env python3
"""
============================================================
                 G O D ' S   E Y E
                     OSINT Suite

                 Developed by: Vaishnav Rajeev
                 Contributors: Rishabh Gurnani
============================================================
"""

import os
import sys
import subprocess
import threading
import socket
import time

# ANSI colours
BLUE = "\033[1;34m"
GREEN = "\033[1;32m"
CYAN = "\033[1;36m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
MAGENTA = "\033[1;35m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Tool name -> actual Kali binary mapping
# Keys are display names; values are (binary, apt_package)
TOOL_MAP = {
    "amass": ("amass", "amass"),
    "nmap": ("nmap", "nmap"),
    "theHarvester": ("theHarvester", "theharvester"),
    "dnsenum": ("dnsenum", "dnsenum"),
    "dnsrecon": ("dnsrecon", "dnsrecon"),
    "dirb": ("dirb", "dirb"),
    "gobuster": ("gobuster", "gobuster"),
    "ffuf": ("ffuf", "ffuf"),
    "wapiti": ("wapiti", "wapiti"),
    "wpscan": ("wpscan", "wpscan"),
    "aircrack-ng": ("aircrack-ng", "aircrack-ng"),
    "wifite": ("wifite", "wifite"),
}

# Plain-English descriptions, example usage, and the exact help flag per tool
TOOL_INFO = {
    "amass": {
        "what": [
            "Amass is a subdomain discovery and DNS mapping tool.",
            "It finds every subdomain attached to a target domain",
            "using passive and active reconnaissance techniques.",
        ],
        "example": [
            "amass enum -d example.com",
            "amass enum -d example.com -passive",
            "amass enum -d example.com -brute",
        ],
        "help_cmd": "amass -h",
    },
    "nmap": {
        "what": [
            "Nmap scans a target to find open ports and running services.",
            "It tells you what the target machine has exposed to the network",
            "and what software versions are running on each port.",
        ],
        "example": [
            "nmap -sC -sV 192.168.1.1",
            "nmap -p 1-65535 192.168.1.1",
            "nmap -A example.com",
        ],
        "help_cmd": "nmap -h",
    },
    "theHarvester": {
        "what": [
            "theHarvester collects emails, subdomains, IPs and employee names",
            "from public sources like Google, Bing, LinkedIn and Shodan.",
            "Perfect for building an OSINT profile of a target organisation.",
        ],
        "example": [
            "theHarvester -d example.com -b google",
            "theHarvester -d example.com -b all",
            "theHarvester -d example.com -b linkedin",
        ],
        "help_cmd": "theHarvester -h",
    },
    "dnsenum": {
        "what": [
            "dnsenum enumerates DNS records for a domain.",
            "It finds A, MX, NS and SOA records and attempts zone transfers.",
            "Useful for mapping the DNS infrastructure of a target.",
        ],
        "example": [
            "dnsenum example.com",
            "dnsenum --enum example.com",
            "dnsenum --dnsserver 8.8.8.8 example.com",
        ],
        "help_cmd": "dnsenum --help",
    },
    "dnsrecon": {
        "what": [
            "dnsrecon performs deep DNS reconnaissance on a target domain.",
            "It checks for zone transfers, reverse lookups, SRV records",
            "and can brute-force subdomains from a wordlist.",
        ],
        "example": [
            "dnsrecon -d example.com",
            "dnsrecon -d example.com -t axfr",
            "dnsrecon -d example.com -t brt -D /usr/share/wordlists/dnsmap.txt",
        ],
        "help_cmd": "dnsrecon -h",
    },
    "dirb": {
        "what": [
            "dirb brute-forces hidden directories and files on a web server.",
            "It sends requests to a target URL using a wordlist and reports",
            "every path that returns a valid HTTP response.",
        ],
        "example": [
            "dirb https://example.com",
            "dirb https://example.com /usr/share/wordlists/dirb/common.txt",
            "dirb https://example.com -r -z 100",
        ],
        "help_cmd": "dirb",
    },
    "gobuster": {
        "what": [
            "gobuster is a fast directory, DNS and vhost brute-forcer.",
            "It runs multiple threads simultaneously making it much faster",
            "than older tools like dirb for large wordlists.",
        ],
        "example": [
            "gobuster dir -u https://example.com -w /usr/share/wordlists/dirb/common.txt",
            "gobuster dns -d example.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt",
            "gobuster dir -u https://example.com -w /usr/share/wordlists/dirb/big.txt -t 50",
        ],
        "help_cmd": "gobuster help",
    },
    "ffuf": {
        "what": [
            "ffuf (Fuzz Faster U Fool) is a high-speed web fuzzer.",
            "It can fuzz directories, parameters, headers and subdomains.",
            "The FUZZ keyword in the URL marks where the wordlist is injected.",
        ],
        "example": [
            "ffuf -u https://example.com/FUZZ -w /usr/share/wordlists/dirb/common.txt",
            "ffuf -u https://example.com/FUZZ -w /usr/share/wordlists/dirb/common.txt -mc 200",
            "ffuf -u https://FUZZ.example.com -w subdomains.txt -H 'Host: FUZZ.example.com'",
        ],
        "help_cmd": "ffuf -h",
    },
    "wapiti": {
        "what": [
            "wapiti scans a web application for common vulnerabilities.",
            "It tests for SQL injection, XSS, file inclusion, SSRF and more",
            "by crawling the target site and sending crafted payloads.",
        ],
        "example": [
            "wapiti -u https://example.com",
            "wapiti -u https://example.com -f html -o /tmp/wapiti_report",
            "wapiti -u https://example.com --scope domain",
        ],
        "help_cmd": "wapiti -h",
    },
    "wpscan": {
        "what": [
            "wpscan is a WordPress security scanner.",
            "It detects vulnerable plugins, themes and WordPress core versions.",
            "It can also enumerate usernames and brute-force passwords.",
        ],
        "example": [
            "wpscan --url https://example.com",
            "wpscan --url https://example.com --enumerate u",
            "wpscan --url https://example.com --enumerate vp --plugins-detection aggressive",
        ],
        "help_cmd": "wpscan --help",
    },
    "aircrack-ng": {
        "what": [
            "aircrack-ng is a complete suite for auditing wireless networks.",
            "It captures WPA/WEP handshakes and cracks them using wordlists.",
            "Must be used on networks you own or have permission to test.",
        ],
        "example": [
            "airmon-ng start wlan0",
            "airodump-ng wlan0mon",
            "aircrack-ng -w /usr/share/wordlists/rockyou.txt capturefile.cap",
        ],
        "help_cmd": "aircrack-ng --help",
    },
    "wifite": {
        "what": [
            "wifite is an automated wireless auditing tool.",
            "It automates the process of capturing handshakes and attacking",
            "WEP, WPA and WPS networks with minimal manual steps.",
        ],
        "example": [
            "sudo wifite",
            "sudo wifite --wpa --dict /usr/share/wordlists/rockyou.txt",
            "sudo wifite --kill --wps",
        ],
        "help_cmd": "wifite --help",
    },
}


# ─────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────

def clear_screen():
    os.system("clear")


def header():
    print(f"{RED}{BOLD}")
    print("        *  *  *   G O D ' S   E Y E   *  *  *")
    print(f"{CYAN}  " + "=" * 56)
    print("            OSINT SUITE")
    print(f"               Developed by: {RED}VAISHNAV{CYAN}")
    print(f"  " + "=" * 56 + f"{RESET}\n")


def pause():
    input(f"\n{BOLD}{CYAN}  [+] Done. Press {GREEN}ENTER{CYAN} to return to menu...{RESET}")


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
            return term
    return None


def open_in_terminal(tool_display: str, script_path: str, wait: bool = False) -> bool:
    """
    Open a shell script in a new graphical terminal window.
    Returns True if a new window was opened, False if we fell back
    to running in the current terminal.
    """
    term = best_terminal()
    title = f"GOD'S EYE | {tool_display.upper()}"

    if term is None:
        subprocess.run(["bash", script_path])
        return False

    # Every terminal emulator has a different flag syntax.
    # We build the exact correct command for each one.
    if term == "qterminal":
        cmd = ["qterminal", "-T", title, "-e", "bash", script_path]
    elif term == "xfce4-terminal":
        # xfce4-terminal --command must receive the full command as ONE string
        cmd = ["xfce4-terminal", "--title", title, "--command", f"bash {script_path}"]
    elif term in ("gnome-terminal", "mate-terminal"):
        # These use -- to separate terminal args from the command
        cmd = [term, "--title", title, "--", "bash", script_path]
    elif term == "konsole":
        cmd = ["konsole", "--title", title, "-e", "bash", script_path]
    elif term == "terminator":
        cmd = ["terminator", "-T", title, "-x", "bash", script_path]
    else:
        # lxterminal, x-terminal-emulator, xterm — all accept -e "cmd"
        cmd = [term, "-e", f"bash {script_path}"]

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if wait:
            proc.wait()
        return True
    except FileNotFoundError:
        # Terminal vanished between detection and launch
        subprocess.run(["bash", script_path])
        return False


def install_tool_interactive(apt_package: str):
    """Install an apt package in a blocking terminal window."""
    script_path = f"/tmp/godseye_install_{apt_package}.sh"
    with open(script_path, "w") as f:
        f.write(
            "#!/bin/bash\n"
            f"echo '[*] Installing {apt_package}...'\n"
            f"sudo apt-get install -y {apt_package}\n"
            "echo '[+] Done.'\n"
            "read -p 'Press ENTER to close this window...' _\n"
        )
    os.chmod(script_path, 0o755)
    open_in_terminal(f"Install {apt_package}", script_path, wait=True)


# ─────────────────────────────────────────────────────────
# launch_tool — THE ONLY FUNCTION CHANGED FROM THE ORIGINAL
# Opens a clean new terminal showing:
#   1. What the tool does (plain English)
#   2. Example commands with explanations
#   3. The tool's actual --help output
#   4. A live bash shell so the user can run commands freely
# ─────────────────────────────────────────────────────────

def launch_tool(display_name: str):
    if display_name not in TOOL_MAP:
        print(f"{RED}  [!] Unknown tool: {display_name}{RESET}")
        pause()
        return

    binary, apt_pkg = TOOL_MAP[display_name]
    clear_screen()
    header()

    # ── Install check ────────────────────────────────────
    if not is_installed(binary):
        ans = input(
            f"  {YELLOW}[!] '{binary}' not found. Install via apt? [y/N]: {RESET}"
        ).strip().lower()
        if ans == "y":
            install_tool_interactive(apt_pkg)
        else:
            print(f"  {RED}[-] Skipping launch.{RESET}")
            pause()
            return

    if not is_installed(binary):
        print(f"  {RED}[-] Installation failed or was cancelled.{RESET}")
        pause()
        return

    # ── Pull description data ────────────────────────────
    info = TOOL_INFO.get(display_name, {})
    what_lines = info.get("what", [f"{display_name} — no description available."])
    example_lines = info.get("example", [f"{binary} -h"])
    help_cmd = info.get("help_cmd", f"{binary} -h")

    # ── Build the script that runs in the new terminal ───
    # Rules:
    #   - No shlex.quote() around echo strings (adds unwanted literal quotes)
    #   - No read -e -i (not portable, causes "stuck" appearance)
    #   - Run help command directly so output appears immediately
    #   - exec bash at end gives a live shell — user can run their own commands
    script_path = f"/tmp/godseye_{display_name.replace('/', '_')}.sh"

    lines = ["#!/bin/bash", "clear", ""]

    # Header bar
    lines.append("echo '================================================================'")
    lines.append(f"echo '  GOD'\"'\"'S EYE  |  {display_name.upper()}'")
    lines.append("echo '================================================================'")
    lines.append("echo ''")

    # What it does
    lines.append("echo '  WHAT THIS TOOL DOES'")
    lines.append("echo '  -------------------'")
    for line in what_lines:
        # Escape single quotes by ending the string, inserting escaped quote, resuming
        safe = line.replace("'", "'\"'\"'")
        lines.append(f"echo '  {safe}'")
    lines.append("echo ''")

    # Example usage
    lines.append("echo '  EXAMPLE COMMANDS'")
    lines.append("echo '  ----------------'")
    for ex in example_lines:
        safe = ex.replace("'", "'\"'\"'")
        lines.append(f"echo '    {safe}'")
    lines.append("echo ''")

    # Divider before help output
    lines.append("echo '================================================================'")
    lines.append(f"echo '  RUNNING: {help_cmd}'")
    lines.append("echo '================================================================'")
    lines.append("echo ''")

    # Actually run the help command so output appears live
    lines.append(help_cmd)
    lines.append("echo ''")

    # Divider and drop to shell
    lines.append("echo '================================================================'")
    lines.append(f"echo '  Shell ready. Type your {display_name} command and press ENTER.'")
    lines.append("echo '  Type exit to close this window.'")
    lines.append("echo '================================================================'")
    lines.append("echo ''")
    lines.append("exec bash")

    script_content = "\n".join(lines) + "\n"

    with open(script_path, "w") as f:
        f.write(script_content)
    os.chmod(script_path, 0o755)

    # ── Open the new terminal (non-blocking) ─────────────
    opened = open_in_terminal(display_name, script_path, wait=False)

    if opened:
        print(f"  {GREEN}[+] '{display_name}' launched in new terminal window.{RESET}")
    else:
        print(f"  {GREEN}[+] '{display_name}' ran in the current terminal.{RESET}")

    # Small sleep so the new window has time to appear before we print pause()
    time.sleep(0.4)
    pause()


# ─────────────────────────────────────────────────────────
# Anonymity utilities  — UNCHANGED
# ─────────────────────────────────────────────────────────

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
        capture_output=True,
        text=True,
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
    print(f"\n  {GREEN}[+] Current IP  : {new_ip}{RESET}")
    pause()


def gods_fix():
    """Restore original MAC and verify connectivity in a background thread."""
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
            capture_output=True,
            text=True,
        )
        print(result.stdout)
        if "0% packet loss" in result.stdout:
            print(f"  {GREEN}[+] Network stable.{RESET}")
        else:
            print(f"  {RED}[!] Packet loss detected. Check your connection.{RESET}")

    t = threading.Thread(target=run_ping, daemon=True)
    t.start()
    t.join()
    pause()


# ─────────────────────────────────────────────────────────
# Browser launchers  — UNCHANGED
# ─────────────────────────────────────────────────────────

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
    print(f"  {GREEN}[+] Browser process detached.{RESET}")
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
            "#!/bin/bash\n"
            f"echo '[*] Cloning {label}...'\n"
            f"[ -d '{dest}' ] && echo '[*] Already cloned, skipping.' "
            f"|| git clone --depth=1 {repo_url} {dest}\n"
            f"cd {dest}\n"
            f"echo '[*] Launching {label}...'\n"
            f"{run_cmd}\n"
            "exec bash\n"
        )
    os.chmod(script_path, 0o755)
    open_in_terminal(label, script_path)
    print(f"  {GREEN}[+] '{label}' launched in new terminal.{RESET}")
    pause()


# ─────────────────────────────────────────────────────────
# Sub-menus  — UNCHANGED
# ─────────────────────────────────────────────────────────

def host_menu():
    options = {
        "1": ("amass", "Subdomain enumeration"),
        "2": ("nmap", "Port / service scanning"),
        "3": ("theHarvester", "Email & host harvesting"),
    }
    while True:
        clear_screen()
        header()
        print(f"  {YELLOW}[ Host OSINT ]{RESET}\n")
        for k, (name, desc) in options.items():
            print(f"  {GREEN}[{k}]{RESET} {name:<16} {CYAN}->{RESET} {desc}")
        print(f"\n  {RED}[0]{RESET} Back\n")
        c = input(f"  {BOLD}Vector: {RESET}").strip()
        if c in options:
            launch_tool(options[c][0])
        elif c == "0":
            break


def network_menu():
    options = {
        "1": ("dnsenum", "DNS record enumeration"),
        "2": ("dnsrecon", "DNS zone & record recon"),
    }
    while True:
        clear_screen()
        header()
        print(f"  {YELLOW}[ DNS Recon ]{RESET}\n")
        for k, (name, desc) in options.items():
            print(f"  {GREEN}[{k}]{RESET} {name:<16} {CYAN}->{RESET} {desc}")
        print(f"\n  {RED}[0]{RESET} Back\n")
        c = input(f"  {BOLD}Vector: {RESET}").strip()
        if c in options:
            launch_tool(options[c][0])
        elif c == "0":
            break


def web_scan_menu():
    options = {
        "1": ("dirb", "Directory brute-force (wordlist)"),
        "2": ("gobuster", "Directory / DNS brute-force"),
        "3": ("ffuf", "Fast web fuzzer"),
    }
    while True:
        clear_screen()
        header()
        print(f"  {YELLOW}[ Web Scan ]{RESET}\n")
        for k, (name, desc) in options.items():
            print(f"  {GREEN}[{k}]{RESET} {name:<16} {CYAN}->{RESET} {desc}")
        print(f"\n  {RED}[0]{RESET} Back\n")
        c = input(f"  {BOLD}Vector: {RESET}").strip()
        if c in options:
            launch_tool(options[c][0])
        elif c == "0":
            break


def web_vuln_menu():
    options = {
        "1": ("wapiti", "Web application vulnerability scanner"),
        "2": ("wpscan", "WordPress security scanner"),
    }
    while True:
        clear_screen()
        header()
        print(f"  {YELLOW}[ Web Vulnerability Scan ]{RESET}\n")
        for k, (name, desc) in options.items():
            print(f"  {GREEN}[{k}]{RESET} {name:<16} {CYAN}->{RESET} {desc}")
        print(f"\n  {RED}[0]{RESET} Back\n")
        c = input(f"  {BOLD}Vector: {RESET}").strip()
        if c in options:
            launch_tool(options[c][0])
        elif c == "0":
            break


def wireless_menu():
    options = {
        "1": ("aircrack-ng", "WPA/WEP handshake analysis"),
        "2": ("wifite", "Automated wireless auditing"),
    }
    while True:
        clear_screen()
        header()
        print(f"  {YELLOW}[ Wireless Audit ]{RESET}\n")
        for k, (name, desc) in options.items():
            print(f"  {GREEN}[{k}]{RESET} {name:<16} {CYAN}->{RESET} {desc}")
        print(f"\n  {RED}[0]{RESET} Back\n")
        c = input(f"  {BOLD}Vector: {RESET}").strip()
        if c in options:
            launch_tool(options[c][0])
        elif c == "0":
            break


# ─────────────────────────────────────────────────────────
# Integrations  — UNCHANGED
# ─────────────────────────────────────────────────────────

def integrations_menu():
    while True:
        clear_screen()
        header()
        print(f"  {YELLOW}[ Integrations & External Tools ]{RESET}\n")
        print(f"  {GREEN}[1]{RESET} Aegis Cyber Gateway     {CYAN}->{RESET} Open Aegis portfolio in browser")
        print(f"  {GREEN}[2]{RESET} OSINT Framework          {CYAN}->{RESET} Open osintframework.com")
        print(f"  {GREEN}[3]{RESET} Shannon AI (LLM)         {CYAN}->{RESET} Clone & run Keygraph Shannon")
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
                "python3 shannon.py 2>/dev/null || python3 main.py 2>/dev/null || bash",
            )
        elif c == "0":
            break


# ─────────────────────────────────────────────────────────
# About  — UNCHANGED
# ─────────────────────────────────────────────────────────

def about():
    clear_screen()
    header()
    print(f"""  {CYAN}{"-" * 56}
  [!] PROJECT GOD'S EYE - CREDENTIALS REPORT
  {"-" * 56}{RESET}

  {BOLD}Architect{RESET}
  Vaishnav Rajeev - B.Tech Cyber Security
  Specialisation: OSINT, digital forensics, network analysis,
  scripting and automation

  {BOLD}Core Contributors{RESET}
  Rishabh Gurnani - B.Tech Cyber Security
  Specialisation: Governance, risk & compliance (GRC),
  identity and multi-factor authentication

  {CYAN}{"-" * 56}
  Mission
  {"-" * 56}{RESET}
  God's Eye consolidates industry-standard reconnaissance
  and OSINT tools into a single, accessible framework for
  ethical hackers, security researchers, and defenders.

  All activities must be performed on systems you own or
  have explicit written authorisation to test.

  {CYAN}{"-" * 56}{RESET}
  {MAGENTA}Contact: vaishnav.cvv240888@cvv.ac.in{RESET}
  {CYAN}{"-" * 56}{RESET}
""")
    pause()


# ─────────────────────────────────────────────────────────
# Main menu  — UNCHANGED
# ─────────────────────────────────────────────────────────

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
            "1": host_menu,
            "2": network_menu,
            "3": web_scan_menu,
            "4": web_vuln_menu,
            "5": wireless_menu,
            "6": mac_changer,
            "7": ip_changer,
            "8": gods_fix,
            "9": integrations_menu,
            "10": about,
        }

        if c in routes:
            routes[c]()
        elif c == "0":
            print(f"\n  {CYAN}[*] Session closed. Stay ethical.{RESET}\n")
            sys.exit(0)


# ─────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}[!] Interrupted. Exiting cleanly.{RESET}\n")
        sys.exit(0)
