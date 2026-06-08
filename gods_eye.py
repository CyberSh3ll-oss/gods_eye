import os
import sys
import subprocess
import time

# ANSI Color Codes for an amazing terminal UI
BLUE = "\033[1;34m"
GREEN = "\033[1;32m"
CYAN = "\033[1;36m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
MAGENTA = "\033[1;35m"
BOLD = "\033[1m"
RESET = "\033[0m"

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def header():
    print(f"{CYAN}{BOLD}" + "👁️  " + "="*56 + "  👁️")
    print(f"        ⚡ G O D ' S   E Y E  :  O S I N T   S U I T E ⚡")
    print(f"               Developed by: {YELLOW}Osint_by_vaishnav{CYAN}")
    print(f" " + "="*60 + f"{RESET}\n")

def display_tool_info(name, desc, usage_examples):
    clear_screen()
    header()
    print(f"{MAGENTA}{BOLD}[ TOOL INTERFACE: {name} ]{RESET}")
    print(f"{BLUE}{BOLD}Description:{RESET} {desc}\n")
    print(f"{YELLOW}{BOLD}Educational Reference & Basic Command Flags:{RESET}")
    for cmd, explanation in usage_examples.items():
        print(f"  {GREEN}{cmd}{RESET} -> {explanation}")
    print("\n" + f"{RED}" + "-"*60 + f"{RESET}")
    input(f"\n{BOLD}Press [ENTER] to initialize or view tool parameters...{RESET}")

def run_command(command_list):
    try:
        subprocess.run(command_list)
    except FileNotFoundError:
        print(f"\n{RED}[!] Notice: Dynamic execution restricted. Tool requires target args or GUI display mapping.{RESET}")
        input("\nPress Enter to return...")
    except Exception as e:
        print(f"\n{RED}[!] Framework runtime notice: {e}{RESET}")
        input("\nPress Enter to return...")

def main_menu():
    while True:
        clear_screen()
        header()
        print(f"{BLUE}{BOLD}Select an Operational Vector to Begin Blueprint Discovery:{RESET}\n")
        print(f"  {GREEN}1.{RESET} Host Information & General OSINT Mapping")
        print(f"  {GREEN}2.{RESET} Network & DNS Infrastructure Reconnaissance")
        print(f"  {GREEN}3.{RESET} Web Application Fingerprinting & Endpoint Discovery")
        print(f"  {GREEN}4.{RESET} Web Application Vulnerability Auditing Frameworks")
        print(f"  {GREEN}5.{RESET} Wireless & Bluetooth Physical Layer Inspection")
        print(f"  {GREEN}6.{RESET} Social Engineering Assessment Simulator")
        print(f"  {RED}0. Terminate Session (Exit){RESET}\n")
        
        choice = input(f"{BOLD}Execute Vector [0-6]: {RESET}").strip()
        
        if choice == "1":
            host_menu()
        elif choice == "2":
            network_menu()
        elif choice == "3":
            web_scan_menu()
        elif choice == "4":
            web_vuln_menu()
        elif choice == "5":
            wireless_menu()
        elif choice == "6":
            phishing_menu()
        elif choice == "0":
            print(f"\n{GREEN}Closing GOD'S EYE framework session. Goodbye, Vaishnav.{RESET}")
            sys.exit(0)
        else:
            print(f"{RED}Invalid Vector Option!{RESET}")
            time.sleep(1)

def host_menu():
    while True:
        clear_screen()
        header()
        print(f"{MAGENTA}{BOLD}--- HOST INFORMATION & GENERAL OSINT ---{RESET}\n")
        print(f"  {GREEN}1.{RESET} Amass          {GREEN}2.{RESET} Dmitry")
        print(f"  {GREEN}3.{RESET} Legion         {GREEN}4.{RESET} Nmap (Vulnerability Scanner Mode)")
        print(f"  {GREEN}5.{RESET} Spiderfoot     {GREEN}6.{RESET} TheHarvester")
        print(f"  {GREEN}7.{RESET} Unicornscan    {GREEN}8.{RESET} Zenmap (GUI Interface)")
        print(f"  {RED}0. Return to Main Core{RESET}\n")
        
        choice = input(f"{BOLD}Select Engine: {RESET}").strip()
        
        if choice == "1":
            display_tool_info("Amass", 
                "In-depth attack surface mapping and external asset discovery engine.",
                {"amass enum -d target.com": "Execute passive subdomain harvesting against a primary target zone."})
            run_command(["amass", "--help"])
        elif choice == "2":
            display_tool_info("Dmitry (Deepmagic Information Gathering Tool)", 
                "Gathers public host records including subdomains, email strings, uptime status, and WHOIS entries.",
                {"dmitry -wnpb target.com": "Run an integrated lookup spanning WHOIS details, Netcraft indices, and basic port states."})
            run_command(["dmitry"])
        elif choice == "3":
            display_tool_info("Legion", "An automated, modular network pentesting tool and infrastructure scanner.", {"legion": "Launch the multi-threaded host discovery and tracking wizard UI."})
            run_command(["legion", "--help"])
        elif choice == "4":
            display_tool_info("Nmap Core Engine", "The premier network mapper designed for port state tracking and OS signature detection.", {
                "nmap -sV -sC target_ip": "Detect active software versions and run standard vulnerability scripts.",
                "nmap --script vuln target_ip": "Query target assets for prominent software flaws using the NSE engine."
            })
            target = input("Enter target IP/Domain to scan (or press enter for help text): ").strip()
            if target: run_command(["nmap", "-sV", target])
            else: run_command(["nmap", "--help"])
        elif choice == "5":
            display_tool_info("Spiderfoot", "Automated OSINT asset crawler capable of parsing over 100 open data repositories simultaneously.", {"spiderfoot -l 127.0.0.1:5001": "Spin up the localized operational web interface server over port 5001."})
            run_command(["spiderfoot", "--help"])
        elif choice == "6":
            display_tool_info("TheHarvester", "Catalogs intelligence metadata including emails, subdomains, subnets, and employee listings using open search pipelines.", {"theHarvester -d target.com -l 300 -b google": "Scrape open search engines for the first 300 hits matching target domains."})
            run_command(["theHarvester", "--help"])
        elif choice == "7":
            display_tool_info("Unicornscan", "An asynchronous, high-throughput port tracking engine designed for rapid scale deployments.", {"unicornscan -mT target_ip:1-1024": "Launch an asynchronous TCP scan checking ports 1 through 1024."})
            run_command(["unicornscan", "--help"])
        elif choice == "8":
            display_tool_info("Zenmap", "The official graphical dashboard utility engineered for visual management of Nmap data sets.", {"zenmap": "Instantiates the visualization platform dashboard window."})
            run_command(["zenmap-kbx", "--help"])
        elif choice == "0":
            break

def network_menu():
    while True:
        clear_screen()
        header()
        print(f"{MAGENTA}{BOLD}--- NETWORK & DNS INFRASTRUCTURE RECON ---{RESET}\n")
        print(f"  {GREEN}1.{RESET} Dnsenum")
        print(f"  {GREEN}2.{RESET} Dnsmap")
        print(f"  {GREEN}3.{RESET} Dnsrecon")
        print(f"  {RED}0. Return to Main Core{RESET}\n")
        
        choice = input(f"{BOLD}Select Engine: {RESET}").strip()
        if choice == "1":
            display_tool_info("Dnsenum", "Identifies all critical DNS asset lines, records, and subdomains.", {"dnsenum target.com": "Enumerate zone definitions and attempt standard AXFR inter-server transfers."})
            run_command(["dnsenum", "--help"])
        elif choice == "2":
            display_tool_info("Dnsmap", "Subdomain dictionary brute-forcer designed for localized network environments.", {"dnsmap target.com -w wordlist.txt": "Brute force structural assets utilizing custom text directories."})
            run_command(["dnsmap"])
        elif choice == "3":
            display_tool_info("Dnsrecon", "Advanced DNS administration inspection platform analyzing SOA, wildcard domains, and SRV rows.", {"dnsrecon -d target.com -t std": "Execute standard lookup sweeps pulling fundamental name configs."})
            run_command(["dnsrecon", "--help"])
        elif choice == "0":
            break

def web_scan_menu():
    while True:
        clear_screen()
        header()
        print(f"{MAGENTA}{BOLD}--- WEB APPLICATION FINGERPRINTING & DISCOVERY ---{RESET}\n")
        print(f"  {GREEN}1.{RESET} Dirb          {GREEN}2.{RESET} Dirbuster")
        print(f"  {GREEN}3.{RESET} Ffuf          {GREEN}4.{RESET} Gobuster")
        print(f"  {GREEN}5.{RESET} Recon-ng      {GREEN}6.{RESET} Wfuzz")
        print(f"  {RED}0. Return to Main Core{RESET}\n")
        
        choice = input(f"{BOLD}Select Engine: {RESET}").strip()
        if choice == "1":
            display_tool_info("Dirb", "URL Content dictionary fuzzer tracking unlinked system directories.", {"dirb http://target.com/": "Scan host endpoints using default system path dictionaries."})
            run_command(["dirb"])
        elif choice == "2":
            display_tool_info("Dirbuster", "Multi-threaded GUI web directory crawler map engine.", {"dirbuster": "Initializes the multi-thread interface window."})
            run_command(["dirbuster", "--help"])
        elif choice == "3":
            display_tool_info("Ffuf (Fast Fuzzing)", "A high-performance web endpoint dictionary fuzzer compiled in Go.", {"ffuf -w words.txt -u http://target.com/FUZZ": "Inject lookup arrays into the custom 'FUZZ' parameter marker."})
            run_command(["ffuf", "-h"])
        elif choice == "4":
            display_tool_info("Gobuster", "Parallelized brute-force scanner tracking hidden routes and virtual hosts.", {"gobuster dir -u http://target.com/ -w list.txt": "Discover active paths utilizing concurrency routing rules."})
            run_command(["gobuster", "--help"])
        elif choice == "5":
            display_tool_info("Recon-ng", "A command-line web intelligence gathering framework modeled around modular tables.", {"recon-ng": "Launches the modular console workstation profile."})
            run_command(["recon-ng", "-h"])
        elif choice == "6":
            display_tool_info("Wfuzz", "Comprehensive parameter, variable, payload, and content delivery fuzzer.", {"wfuzz -c -z file,dict.txt --hc 404 http://target.com/FUZZ": "Fuzz route arrays while filtering out 404 page responses."})
            run_command(["wfuzz", "--help"])
        elif choice == "0":
            break

def web_vuln_menu():
    while True:
        clear_screen()
        header()
        print(f"{MAGENTA}{BOLD}--- WEB APPLICATION VULNERABILITY AUDITING ---{RESET}\n")
        print(f"  {GREEN}1.{RESET} BurpSuite     {GREEN}2.{RESET} Davtest")
        print(f"  {GREEN}3.{RESET} Skipfish      {GREEN}4.{RESET} Wapiti")
        print(f"  {GREEN}5.{RESET} WhatWeb       {GREEN}6.{RESET} WPScan")
        print(f"  {RED}0. Return to Main Core{RESET}\n")
        
        choice = input(f"{BOLD}Select Engine: {RESET}").strip()
        if choice == "1":
            display_tool_info("BurpSuite", "The gold-standard proxy tool used to catch, modify, and replay active web requests.", {"burpsuite": "Triggers the central utility control layout."})
            run_command(["burpsuite", "--help"])
        elif choice == "2":
            display_tool_info("Davtest", "Verifies authorization security configuration across WebDAV servers via remote execution tests.", {"davtest -url http://target.com/dav/": "Attempt multi-format validation script injection."})
            run_command(["davtest"])
        elif choice == "3":
            display_tool_info("Skipfish", "Fully autonomous, speed-optimized path mapping security auditor.", {"skipfish -o /tmp/log http://target.com/": "Generate descriptive vulnerability evaluation charts inside local paths."})
            run_command(["skipfish", "-h"])
        elif choice == "4":
            display_tool_info("Wapiti", "Black-box security testing utility targeting inputs, parameter leaks, and dangerous backend scripts.", {"wapiti -u http://target.com/": "Initiate automated audit loops against web input frameworks."})
            run_command(["wapiti", "-h"])
        elif choice == "5":
            display_tool_info("WhatWeb", "Fingerprints web application infrastructure configurations, plugin versions, and backend frameworks.", {"whatweb http://target.com/": "Extract component metadata signatures and version profiles."})
            run_command(["whatweb", "--help"])
        elif choice == "6":
            display_tool_info("WPScan", "Specialized security scanner tailored to map vulnerabilities within WordPress instances.", {"wpscan --url http://target.com/blog --enumerate p": "Identify active software extensions containing structural code exploits."})
            run_command(["wpscan", "--help"])
        elif choice == "0":
            break

def wireless_menu():
    while True:
        clear_screen()
        header()
        print(f"{MAGENTA}{BOLD}--- WIRELESS & BLUETOOTH PHYSICAL LAYERS ---{RESET}\n")
        print(f"  {GREEN}1.{RESET} Spooftooph (Bluetooth Emulation/Spoofing Tool)")
        print(f"  {GREEN}2.{RESET} Aircrack-ng Core Suite (WiFi Inspection)")
        print(f"  {GREEN}3.{RESET} Wifite & Reaver (Automated Radio Audits)")
        print(f"  {RED}0. Return to Main Core{RESET}\n")
        
        choice = input(f"{BOLD}Select Engine: {RESET}").strip()
        if choice == "1":
            display_tool_info("Spooftooph", "Automates modification and emulation of local Bluetooth radio flags (Name, MAC, Class).", {"spooftooph -i hci0 -n SpoofName": "Modify host Bluetooth radio broadcast identifier tags dynamically via hci0 interface."})
            run_command(["spooftooph", "-h"])
        elif choice == "2":
            display_tool_info("Aircrack-ng Suite", "A comprehensive suite of wireless configuration verification utilities analyzing local data stream flows.", {"airmon-ng start wlan0": "Switch hardware adapter processing mode over to monitor status parameters."})
            run_command(["aircrack-ng", "--help"])
        elif choice == "3":
            display_tool_info("Wifite Framework", "Automates standard script processes to verify the defense strengths of surrounding networks.", {"wifite": "Begin wireless hardware processing routines."})
            run_command(["wifite", "-h"])
        elif choice == "0":
            break

def phishing_menu():
    display_tool_info("ZPhisher Module (Social Engineering Simulator)", 
        "An open source wizard interface used exclusively to show users how modern phishing operations compromise credentials.",
        {"bash zphisher.sh": "Initializes the step-by-step phishing template engine."})
    if os.path.exists("/opt/zphisher/zphisher.sh"):
        os.chdir("/opt/zphisher")
        run_command(["bash", "zphisher.sh"])
        os.chdir("/opt/gods_eye")
    else:
        print(f"{RED}[!] Error: Integrated simulator files are unavailable inside the current working path.{RESET}")
        time.sleep(2)

if __name__ == "__main__":
    main_menu()
