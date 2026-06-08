#!/bin/bash
# ============================================================
#   GOD'S EYE — OSINT Suite
#   Developed by: VAISHNAV
#   Auto-installer for all required system tools
# ============================================================
#   Usage:
#     chmod +x setup.sh
#     sudo ./setup.sh
# ============================================================

# ── ANSI Colors ──────────────────────────────────────────────
RED='\033[1;31m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
RESET='\033[0m'

# ── Root check ───────────────────────────────────────────────
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[!] Please run as root: sudo ./setup.sh${RESET}"
    exit 1
fi

# ── Header ───────────────────────────────────────────────────
clear
echo -e "${RED}${BOLD}"
echo "      👁️  👁️  👁️   G O D ' S   E Y E   👁️  👁️  👁️"
echo -e "${CYAN}  ========================================================"
echo "        ⚡  O S I N T   S U I T E  —  S E T U P  ⚡"
echo -e "               Developed by: ${RED}VAISHNAV${CYAN}"
echo -e "  ========================================================${RESET}"
echo ""

# ── Counters ─────────────────────────────────────────────────
INSTALLED=0
SKIPPED=0
FAILED=0
FAILED_LIST=()

# ── Helper: install one apt package ──────────────────────────
install_pkg() {
    local pkg=$1
    local label=$2

    # Check if already installed (by binary or dpkg)
    if command -v "$label" &>/dev/null || dpkg -s "$pkg" &>/dev/null 2>&1; then
        echo -e "  ${CYAN}[~]${RESET} ${label} — already installed, skipping."
        ((SKIPPED++))
        return
    fi

    echo -e "  ${YELLOW}[*]${RESET} Installing ${BOLD}${label}${RESET}..."
    if apt-get install -y "$pkg" &>/dev/null 2>&1; then
        echo -e "  ${GREEN}[✓]${RESET} ${label} — installed successfully."
        ((INSTALLED++))
    else
        echo -e "  ${RED}[✗]${RESET} ${label} — FAILED. Try manually: sudo apt-get install ${pkg}"
        ((FAILED++))
        FAILED_LIST+=("$pkg")
    fi
}

# ── Update apt ───────────────────────────────────────────────
echo -e "${YELLOW}  [*] Updating apt package lists...${RESET}"
apt-get update -y &>/dev/null
echo -e "${GREEN}  [✓] apt updated.${RESET}\n"

# ── Python check ─────────────────────────────────────────────
echo -e "${CYAN}${BOLD}  ── PYTHON ──────────────────────────────────────────${RESET}"
if command -v python3 &>/dev/null; then
    PY_VER=$(python3 --version 2>&1)
    echo -e "  ${GREEN}[✓]${RESET} ${PY_VER} — already installed."
    ((SKIPPED++))
else
    echo -e "  ${YELLOW}[*]${RESET} Installing python3..."
    apt-get install -y python3 &>/dev/null && echo -e "  ${GREEN}[✓]${RESET} python3 installed." && ((INSTALLED++))
fi
echo ""

# ── Terminal emulator check ───────────────────────────────────
echo -e "${CYAN}${BOLD}  ── TERMINAL EMULATOR ───────────────────────────────${RESET}"
install_pkg "qterminal"     "qterminal"
echo ""

# ── Host / General OSINT ─────────────────────────────────────
echo -e "${CYAN}${BOLD}  ── HOST & GENERAL OSINT ────────────────────────────${RESET}"
install_pkg "amass"         "amass"
install_pkg "dmitry"        "dmitry"
install_pkg "nmap"          "nmap"
install_pkg "spiderfoot"    "spiderfoot"
install_pkg "theharvester"  "theHarvester"
install_pkg "unicornscan"   "unicornscan"
install_pkg "legion"        "legion"

# Zenmap — try zenmap first, fall back to nmapsi4
echo -e "  ${YELLOW}[*]${RESET} Installing ${BOLD}zenmap${RESET}..."
if apt-get install -y zenmap &>/dev/null 2>&1; then
    echo -e "  ${GREEN}[✓]${RESET} zenmap — installed successfully."
    ((INSTALLED++))
elif apt-get install -y nmapsi4 &>/dev/null 2>&1; then
    echo -e "  ${GREEN}[✓]${RESET} zenmap (via nmapsi4) — installed successfully."
    ((INSTALLED++))
else
    echo -e "  ${YELLOW}[~]${RESET} zenmap — not available in apt. Skipping (Nmap CLI still works)."
    ((SKIPPED++))
fi
echo ""

# ── Network / DNS ────────────────────────────────────────────
echo -e "${CYAN}${BOLD}  ── NETWORK & DNS ───────────────────────────────────${RESET}"
install_pkg "dnsenum"       "dnsenum"
install_pkg "dnsmap"        "dnsmap"
install_pkg "dnsrecon"      "dnsrecon"
echo ""

# ── Web Fingerprinting ───────────────────────────────────────
echo -e "${CYAN}${BOLD}  ── WEB FINGERPRINTING & DISCOVERY ─────────────────${RESET}"
install_pkg "dirb"          "dirb"
install_pkg "dirbuster"     "dirbuster"
install_pkg "ffuf"          "ffuf"
install_pkg "gobuster"      "gobuster"
install_pkg "recon-ng"      "recon-ng"
install_pkg "wfuzz"         "wfuzz"
echo ""

# ── Web Vulnerability ────────────────────────────────────────
echo -e "${CYAN}${BOLD}  ── WEB VULNERABILITY AUDITING ──────────────────────${RESET}"
install_pkg "burpsuite"     "burpsuite"
install_pkg "davtest"       "davtest"
install_pkg "skipfish"      "skipfish"
install_pkg "wapiti"        "wapiti"
install_pkg "whatweb"       "whatweb"
install_pkg "wpscan"        "wpscan"
echo ""

# ── Wireless / Bluetooth ─────────────────────────────────────
echo -e "${CYAN}${BOLD}  ── WIRELESS & BLUETOOTH ────────────────────────────${RESET}"
install_pkg "spooftooph"    "spooftooph"
install_pkg "aircrack-ng"   "aircrack-ng"
install_pkg "wifite"        "wifite"
echo ""

# ── Social Engineering ───────────────────────────────────────
echo -e "${CYAN}${BOLD}  ── SOCIAL ENGINEERING ──────────────────────────────${RESET}"
# Zphisher is a git repo, not an apt package
ZPHISHER_DIR="/opt/zphisher"
if [ -d "$ZPHISHER_DIR" ]; then
    echo -e "  ${CYAN}[~]${RESET} zphisher — already installed at ${ZPHISHER_DIR}."
    ((SKIPPED++))
else
    echo -e "  ${YELLOW}[*]${RESET} Installing ${BOLD}zphisher${RESET} from GitHub..."
    if command -v git &>/dev/null; then
        if git clone https://github.com/htr-tech/zphisher.git "$ZPHISHER_DIR" &>/dev/null 2>&1; then
            chmod +x "$ZPHISHER_DIR/zphisher.sh"
            echo -e "  ${GREEN}[✓]${RESET} zphisher — cloned to ${ZPHISHER_DIR}."
            ((INSTALLED++))
        else
            echo -e "  ${RED}[✗]${RESET} zphisher — clone failed. Check your internet connection."
            ((FAILED++))
            FAILED_LIST+=("zphisher (git clone)")
        fi
    else
        install_pkg "git" "git"
        git clone https://github.com/htr-tech/zphisher.git "$ZPHISHER_DIR" &>/dev/null 2>&1
        chmod +x "$ZPHISHER_DIR/zphisher.sh" 2>/dev/null
        echo -e "  ${GREEN}[✓]${RESET} zphisher — cloned to ${ZPHISHER_DIR}."
        ((INSTALLED++))
    fi
fi
echo ""

# ── Make godseye.py executable ───────────────────────────────
echo -e "${CYAN}${BOLD}  ── FINALISING ──────────────────────────────────────${RESET}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/godseye.py" ]; then
    chmod +x "$SCRIPT_DIR/godseye.py"
    echo -e "  ${GREEN}[✓]${RESET} godseye.py — marked executable."
else
    echo -e "  ${YELLOW}[~]${RESET} godseye.py not found in ${SCRIPT_DIR} — skipping chmod."
fi
echo ""

# ── Summary ──────────────────────────────────────────────────
echo -e "${CYAN}  ========================================================"
echo -e "${BOLD}  SETUP COMPLETE — SUMMARY${RESET}"
echo -e "${CYAN}  ========================================================${RESET}"
echo -e "  ${GREEN}[✓] Installed  : ${INSTALLED}${RESET}"
echo -e "  ${CYAN}[~] Skipped    : ${SKIPPED} (already present)${RESET}"
if [ $FAILED -gt 0 ]; then
    echo -e "  ${RED}[✗] Failed     : ${FAILED}${RESET}"
    echo -e "  ${RED}      Failed packages:${RESET}"
    for pkg in "${FAILED_LIST[@]}"; do
        echo -e "  ${RED}        • ${pkg}${RESET}"
    done
else
    echo -e "  ${RED}[✗] Failed     : 0${RESET}"
fi
echo ""
echo -e "  ${GREEN}${BOLD}Run the framework:${RESET}"
echo -e "  ${YELLOW}    python3 godseye.py${RESET}"
echo ""
