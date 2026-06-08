# 👁️ GOD'S EYE — OSINT Suite
**Developed by: VAISHNAV**

> A terminal-based OSINT framework for Kali Linux. Launches every tool in its own persistent terminal window with live help output and usage examples — so your control hub never gets cluttered.

---

## ⚡ Features

- Branded terminal UI with ANSI colors
- Every CLI tool opens in a **new qterminal window** with:
  - Live `--help` output from your system
  - Curated usage examples
  - Persistent bash prompt (window never auto-closes)
- GUI tools launch silently in the background
- Auto-detects if a tool is missing and **offers to install it**
- Works with qterminal, gnome-terminal, xfce4-terminal, xterm

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/godseye.git
cd godseye

# 2. Run the installer (installs all tools)
chmod +x setup.sh
sudo ./setup.sh

# 3. Launch the framework
python3 godseye.py
```

---

## 🗂️ Tool Categories

| Category | Tools |
|---|---|
| Host & General OSINT | Amass, Dmitry, Nmap, Spiderfoot, theHarvester, Unicornscan, Legion, Zenmap |
| Network & DNS | Dnsenum, Dnsmap, Dnsrecon |
| Web Fingerprinting | Dirb, Dirbuster, Ffuf, Gobuster, Recon-ng, Wfuzz |
| Web Vulnerability | BurpSuite, Davtest, Skipfish, Wapiti, WhatWeb, WPScan |
| Wireless & Bluetooth | Spooftooph, Aircrack-ng, Wifite |
| Social Engineering | Zphisher |

---

## 📋 Requirements

- **OS:** Kali Linux
- **Python:** 3.6+ (standard library only — no pip install needed)
- **Terminal:** qterminal (default on Kali), or any of: gnome-terminal, xfce4-terminal, xterm

All system tools are installed automatically by `setup.sh`.

---

## ⚠️ Disclaimer

This tool is intended for **authorized penetration testing and educational purposes only**.
Use only on systems you have explicit permission to test.
The developer is not responsible for any misuse.
