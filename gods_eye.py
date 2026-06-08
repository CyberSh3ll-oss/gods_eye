import os
import sys
import subprocess
import time
import socket

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

def check_internet():
    try:
        socket.setdefaulttimeout(3)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("8.8.8.8", 53))
        s.close()
        return True
    except OSError:
        return False

def pause():
    input(f"\n{BOLD}{CYAN}  [✓] Process finished. Press {GREEN}ENTER{CYAN} to return to menu...{RESET}")

def is_installed(binary):
    return subprocess.call(['which', binary], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def install_tool(apt_package):
    script_path = f"/tmp/godseye_install.sh"
    with open(script_path, "w") as f:
        f.write(f"#!/bin/bash\nsudo apt-get install -y {apt_package}\necho '[✓] Done.'\nbash\n")
    os.chmod(script_path, 0o755)
    subprocess.Popen(['xterm', '-e', script_path]).wait()

def open_new_terminal(tool_name, script_path):
    title = f"GOD'S EYE | {tool_name.upper()}"
    cmd = ['qterminal', '-e', script_path] # Fallback to standard
    if is_installed('gnome-terminal'): cmd = ['gnome-terminal', '--title', title, '--', 'bash', script_path]
    elif is_installed('xfce4-terminal'): cmd = ['xfce4-terminal', '--title', title, '-e', script_path]
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def launch_cli(tool_name, description, apt_pkg):
    clear_screen()
    header()
    if not is_installed(tool_name.lower().replace(" ", "")):
        if input(f"  {RED}[!] {tool_name} not found. Install? [y/N]: ").lower() == 'y': install_tool(apt_pkg)
        else: return
    
    script_path = f"/tmp/godseye_{tool_name}.sh"
    with open(script_path, "w") as f:
        f.write(f"#!/bin/bash\nclear\necho 'Launching {tool_name}...'\n{tool_name.lower()} --help\nbash\n")
    os.chmod(script_path, 0o755)
    open_new_terminal(tool_name, script_path)
    pause()

# ── ANONYMITY & FIX FUNCTIONS ──────────────────

def physical_mac_changer():
    os.system("sudo macchanger -r eth0")
    pause()

def get_current_ip(iface):
    try:
        cmd = f"ip -4 addr show {iface} | awk '/inet / {{print $2}}' | cut -d/ -f1"
        ip = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode('utf-8').strip()
        return ip if ip else "None"
    except: return "Error"

def local_ip_changer():
    iface = input(f"  {BOLD}Enter interface [Default eth0]: {RESET}").strip() or "eth0"
    prev_ip = get_current_ip(iface)
    print(f"\n{CYAN}  [*] Previous IP : {prev_ip}{RESET}")
    os.system(f"sudo ip link set {iface} down && sudo macchanger -r {iface} && sudo ip link set {iface} up")
    os.system("sudo systemctl restart NetworkManager")
    time.sleep(6)
    print(f"\n{GREEN}  [*] Current IP : {get_current_ip(iface)}{RESET}")
    pause()

def gods_fix():
    print(f"{YELLOW}  [*] Rolling back network...{RESET}")
    os.system("sudo ip link set eth0 down && sudo macchanger -p eth0 > /dev/null && sudo ip link set eth0 up")
    os.system("sudo systemctl restart NetworkManager")
    time.sleep(8)
    ping = subprocess.run(['ping', '-c', '4', '8.8.8.8'], capture_output=True, text=True)
    print(ping.stdout)
    if "0% packet loss" in ping.stdout: print(f"{GREEN}[✓] Stable.{RESET}")
    else: print(f"{RED}[!] Unstable.{RESET}")
    pause()

# ── MENUS ─────────────────────────────────────

def host_menu():
    while True:
        clear_screen()
        header()
        print(f"  {GREEN}[1]{RESET} Amass  {GREEN}[2]{RESET} Nmap  {GREEN}[3]{RESET} TheHarvester  {RED}[0]{RESET} Back")
        c = input("\n  Select: ")
        if c == "1": launch_cli("amass", "Subdomain enum", "amass")
        elif c == "2": launch_cli("nmap", "Port scan", "nmap")
        elif c == "3": launch_cli("theHarvester", "Email scraper", "theharvester")
        elif c == "0": break

def network_menu():
    while True:
        clear_screen()
        header()
        print(f"  {GREEN}[1]{RESET} Dnsenum  {GREEN}[2]{RESET} Dnsrecon  {RED}[0]{RESET} Back")
        c = input("\n  Select: ")
        if c == "1": launch_cli("dnsenum", "DNS Recon", "dnsenum")
        elif c == "2": launch_cli("dnsrecon", "DNS Recon", "dnsrecon")
        elif c == "0": break

def web_scan_menu():
    while True:
        clear_screen()
        header()
        print(f"  {GREEN}[1]{RESET} Dirb  {GREEN}[2]{RESET} Gobuster  {GREEN}[3]{RESET} Ffuf  {RED}[0]{RESET} Back")
        c = input("\n  Select: ")
        if c == "1": launch_cli("dirb", "Dir scan", "dirb")
        elif c == "2": launch_cli("gobuster", "Dir brute", "gobuster")
        elif c == "3": launch_cli("ffuf", "Fuzzing", "ffuf")
        elif c == "0": break

def web_vuln_menu():
    while True:
        clear_screen()
        header()
        print(f"  {GREEN}[1]{RESET} Wapiti  {GREEN}[2]{RESET} WPScan  {RED}[0]{RESET} Back")
        c = input("\n  Select: ")
        if c == "1": launch_cli("wapiti", "Web scan", "wapiti")
        elif c == "2": launch_cli("wpscan", "WP scan", "wpscan")
        elif c == "0": break

def wireless_menu():
    while True:
        clear_screen()
        header()
        print(f"  {GREEN}[1]{RESET} Aircrack-ng  {GREEN}[2]{RESET} Wifite  {RED}[0]{RESET} Back")
        c = input("\n  Select: ")
        if c == "1": launch_cli("aircrack-ng", "WiFi Crack", "aircrack-ng")
        elif c == "2": launch_cli("wifite", "Auto WiFi", "wifite")
        elif c == "0": break

def phishing_menu():
    while True:
        clear_screen()
        header()
        print(f"  {GREEN}[1]{RESET} Zphisher  {RED}[0]{RESET} Back")
        c = input("\n  Select: ")
        if c == "1": launch_cli("zphisher", "Phishing", "zphisher")
        elif c == "0": break

def main_menu():
    while True:
        clear_screen()
        header()
        print(f"  {GREEN}[1]{RESET} Host OSINT  {GREEN}[2]{RESET} DNS Recon  {GREEN}[3]{RESET} Web Scan")
        print(f"  {GREEN}[4]{RESET} Web Vuln    {GREEN}[5]{RESET} Wireless   {GREEN}[6]{RESET} Phishing")
        print(f"  {GREEN}[7]{RESET} MAC Changer {GREEN}[8]{RESET} IP Changer {GREEN}[9]{RESET} GOD'S FIX")
        print(f"  {RED}[0]{RESET} Exit\n")
        c = input(f"  {BOLD}Vector: {RESET}")
        if c == "1": host_menu()
        elif c == "2": network_menu()
        elif c == "3": web_scan_menu()
        elif c == "4": web_vuln_menu()
        elif c == "5": wireless_menu()
        elif c == "6": phishing_menu()
        elif c == "7": physical_mac_changer()
        elif c == "8": local_ip_changer()
        elif c == "9": gods_fix()
        elif c == "0": sys.exit()

if __name__ == "__main__":
    main_menu()
