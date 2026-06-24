# God's Eye — OSINT Suite

```
        *  *  *   G O D ' S   E Y E   *  *  *
  ========================================================
              OSINT SUITE
         Developed by: VAISHNAV
  ========================================================
```

A unified command-line framework that consolidates industry-standard
reconnaissance, DNS analysis, web scanning, wireless auditing, and
network anonymity tools into a single interactive menu — built for
ethical hackers, security researchers, and defenders.

---

## Table of Contents

- [Features](#features)
- [Menu Structure](#menu-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Tool Reference](#tool-reference)
- [Integrations](#integrations)
- [Repository Structure](#repository-structure)
- [Authors](#authors)
- [Legal Notice](#legal-notice)
- [Licence](#licence)

---

## Features

- Single interactive menu — no memorising commands
- Auto-detects whether each tool is installed; offers to install it on the spot
- Selecting any reconnaissance tool clears the screen and shows:
  - Plain-English explanation of what the tool does
  - Real example commands ready to copy
  - Live help output from the tool itself
- Network anonymity utilities (MAC changer, IP changer, network rollback)
- Integrated browser launcher and Shannon AI LLM integration
- Internet connectivity check on every launch
- Clean exit on Ctrl+C at any point

---

## Menu Structure

```
  [ Reconnaissance ]
  [1] Host OSINT        [2] DNS Recon
  [3] Web Scan          [4] Web Vuln
  [5] Wireless Audit

  [ Anonymity ]
  [6] MAC Changer       [7] IP Changer
  [8] GOD'S FIX

  [ Integrations ]
  [9] External Tools & Integrations

  [ Info ]
  [10] About / Authors
  [0]  Exit
```

### Sub-menus

**[1] Host OSINT**
```
  [1] amass         →  Subdomain enumeration
  [2] nmap          →  Port / service scanning
  [3] theHarvester  →  Email & host harvesting
```

**[2] DNS Recon**
```
  [1] dnsenum   →  DNS record enumeration
  [2] dnsrecon  →  DNS zone & record recon
```

**[3] Web Scan**
```
  [1] dirb      →  Directory brute-force (wordlist)
  [2] gobuster  →  Directory / DNS brute-force
  [3] ffuf      →  Fast web fuzzer
```

**[4] Web Vuln**
```
  [1] wapiti  →  Web application vulnerability scanner
  [2] wpscan  →  WordPress security scanner
```

**[5] Wireless Audit**
```
  [1] aircrack-ng  →  WPA/WEP handshake analysis
  [2] wifite       →  Automated wireless auditing
```

**[9] Integrations**
```
  [1] Aegis Cyber Gateway  →  Opens aegiscybercomms.netlify.app
  [2] OSINT Framework      →  Opens osintframework.com
  [3] Shannon AI (LLM)     →  Clones and runs Keygraph Shannon
```

---

## Requirements

- **OS:** Kali Linux / Parrot OS / any Debian-based distro
- **Python:** 3.6+ (no pip packages — standard library only)
- **Privileges:** `sudo` access for installation and anonymity tools
- **Terminal:** qterminal, xfce4-terminal, gnome-terminal, or xterm

God's Eye uses **zero third-party Python packages**. Do not run
`pip install -r requirements.txt`. The requirements file is
documentation only.

---

## Installation

**Clone the repository:**
```bash
git clone https://github.com/CyberSh3ll-oss/gods_eye.git
cd gods_eye
```

**Run the auto-installer** (installs all system tools via apt):
```bash
chmod +x setup.sh
sudo ./setup.sh
```

The installer will:
- Update apt package lists
- Install all core runtime dependencies
- Install all active tool modules
- Install extended tools for future modules
- Mark `godseye.py` executable

**If you only want the active tools** (smaller install):
```bash
sudo apt-get install -y amass nmap theharvester dnsenum dnsrecon \
  dirb gobuster ffuf wapiti wpscan aircrack-ng wifite
```

---

## Usage

```bash
python3 godseye.py
```

**How tool selection works:**

1. From the main menu, enter a number (e.g. `3` for Web Scan)
2. From the sub-menu, enter a number (e.g. `2` for gobuster)
3. The screen clears and shows:
   - What the tool does in plain English
   - Three real example commands
   - Live help output from the tool
4. Press **ENTER** to return to the sub-menu
5. Enter `0` at any sub-menu to go back to the main menu
6. Enter `0` at the main menu to exit

**Anonymity tools:**

| Vector | Function | What it does |
|--------|----------|--------------|
| `6` | MAC Changer | Randomises the MAC address of a chosen interface |
| `7` | IP Changer | Cycles MAC + requests a new DHCP lease |
| `8` | GOD'S FIX | Restores original MAC and tests connectivity |

---

## Tool Reference

### Active Tools (wired into menus)

| Tool | Category | Purpose |
|------|----------|---------|
| amass | Host OSINT | Subdomain enumeration and DNS asset mapping |
| nmap | Host OSINT | Port scanning and service detection |
| theHarvester | Host OSINT | Email, host and subdomain harvesting from public sources |
| dnsenum | DNS Recon | DNS record enumeration and zone transfer attempts |
| dnsrecon | DNS Recon | Deep DNS reconnaissance and reverse lookups |
| dirb | Web Scan | Directory brute-force using wordlists |
| gobuster | Web Scan | Fast directory, DNS and vhost brute-forcer |
| ffuf | Web Scan | High-speed web fuzzer with FUZZ keyword injection |
| wapiti | Web Vuln | Web application vulnerability scanner (SQLi, XSS, etc.) |
| wpscan | Web Vuln | WordPress plugin, theme and user enumeration |
| aircrack-ng | Wireless | WPA/WEP handshake analysis and cracking suite |
| wifite | Wireless | Automated wireless network auditing |

### Extended Tools (installed by setup.sh, available for future modules)

| Tool | Category | Purpose |
|------|----------|---------|
| dmitry | Host OSINT | Deepmagic information gathering |
| spiderfoot | Host OSINT | Automated OSINT framework |
| unicornscan | Host OSINT | Async port and service scanner |
| legion | Host OSINT | GUI network pentest framework |
| nmapsi4 | Host OSINT | Zenmap GUI replacement |
| dnsmap | DNS Recon | DNS domain brute-force mapping |
| dirbuster | Web Scan | Java-based directory brute-forcer |
| recon-ng | Web Scan | Web reconnaissance framework |
| wfuzz | Web Scan | Web content fuzzer |
| burpsuite | Web Vuln | Web app security testing suite |
| davtest | Web Vuln | WebDAV vulnerability tester |
| skipfish | Web Vuln | Active web app security recon |
| whatweb | Web Vuln | Web tech fingerprinting |
| spooftooph | Wireless | Bluetooth device spoofing |

---

## Integrations

All three integrations require an active internet connection.

**Aegis Cyber Gateway**
Opens `https://aegiscybercomms.netlify.app/` in the default browser.
The Aegis cybersecurity consulting portfolio and service platform.

**OSINT Framework**
Opens `https://osintframework.com/` in the default browser.
A categorised directory of free OSINT tools and resources.

**Shannon AI (LLM)**
Clones `https://github.com/KeygraphHQ/shannon.git` into `/tmp/shannon`
and launches the LLM in a new terminal session. Requires `git`.

---

## Repository Structure

```
gods_eye/
├── godseye.py        ← main launcher (run this)
├── setup.sh          ← one-command apt installer
├── requirements.txt  ← dependency documentation (not for pip)
├── README.md         ← this file
└── LICENSE           ← MIT licence
```

---

## Authors

| Role | Name | Specialisation |
|------|------|---------------|
| Architect | Vaishnav Rajeev | OSINT, digital forensics, network analysis, scripting & automation |
| Core Contributor | Rishabh Gurnani | Governance, risk & compliance (GRC), identity & MFA |

**Contact:** vaishnav.cvv240888@cvv.ac.in

---

## Legal Notice

> God's Eye is built for **authorised security testing and research only**.
>
> Scanning, probing, or accessing systems without explicit written
> permission from the owner is illegal under the Computer Misuse Act,
> the CFAA, and equivalent legislation in most jurisdictions.
>
> The authors accept no liability for misuse of this software.
> Always verify you have written authorisation before running any tool.

---

## Licence

MIT — see [LICENSE](LICENSE) for full terms.

Copyright © 2025 Vaishnav Rajeev
