import os
import sys
import subprocess
import time

# ANSI Color Codes
BLUE    = "\033[1;34m"
GREEN   = "\033[1;32m"
CYAN    = "\033[1;36m"
YELLOW  = "\033[1;33m"
RED     = "\033[1;31m"
MAGENTA = "\033[1;35m"
BOLD    = "\033[1m"
RESET   = "\033[0m"

def clear_screen():
    os.system('clear')

def header():
    print(f"{RED}{BOLD}")
    print("      👁️  👁️  👁️   G O D ' S   E Y E   👁️  👁️  👁️")
    print(f"{CYAN}  " + "="*56)
    print(f"        ⚡  O S I N T   S U I T E   ⚡")
    print(f"               Developed by: {RED}VAISHNAV{CYAN}")
    print(f"  " + "="*56 + f"{RESET}\n")

def pause():
    """
    THE CORE FIX:
    After launching any tool, the menu STOPS here and waits.
    It will NOT redraw until you press Enter.
    This prevents the screen from wiping and jumping back to the menu.
    """
    input(f"\n{BOLD}{CYAN}  [✓] Tool launched in new window. Press {GREEN}ENTER{CYAN} to return to menu...{RESET}")

def open_new_terminal(tool_name, script_path):
    """
    Auto-detects the available terminal emulator on Kali and launches
    the script with the correct flags for that specific terminal.
    Tries in order: qterminal -> gnome-terminal -> xfce4-terminal -> xterm
    """

    def try_popen(cmd):
        try:
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"\n{RED}  [!] Launch error: {e}{RESET}")
            return False

    title = f"GOD'S EYE | {tool_name.upper()}"

    # 1. qterminal  — default on Kali XFCE/LXQt, only supports -e (no -T flag)
    if try_popen(['qterminal', '-e', script_path]):
        return

    # 2. gnome-terminal — uses -- separator before command
    if try_popen(['gnome-terminal', '--title', title, '--', 'bash', script_path]):
        return

    # 3. xfce4-terminal
    if try_popen(['xfce4-terminal', '--title', title, '-e', script_path]):
        return

    # 4. xterm — classic, supports -title and -e
    if try_popen(['xterm', '-title', title, '-e', script_path]):
        return

    # 5. Last resort: run inline so it never silently fails
    print(f"\n{RED}  [!] No supported terminal found. Running inline:{RESET}\n")
    subprocess.run(['bash', script_path])



# ──────────────────────────────────────────────────────────────────────────────
# TOOL KNOWLEDGE BASE
# Each entry: binary_name -> (apt_package, help_command, usage_examples)
# help_command : exact shell string to run for help output (2>&1 captures stderr too)
# usage_examples: list of practical example strings shown below the help output
# ──────────────────────────────────────────────────────────────────────────────
TOOL_INFO = {
    # ── HOST / GENERAL OSINT ───────────────────────────────────────────────────
    "amass": (
        "amass",
        "amass --help 2>&1 | head -60",
        [
            "amass enum -d example.com",
            "amass enum -d example.com -o output.txt",
            "amass intel -whois -d example.com",
        ]
    ),
    "dmitry": (
        "dmitry",
        "dmitry 2>&1 | head -40",
        [
            "dmitry -winsepfb example.com",
            "dmitry -p example.com -o output.txt",
            "dmitry -s example.com          # subdomain search",
        ]
    ),
    "nmap": (
        "nmap",
        "nmap --help 2>&1 | head -60",
        [
            "nmap -sV -sC 192.168.1.1",
            "nmap -A -T4 192.168.1.0/24",
            "nmap -p 1-65535 -sS target.com",
            "nmap -sn 192.168.1.0/24        # ping sweep",
        ]
    ),
    "spiderfoot": (
        "spiderfoot",
        "spiderfoot --help 2>&1 | head -50",
        [
            "spiderfoot -l 127.0.0.1:5001   # start web UI",
            "spiderfoot -s example.com -t all",
        ]
    ),
    "theharvester": (
        "theharvester",
        "theHarvester --help 2>&1 | head -50",
        [
            "theHarvester -d example.com -b google",
            "theHarvester -d example.com -b all -l 500",
            "theHarvester -d example.com -b linkedin",
        ]
    ),
    "unicornscan": (
        "unicornscan",
        "unicornscan --help 2>&1 | head -50",
        [
            "unicornscan 192.168.1.1:1-65535",
            "unicornscan -mU 192.168.1.1     # UDP scan",
            "unicornscan -r 10000 192.168.1.0/24",
        ]
    ),
    # ── NETWORK / DNS ──────────────────────────────────────────────────────────
    "dnsenum": (
        "dnsenum",
        "dnsenum --help 2>&1 | head -50",
        [
            "dnsenum example.com",
            "dnsenum --enum example.com",
            "dnsenum --noreverse example.com",
        ]
    ),
    "dnsmap": (
        "dnsmap",
        "dnsmap 2>&1 | head -40",
        [
            "dnsmap example.com",
            "dnsmap example.com -w /usr/share/dnsmap/wordlist_TLAs.txt",
        ]
    ),
    "dnsrecon": (
        "dnsrecon",
        "dnsrecon --help 2>&1 | head -60",
        [
            "dnsrecon -d example.com",
            "dnsrecon -d example.com -t axfr   # zone transfer",
            "dnsrecon -d example.com -t brute",
        ]
    ),
    # ── WEB FINGERPRINTING ─────────────────────────────────────────────────────
    "dirb": (
        "dirb",
        "dirb 2>&1 | head -40",
        [
            "dirb http://target.com",
            "dirb http://target.com /usr/share/wordlists/dirb/big.txt",
            "dirb http://target.com -o results.txt",
        ]
    ),
    "ffuf": (
        "ffuf",
        "ffuf --help 2>&1 | head -60",
        [
            "ffuf -w /usr/share/wordlists/dirb/big.txt -u http://target.com/FUZZ",
            "ffuf -w users.txt:USER -w pass.txt:PASS -u http://target.com/login -d 'u=USER&p=PASS'",
        ]
    ),
    "gobuster": (
        "gobuster",
        "gobuster --help 2>&1 | head -50",
        [
            "gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/big.txt",
            "gobuster dns -d example.com -w /usr/share/wordlists/subdomains.txt",
            "gobuster vhost -u http://target.com -w vhosts.txt",
        ]
    ),
    "recon-ng": (
        "recon-ng",
        "recon-ng --help 2>&1 | head -40",
        [
            "recon-ng                        # starts interactive console",
            "  > marketplace install all",
            "  > workspaces create myproject",
            "  > modules load recon/domains-hosts/hackertarget",
        ]
    ),
    "wfuzz": (
        "wfuzz",
        "wfuzz --help 2>&1 | head -60",
        [
            "wfuzz -w /usr/share/wordlists/dirb/big.txt http://target.com/FUZZ",
            "wfuzz -c -z range,1-100 http://target.com/id=FUZZ",
            "wfuzz -w users.txt -w pass.txt -d 'user=FUZZ&pass=FUZ2Z' http://target.com/login",
        ]
    ),
    # ── WEB VULN ───────────────────────────────────────────────────────────────
    "davtest": (
        "davtest",
        "davtest --help 2>&1 | head -40",
        [
            "davtest -url http://target.com/webdav",
            "davtest -url http://target.com/webdav -auth user:pass",
        ]
    ),
    "skipfish": (
        "skipfish",
        "skipfish --help 2>&1 | head -50",
        [
            "skipfish -o /tmp/skipfish_out http://target.com",
            "skipfish -o /tmp/out -S /usr/share/skipfish/dictionaries/complete.wl http://target.com",
        ]
    ),
    "wapiti": (
        "wapiti",
        "wapiti --help 2>&1 | head -60",
        [
            "wapiti -u http://target.com",
            "wapiti -u http://target.com -m sql,xss",
            "wapiti -u http://target.com --scope domain -o /tmp/report",
        ]
    ),
    "whatweb": (
        "whatweb",
        "whatweb --help 2>&1 | head -50",
        [
            "whatweb http://target.com",
            "whatweb -v http://target.com",
            "whatweb -a 3 http://target.com  # aggression level 3",
        ]
    ),
    "wpscan": (
        "wpscan",
        "wpscan --help 2>&1 | head -60",
        [
            "wpscan --url http://target.com",
            "wpscan --url http://target.com --enumerate u    # users",
            "wpscan --url http://target.com --enumerate p    # plugins",
            "wpscan --url http://target.com -P rockyou.txt   # brute-force",
        ]
    ),
    # ── WIRELESS ───────────────────────────────────────────────────────────────
    "spooftooph": (
        "spooftooph",
        "spooftooph 2>&1 | head -40",
        [
            "spooftooph -i hci0 -a 00:11:22:33:44:55",
            "spooftooph -i hci0 -n 'FakeName' -c 0x000000",
            "spooftooph -i hci0 -s             # scan nearby devices",
        ]
    ),
    "aircrack-ng": (
        "aircrack-ng",
        "aircrack-ng --help 2>&1 | head -50",
        [
            "airmon-ng start wlan0            # enable monitor mode first",
            "airodump-ng wlan0mon             # capture packets",
            "aircrack-ng -w rockyou.txt capture.cap",
        ]
    ),
    "wifite": (
        "wifite",
        "wifite --help 2>&1 | head -60",
        [
            "wifite                           # auto scan & attack",
            "wifite --wpa --dict rockyou.txt",
            "wifite --wps                     # WPS attack only",
        ]
    ),
    # ── SOCIAL ENG ─────────────────────────────────────────────────────────────
    "zphisher": (
        "zphisher",
        "echo 'Zphisher is a phishing framework. Launch it with the command below.'",
        [
            "bash /opt/zphisher/zphisher.sh",
        ]
    ),
}


def launch_cli(tool_name, description):
    """
    1. Checks if the tool binary is installed.
    2. If missing → offers auto-install via apt in a new terminal.
    3. If installed → opens a new terminal showing:
         - Branded GOD'S EYE header
         - Description + curated usage examples
         - Live --help output (correct flag per tool)
         - A live bash prompt for native commands
    """
    clear_screen()
    header()

    # Normalise key: lowercase, strip spaces
    key = tool_name.lower().replace(" ", "")

    # Look up tool knowledge
    apt_pkg, help_cmd, examples = TOOL_INFO.get(key, (key, f"{key} --help 2>&1 | head -50", []))

    print(f"{YELLOW}  [*] Checking {GREEN}{tool_name}{YELLOW}...{RESET}\n")

    # ── INSTALL CHECK ──────────────────────────────────────────────────────────
    # Use the first word of help_cmd as the binary to check
    binary = key if key != "theharvester" else "theHarvester"
    # Special cases where binary name differs from key
    binary_map = {
        "theharvester": "theHarvester",
        "aircrack-ng":  "aircrack-ng",
        "recon-ng":     "recon-ng",
        "zphisher":     None,   # script-based, skip binary check
    }
    binary = binary_map.get(key, key)

    if binary and not is_installed(binary):
        print(f"{RED}  [!] '{tool_name}' is not installed on this system.{RESET}")
        print(f"{CYAN}  Package : {RESET}{apt_pkg}")
        confirm = input(f"\n  {BOLD}Install {tool_name} now via apt? [y/N]: {RESET}").strip().lower()
        if confirm == 'y':
            install_tool(apt_pkg)
            if not is_installed(binary):
                print(f"\n{RED}  [!] Install may have failed. Try: sudo apt-get install {apt_pkg}{RESET}")
                pause()
                return
        else:
            print(f"\n{YELLOW}  [!] Skipping. Tool not launched.{RESET}")
            pause()
            return

    # ── BUILD THE TEMP SCRIPT ──────────────────────────────────────────────────
    script_path = f"/tmp/godseye_{key}.sh"
    with open(script_path, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("clear\n\n")

        # ── Branded header ─────────────────────────────────────────────────────
        f.write("echo -e '\\e[1;31m\\e[1m      👁️  👁️  👁️   G O D S   E Y E   👁️  👁️  👁️\\e[0m'\n")
        f.write("echo -e '\\e[1;36m  ========================================================\\e[0m'\n")
        f.write(f"echo -e '\\e[1;33m          ⚡  {tool_name.upper()}  ⚡\\e[0m'\n")
        f.write("echo -e '\\e[1;36m  ========================================================\\e[0m'\n")
        f.write("echo ''\n")

        # ── Description ────────────────────────────────────────────────────────
        f.write(f"echo -e '\\e[1;34m  DESCRIPTION:\\e[0m'\n")
        f.write(f"echo -e '  {description}'\n")
        f.write("echo ''\n")

        # ── Curated usage examples ──────────────────────────────────────────────
        if examples:
            f.write("echo -e '\\e[1;34m  COMMON USAGE EXAMPLES:\\e[0m'\n")
            for ex in examples:
                # Escape single quotes inside example strings
                ex_escaped = ex.replace("'", "'\\''")
                f.write(f"echo -e '  \\e[1;32m$\\e[0m  {ex_escaped}'\n")
            f.write("echo ''\n")

        # ── Live --help output ──────────────────────────────────────────────────
        f.write("echo -e '\\e[1;34m  TOOL HELP OUTPUT (live from your system):\\e[0m'\n")
        f.write("echo -e '\\e[1;36m  --------------------------------------------------------\\e[0m'\n")
        f.write(f"{help_cmd}\n")
        f.write("echo -e '\\e[1;36m  --------------------------------------------------------\\e[0m'\n")
        f.write("echo ''\n")

        # ── Prompt ─────────────────────────────────────────────────────────────
        f.write("echo -e '\\e[1;32m  [✓] Ready. Type your commands below. Close window when done.\\e[0m'\n")
        f.write("echo ''\n")
        f.write("bash\n")   # Live bash prompt — stays open indefinitely

    os.chmod(script_path, 0o755)
    open_new_terminal(tool_name, script_path)
    pause()

def is_installed(binary):
    """Check if a binary exists on PATH."""
    return subprocess.call(
        ['which', binary],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ) == 0

def install_tool(apt_package):
    """
    Runs apt-get install in a NEW visible terminal window so the user
    can see progress and enter sudo password if needed.
    Blocks until the install window is closed.
    """
    script_path = f"/tmp/godseye_install_{apt_package}.sh"
    with open(script_path, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("clear\n")
        f.write("echo -e '\\e[1;31m\\e[1m'\n")
        f.write("echo '      👁️  👁️  👁️   G O D S   E Y E   👁️  👁️  👁️'\n")
        f.write("echo -e '\\e[1;36m  ========================================================'\n")
        f.write(f"echo -e '  ⚡  INSTALLING: {apt_package.upper()}  ⚡'\n")
        f.write("echo -e '  ========================================================\\e[0m'\n")
        f.write("echo ''\n")
        f.write(f"echo -e '\\e[1;33m  [*] Running: sudo apt-get install -y {apt_package}\\e[0m'\n")
        f.write("echo ''\n")
        f.write(f"sudo apt-get install -y {apt_package}\n")
        f.write("echo ''\n")
        f.write("echo -e '\\e[1;32m  [✓] Done! Close this window to continue.\\e[0m'\n")
        f.write("bash\n")  # Keep open so user sees the result
    os.chmod(script_path, 0o755)

    # Open install terminal — we wait (Popen + communicate) so menu pauses during install
    try:
        proc = subprocess.Popen(['qterminal', '-e', script_path])
        proc.wait()  # Block until the install window is closed
    except FileNotFoundError:
        try:
            proc = subprocess.Popen(['xterm', '-e', script_path])
            proc.wait()
        except Exception as e:
            print(f"\n{RED}  [!] Could not open install terminal: {e}{RESET}")
            print(f"{YELLOW}  [!] Run manually: sudo apt-get install -y {apt_package}{RESET}")
            time.sleep(3)

def launch_gui(tool_name, candidates, apt_package=None):
    """
    Launches a GUI tool in the background.
    `candidates` = list of binary names to try in order.
    `apt_package` = apt package name to install if none of the candidates are found.
    If the tool is missing and apt_package is given, installs it first.
    """
    clear_screen()
    header()
    print(f"{YELLOW}  [*] Launching {GREEN}{tool_name}{YELLOW}...{RESET}\n")

    # Find which binary actually exists
    found_binary = None
    for binary in candidates:
        if is_installed(binary):
            found_binary = binary
            break

    # Not found — offer to install
    if not found_binary:
        if apt_package:
            print(f"{RED}  [!] {tool_name} is not installed.{RESET}")
            print(f"{CYAN}  Package : {RESET}{apt_package}")
            print(f"{CYAN}  Action  : {RESET}A new window will open to install it.\n")
            confirm = input(f"  {BOLD}Install {tool_name} now? [y/N]: {RESET}").strip().lower()
            if confirm == 'y':
                print(f"\n{YELLOW}  [*] Opening install window... close it when done.{RESET}\n")
                install_tool(apt_package)
                # After install, try again
                for binary in candidates:
                    if is_installed(binary):
                        found_binary = binary
                        break
                if not found_binary:
                    print(f"\n{RED}  [!] Install may have failed. Try manually: sudo apt-get install {apt_package}{RESET}")
                    pause()
                    return
            else:
                print(f"\n{YELLOW}  [!] Skipping launch.{RESET}")
                pause()
                return
        else:
            print(f"\n{RED}  [!] {tool_name} binary not found and no install info provided.{RESET}")
            pause()
            return

    # Launch the found binary in background
    print(f"{CYAN}  Binary  : {RESET}{found_binary}")
    print(f"{CYAN}  Status  : {RESET}Launching in background. This menu remains active.\n")
    try:
        subprocess.Popen(
            [found_binary],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"\n{RED}  [!] Error launching {tool_name}: {e}{RESET}")

    pause()

# ──────────────────────────────────────────────
#  MENUS
# ──────────────────────────────────────────────

def main_menu():
    while True:
        clear_screen()
        header()
        print(f"{BLUE}{BOLD}  Select an Operational Vector:{RESET}\n")
        print(f"  {GREEN}[1]{RESET} Host Information & General OSINT Mapping")
        print(f"  {GREEN}[2]{RESET} Network & DNS Infrastructure Reconnaissance")
        print(f"  {GREEN}[3]{RESET} Web Application Fingerprinting & Endpoint Discovery")
        print(f"  {GREEN}[4]{RESET} Web Application Vulnerability Auditing Frameworks")
        print(f"  {GREEN}[5]{RESET} Wireless & Bluetooth Physical Layer Inspection")
        print(f"  {GREEN}[6]{RESET} Social Engineering Assessment Simulator")
        print(f"\n  {RED}[0]{RESET} Terminate Session\n")

        choice = input(f"  {BOLD}Execute Vector [0-6]: {RESET}").strip()

        if   choice == "1": host_menu()
        elif choice == "2": network_menu()
        elif choice == "3": web_scan_menu()
        elif choice == "4": web_vuln_menu()
        elif choice == "5": wireless_menu()
        elif choice == "6": phishing_menu()
        elif choice == "0":
            clear_screen()
            header()
            print(f"  {GREEN}Session terminated. Goodbye, Vaishnav.{RESET}\n")
            sys.exit(0)
        else:
            print(f"\n  {RED}[!] Invalid choice. Try again.{RESET}")
            time.sleep(1)

# ── 1. HOST MENU ────────────────────────────────

def host_menu():
    while True:
        clear_screen()
        header()
        print(f"{MAGENTA}{BOLD}  ── HOST INFORMATION & GENERAL OSINT ──{RESET}\n")
        print(f"  {GREEN}[1]{RESET} Amass           {GREEN}[2]{RESET} Dmitry")
        print(f"  {GREEN}[3]{RESET} Legion (GUI)    {GREEN}[4]{RESET} Nmap")
        print(f"  {GREEN}[5]{RESET} Spiderfoot      {GREEN}[6]{RESET} TheHarvester")
        print(f"  {GREEN}[7]{RESET} Unicornscan     {GREEN}[8]{RESET} Zenmap (GUI)")
        print(f"\n  {RED}[0]{RESET} Return to Main Menu\n")

        choice = input(f"  {BOLD}Select Engine: {RESET}").strip()

        if   choice == "1": launch_cli("amass",       "In-depth attack surface mapping and subdomain enumeration.")
        elif choice == "2": launch_cli("dmitry",      "Deepmagic Info Gathering Tool — whois, ports, emails.")
        elif choice == "3": launch_gui("Legion",      ["legion"],                        apt_package="legion")
        elif choice == "4": launch_cli("nmap",        "Network mapper — port scanning, OS detection, service versioning.")
        elif choice == "5": launch_cli("spiderfoot",  "OSINT asset crawler. Start with: spiderfoot -l 127.0.0.1:5001")
        elif choice == "6": launch_cli("theHarvester","Email & subdomain scraper from public sources.")
        elif choice == "7": launch_cli("unicornscan", "High-throughput, asynchronous TCP/IP port scanner.")
        elif choice == "8": launch_gui("Zenmap",      ["zenmap", "zenmap-kbx", "nmapsi4"], apt_package="zenmap")
        elif choice == "0": break
        else:
            print(f"\n  {RED}[!] Invalid choice.{RESET}"); time.sleep(1)

# ── 2. NETWORK MENU ─────────────────────────────

def network_menu():
    while True:
        clear_screen()
        header()
        print(f"{MAGENTA}{BOLD}  ── NETWORK & DNS INFRASTRUCTURE RECON ──{RESET}\n")
        print(f"  {GREEN}[1]{RESET} Dnsenum        {GREEN}[2]{RESET} Dnsmap")
        print(f"  {GREEN}[3]{RESET} Dnsrecon")
        print(f"\n  {RED}[0]{RESET} Return to Main Menu\n")

        choice = input(f"  {BOLD}Select Engine: {RESET}").strip()

        if   choice == "1": launch_cli("dnsenum",  "DNS enumeration — hostnames, subdomains, MX/NS records.")
        elif choice == "2": launch_cli("dnsmap",   "DNS domain mapping and brute-force subdomain discovery.")
        elif choice == "3": launch_cli("dnsrecon", "DNS reconnaissance — zone transfers, wildcard checks, cache snooping.")
        elif choice == "0": break
        else:
            print(f"\n  {RED}[!] Invalid choice.{RESET}"); time.sleep(1)

# ── 3. WEB SCAN MENU ────────────────────────────

def web_scan_menu():
    while True:
        clear_screen()
        header()
        print(f"{MAGENTA}{BOLD}  ── WEB FINGERPRINTING & ENDPOINT DISCOVERY ──{RESET}\n")
        print(f"  {GREEN}[1]{RESET} Dirb            {GREEN}[2]{RESET} Dirbuster (GUI)")
        print(f"  {GREEN}[3]{RESET} Ffuf            {GREEN}[4]{RESET} Gobuster")
        print(f"  {GREEN}[5]{RESET} Recon-ng        {GREEN}[6]{RESET} Wfuzz")
        print(f"\n  {RED}[0]{RESET} Return to Main Menu\n")

        choice = input(f"  {BOLD}Select Engine: {RESET}").strip()

        if   choice == "1": launch_cli("dirb",     "URL content fuzzer using wordlists to discover hidden paths.")
        elif choice == "2": launch_gui("Dirbuster", ["dirbuster"], apt_package="dirbuster")
        elif choice == "3": launch_cli("ffuf",     "Fast web fuzzer — directories, parameters, virtual hosts.")
        elif choice == "4": launch_cli("gobuster", "Directory & DNS brute-forcer written in Go.")
        elif choice == "5": launch_cli("recon-ng", "Full-featured web intelligence and reconnaissance framework.")
        elif choice == "6": launch_cli("wfuzz",    "Web fuzzer for brute-forcing parameters, auth, paths.")
        elif choice == "0": break
        else:
            print(f"\n  {RED}[!] Invalid choice.{RESET}"); time.sleep(1)

# ── 4. WEB VULN MENU ────────────────────────────

def web_vuln_menu():
    while True:
        clear_screen()
        header()
        print(f"{MAGENTA}{BOLD}  ── WEB APPLICATION VULNERABILITY AUDITING ──{RESET}\n")
        print(f"  {GREEN}[1]{RESET} BurpSuite (GUI) {GREEN}[2]{RESET} Davtest")
        print(f"  {GREEN}[3]{RESET} Skipfish        {GREEN}[4]{RESET} Wapiti")
        print(f"  {GREEN}[5]{RESET} WhatWeb         {GREEN}[6]{RESET} WPScan")
        print(f"\n  {RED}[0]{RESET} Return to Main Menu\n")

        choice = input(f"  {BOLD}Select Engine: {RESET}").strip()

        if   choice == "1": launch_gui("BurpSuite", ["burpsuite"], apt_package="burpsuite")
        elif choice == "2": launch_cli("davtest",  "WebDAV server scanner — tests upload capabilities and vulnerabilities.")
        elif choice == "3": launch_cli("skipfish", "Recursive web app security scanner with intelligent crawling.")
        elif choice == "4": launch_cli("wapiti",   "Black-box web vulnerability scanner — XSS, SQLi, LFI and more.")
        elif choice == "5": launch_cli("whatweb",  "Next-gen web scanner — identifies CMS, frameworks, server info.")
        elif choice == "6": launch_cli("wpscan",   "WordPress vulnerability scanner — users, plugins, themes.")
        elif choice == "0": break
        else:
            print(f"\n  {RED}[!] Invalid choice.{RESET}"); time.sleep(1)

# ── 5. WIRELESS MENU ────────────────────────────

def wireless_menu():
    while True:
        clear_screen()
        header()
        print(f"{MAGENTA}{BOLD}  ── WIRELESS & BLUETOOTH PHYSICAL LAYERS ──{RESET}\n")
        print(f"  {GREEN}[1]{RESET} Spooftooph     {GREEN}[2]{RESET} Aircrack-ng")
        print(f"  {GREEN}[3]{RESET} Wifite")
        print(f"\n  {RED}[0]{RESET} Return to Main Menu\n")

        choice = input(f"  {BOLD}Select Engine: {RESET}").strip()

        if   choice == "1": launch_cli("spooftooph", "Bluetooth device spoofing — clone and impersonate BT devices.")
        elif choice == "2": launch_cli("aircrack-ng","WiFi security auditing — capture, crack WEP/WPA/WPA2 keys.")
        elif choice == "3": launch_cli("wifite",     "Automated wireless network auditor — attacks multiple APs.")
        elif choice == "0": break
        else:
            print(f"\n  {RED}[!] Invalid choice.{RESET}"); time.sleep(1)

# ── 6. PHISHING / SOCIAL ENG MENU ───────────────

def phishing_menu():
    while True:
        clear_screen()
        header()
        print(f"{MAGENTA}{BOLD}  ── SOCIAL ENGINEERING ASSESSMENT ──{RESET}\n")
        print(f"  {GREEN}[1]{RESET} Zphisher")
        print(f"\n  {RED}[0]{RESET} Return to Main Menu\n")

        choice = input(f"  {BOLD}Select Engine: {RESET}").strip()

        if   choice == "1": launch_cli("zphisher", "Phishing page generator. Run: git clone https://github.com/htr-tech/zphisher.git ")
        elif choice == "0": break
        else:
            print(f"\n  {RED}[!] Invalid choice.{RESET}"); time.sleep(1)

# ── ENTRY POINT ─────────────────────────────────

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}[!] Interrupted. Closing GOD'S EYE...{RESET}\n")
        sys.exit(0)
