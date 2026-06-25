#!/bin/bash
# ============================================================
#   GOD'S EYE — OSINT Suite
#   Developed by: Vaishnav Rajeev
#   Contributors: Rishabh Gurnani
# ============================================================
#   Auto-installer for all system tools and runtime deps.
#
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
echo "        ◈  ◈  ◈   G O D ' S   E Y E   ◈  ◈  ◈"
echo -e "${CYAN}  ════════════════════════════════════════════════════"
echo "        ⚡  O S I N T   S U I T E  —  S E T U P  ⚡"
echo -e "               Developed by: ${RED}VAISHNAV${CYAN}"
echo -e "  ════════════════════════════════════════════════════${RESET}"
echo ""

# ── Counters ─────────────────────────────────────────────────
INSTALLED=0
SKIPPED=0
FAILED=0
FAILED_LIST=()

# ── Helper: check binary OR dpkg, then install ───────────────
install_pkg() {
    local apt_pkg="$1"
    local binary="$2"
    local label="${3:-$apt_pkg}"

    if command -v "$binary" &>/dev/null || dpkg -s "$apt_pkg" &>/dev/null 2>&1; then
        echo -e "  ${CYAN}[~]${RESET} ${label} — already installed, skipping."
        ((SKIPPED++))
        return
    fi

    echo -e "  ${YELLOW}[*]${RESET} Installing ${BOLD}${label}${RESET}..."
    if apt-get install -y "$apt_pkg" &>/dev/null 2>&1; then
        echo -e "  ${GREEN}[✓]${RESET} ${label} — OK."
        ((INSTALLED++))
    else
        echo -e "  ${RED}[✗]${RESET} ${label} — FAILED. Try: sudo apt-get install ${apt_pkg}"
        ((FAILED++))
        FAILED_LIST+=("$apt_pkg")
    fi
}

# ── Helper: zenmap has no apt package on modern Kali ─────────
install_zenmap() {
    if command -v zenmap &>/dev/null || command -v nmapsi4 &>/dev/null; then
        echo -e "  ${CYAN}[~]${RESET} zenmap / nmapsi4 — already installed, skipping."
        ((SKIPPED++))
        return
    fi
    echo -e "  ${YELLOW}[*]${RESET} Installing ${BOLD}zenmap${RESET} (trying nmapsi4 fallback)..."
    if apt-get install -y zenmap &>/dev/null 2>&1; then
        echo -e "  ${GREEN}[✓]${RESET} zenmap — OK."
        ((INSTALLED++))
    elif apt-get install -y nmapsi4 &>/dev/null 2>&1; then
        echo -e "  ${GREEN}[✓]${RESET} zenmap (via nmapsi4) — OK."
        ((INSTALLED++))
    else
        echo -e "  ${YELLOW}[~]${RESET} zenmap — not available in apt. Skipping (nmap CLI still works)."
        ((SKIPPED++))
    fi
}

# ════════════════════════════════════════════════════════════
# SECTION 1 — CORE RUNTIME DEPENDENCIES
# ════════════════════════════════════════════════════════════
echo -e "${CYAN}${BOLD}  ── CORE RUNTIME ────────────────────────────────────${RESET}"
install_pkg "python3"          "python3"          "Python 3"
install_pkg "git"              "git"              "git"
install_pkg "iproute2"         "ip"               "iproute2 (ip)"
install_pkg "iputils-ping"     "ping"             "iputils-ping"
install_pkg "network-manager"  "nmcli"            "NetworkManager"
install_pkg "macchanger"       "macchanger"       "macchanger"
install_pkg "xdg-utils"        "xdg-open"         "xdg-utils"
install_pkg "bash"             "bash"             "bash"
install_pkg "sudo"             "sudo"             "sudo"
echo ""

# ════════════════════════════════════════════════════════════
# SECTION 2 — TERMINAL EMULATORS
# ════════════════════════════════════════════════════════════
echo -e "${CYAN}${BOLD}  ── TERMINAL EMULATORS ──────────────────────────────${RESET}"
install_pkg "xterm"            "xterm"            "xterm (fallback — mandatory)"
install_pkg "xfce4-terminal"   "xfce4-terminal"   "xfce4-terminal (recommended)"
echo ""

# ════════════════════════════════════════════════════════════
# SECTION 3 — HOST OSINT
echo -e "${CYAN}${BOLD}  ── HOST OSINT ───────────────────────────────────────${RESET}"
install_pkg "amass"            "amass"            "amass"
install_pkg "nmap"             "nmap"             "nmap"
install_pkg "theharvester"     "theHarvester"     "theHarvester"
install_pkg "dmitry"           "dmitry"           "dmitry"
install_pkg "spiderfoot"       "spiderfoot"       "spiderfoot"
install_pkg "unicornscan"      "unicornscan"      "unicornscan"
install_pkg "legion"           "legion"           "legion"
install_zenmap
echo ""

# ════════════════════════════════════════════════════════════
# SECTION 4 — DNS RECON
echo -e "${CYAN}${BOLD}  ── DNS RECON ────────────────────────────────────────${RESET}"
install_pkg "dnsenum"          "dnsenum"          "dnsenum"
install_pkg "dnsrecon"         "dnsrecon"         "dnsrecon"
install_pkg "dnsmap"           "dnsmap"           "dnsmap"
echo ""

# ════════════════════════════════════════════════════════════
# SECTION 5 — WEB SCAN
echo -e "${CYAN}${BOLD}  ── WEB SCAN ─────────────────────────────────────────${RESET}"
install_pkg "dirb"             "dirb"             "dirb"
install_pkg "gobuster"         "gobuster"         "gobuster"
install_pkg "ffuf"             "ffuf"             "ffuf"
install_pkg "dirbuster"        "dirbuster"        "dirbuster"
install_pkg "recon-ng"         "recon-ng"         "recon-ng"
install_pkg "wfuzz"            "wfuzz"            "wfuzz"
echo ""

# ════════════════════════════════════════════════════════════
# SECTION 6 — WEB VULNERABILITY
echo -e "${CYAN}${BOLD}  ── WEB VULNERABILITY ───────────────────────────────${RESET}"
install_pkg "wapiti"           "wapiti3"          "wapiti (wapiti3)"
install_pkg "wpscan"           "wpscan"           "wpscan"
install_pkg "burpsuite"        "burpsuite"        "burpsuite"
install_pkg "davtest"          "davtest"          "davtest"
install_pkg "skipfish"         "skipfish"         "skipfish"
install_pkg "whatweb"          "whatweb"          "whatweb"
echo ""

# ════════════════════════════════════════════════════════════
# SECTION 7 — WIRELESS & BLUETOOTH
echo -e "${CYAN}${BOLD}  ── WIRELESS & BLUETOOTH ────────────────────────────${RESET}"
install_pkg "aircrack-ng"      "aircrack-ng"      "aircrack-ng"
install_pkg "wifite"           "wifite"           "wifite"
install_pkg "spooftooph"       "spooftooph"       "spooftooph"
echo ""

# ════════════════════════════════════════════════════════════
# SECTION 8 — FINALISE
echo -e "${CYAN}${BOLD}  ── FINALISING ──────────────────────────────────────${RESET}"

SCRIPT_DIR="$(cd)"
