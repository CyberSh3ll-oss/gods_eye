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

# ── Update apt ───────────────────────────────────────────────
echo -e "${YELLOW}  [*] Updating apt package lists...${RESET}"
apt-get update -y &>/dev/null
echo -e "${GREEN}  [✓] apt updated.${RESET}\n"

# ════════════════════════════════════════════════════════════
# SECTION 1 — CORE RUNTIME DEPENDENCIES
# Called directly by godseye.py at runtime — mandatory.
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
# godseye.py probes: gnome-terminal > xfce4-terminal > konsole > xterm
# xterm is the universal fallback — always installed.
# ════════════════════════════════════════════════════════════
echo -e "${CYAN}${BOLD}  ── TERMINAL EMULATORS ──────────────────────────────${RESET}"
install_pkg "xterm"            "xterm"            "xterm (fallback — mandatory)"
install_pkg "xfce4-terminal"   "xfce4-terminal"   "xfce4-terminal (recommended)"
echo ""

# ════════════════════════════════════════════════════════════
# SECTION 3 — HOST OSINT
# Active in godseye.py menus: amass, nmap, theHarvester
# Extended (future modules): dmitry, spiderfoot, unicornscan, legion, zenmap
# ════════════════════════════════════════════════════════════
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
# Active: dnsenum, dnsrecon
# Extended: dnsmap
# ════════════════════════════════════════════════════════════
echo -e "${CYAN}${BOLD}  ── DNS RECON ────────────────────────────────────────${RESET}"
install_pkg "dnsenum"          "dnsenum"          "dnsenum"
install_pkg "dnsrecon"         "dnsrecon"         "dnsrecon"
install_pkg "dnsmap"           "dnsmap"           "dnsmap"
echo ""

# ════════════════════════════════════════════════════════════
# SECTION 5 — WEB SCAN
# Active: dirb, gobuster, ffuf
# Extended: dirbuster, recon-ng, wfuzz
# ════════════════════════════════════════════════════════════
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
# Active: wapiti (binary: wapiti3), wpscan
# Extended: burpsuite, davtest, skipfish, whatweb
# ════════════════════════════════════════════════════════════
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
# Active: aircrack-ng, wifite
# Extended: spooftooph
# ════════════════════════════════════════════════════════════
echo -e "${CYAN}${BOLD}  ── WIRELESS & BLUETOOTH ────────────────────────────${RESET}"
install_pkg "aircrack-ng"      "aircrack-ng"      "aircrack-ng"
install_pkg "wifite"           "wifite"           "wifite"
install_pkg "spooftooph"       "spooftooph"       "spooftooph"
echo ""

# ════════════════════════════════════════════════════════════
# SECTION 8 — FINALISE
# ════════════════════════════════════════════════════════════
echo -e "${CYAN}${BOLD}  ── FINALISING ──────────────────────────────────────${RESET}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$SCRIPT_DIR/godseye.py" ]; then
    chmod +x "$SCRIPT_DIR/godseye.py"
    echo -e "  ${GREEN}[✓]${RESET} godseye.py — marked executable."
else
    echo -e "  ${YELLOW}[~]${RESET} godseye.py not found in ${SCRIPT_DIR} — run setup from the repo root."
fi

if [ -f "$SCRIPT_DIR/setup.sh" ]; then
    chmod +x "$SCRIPT_DIR/setup.sh"
    echo -e "  ${GREEN}[✓]${RESET} setup.sh — marked executable."
fi
echo ""

# ════════════════════════════════════════════════════════════
# SECTION 9 — SUMMARY
# ════════════════════════════════════════════════════════════
echo -e "${CYAN}  ════════════════════════════════════════════════════"
echo -e "${BOLD}  SETUP COMPLETE — SUMMARY${RESET}"
echo -e "${CYAN}  ════════════════════════════════════════════════════${RESET}"
echo -e "  ${GREEN}[✓] Installed  : ${INSTALLED}${RESET}"
echo -e "  ${CYAN}[~] Skipped    : ${SKIPPED} (already present)${RESET}"

if [ "${FAILED}" -gt 0 ]; then
    echo -e "  ${RED}[✗] Failed     : ${FAILED}${RESET}"
    echo -e "  ${RED}      Packages that need manual attention:${RESET}"
    for pkg in "${FAILED_LIST[@]}"; do
        echo -e "  ${RED}        • ${pkg}${RESET}"
    done
    echo ""
    echo -e "  ${YELLOW}  Tip: Some tools may require a third-party repo."
    echo -e "       Check the project README for manual install notes.${RESET}"
else
    echo -e "  ${GREEN}[✗] Failed     : 0 — all clean.${RESET}"
fi

echo ""
echo -e "  ${GREEN}${BOLD}Launch the framework:${RESET}"
echo -e "  ${YELLOW}    python3 godseye.py${RESET}"
echo ""
echo -e "  ${CYAN}  All tools must be used only on systems you own"
echo -e "  or have explicit written authorisation to test.${RESET}"
echo ""
