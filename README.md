# God's Eye — OSINT Suite

```
        ◈  ◈  ◈   G O D ' S   E Y E   ◈  ◈  ◈
  ════════════════════════════════════════════════════
            ⚡  O S I N T   S U I T E   ⚡
                   Developed by: VAISHNAV RAJEEV
                   contribution: RISHABH GURNANI
  ════════════════════════════════════════════════════
```

A unified command-line launcher that consolidates industry-standard
reconnaissance, DNS analysis, web scanning, wireless auditing, and
anonymity tools into a single interactive menu — designed for ethical
hackers, security researchers, and defenders.

---

## Features

| Module | Tools |
|---|---|
| Host OSINT | Amass, Nmap, theHarvester |
| DNS Recon | dnsenum, dnsrecon |
| Web Scan | dirb, gobuster, ffuf |
| Web Vulnerability | Wapiti, WPScan |
| Wireless Audit | Aircrack-ng, Wifite |
| Anonymity | MAC changer, IP changer, network rollback |
| Integrations | Aegis Gateway, OSINT Framework, Shannon AI (LLM) |

---

## Requirements

- **OS:** Kali Linux / Parrot OS / any Debian-based distro
- **Python:** 3.8+
- **Privileges:** `sudo` access (required for MAC/IP changer, wireless tools)
- **Optional:** `gnome-terminal`, `xfce4-terminal`, or `xterm` (for sub-shell spawning)

No Python dependencies outside the standard library.

---

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/gods-eye.git
cd gods-eye
chmod +x godseye.py
python3 godseye.py
```

Tools that are not installed are detected automatically. The suite will
prompt you to install any missing tool via `apt` before launching it.

---

## Usage

```
  Vector: 1    →  Host OSINT sub-menu
  Vector: 2    →  DNS Recon sub-menu
  Vector: 3    →  Web Scan sub-menu
  Vector: 4    →  Web Vulnerability sub-menu
  Vector: 5    →  Wireless Audit sub-menu
  Vector: 6    →  MAC Changer
  Vector: 7    →  IP Changer (MAC randomise + DHCP release/renew)
  Vector: 8    →  GOD'S FIX (restore original MAC, verify connectivity)
  Vector: 9    →  Integrations (Aegis, OSINT Framework, Shannon AI)
  Vector: 10   →  About / Authors
  Vector: 0    →  Exit
```

Each tool opens in its own terminal window as an interactive session,
so you can run commands directly without leaving the launcher.

---

## Architecture

```
godseye.py
│
├── TOOL_MAP            — display name → (binary, apt package) mapping
├── launch_tool()       — install check + new-terminal spawn
├── open_in_terminal()  — best-available terminal detection
│
├── host_menu()
├── network_menu()
├── web_scan_menu()
├── web_vuln_menu()
├── wireless_menu()
│
├── mac_changer()       — macchanger -r
├── ip_changer()        — MAC randomise + NetworkManager restart
├── gods_fix()          — restore permanent MAC, ping test (threaded)
│
├── integrations_menu() — browser/clone launchers
└── about()             — credits and legal notice
```

---

## Legal Notice

> God's Eye is built for **authorised security testing and research only**.
> Scanning, probing, or accessing systems without explicit written permission
> from the owner is illegal in most jurisdictions.
> The authors accept no liability for misuse of this software.
> Always verify you have authorisation before running any tool.

---

## Authors

| Role | Name |
|---|---|
| Lead Architect | Vaishnav Rajeev (B.Tech Cyber Security) |
| Core Contributor | Rishabh Gurnani  (B.Tech Cyber Security) |
| Core Contributor | Puneeth Sai  (B.Tech Cyber Security)  |

Contact: vaishnav.cvv240888@cvv.ac.in

---

## Licence

MIT — see `LICENSE` for details.
