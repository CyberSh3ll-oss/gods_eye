# God's Eye — OSINT & Exploitation Suite

        * * * G O D ' S   E Y E   * * *
  ========================================================
                     OSINT SUITE
       c        Developed by: VAISHNAV
  ========================================================

A unified command-line framework that consolidates industry-standard reconnaissance, exploitation, lateral movement, hardware hacking, and network anonymity tools into a single interactive menu — built for ethical hackers, security researchers, and defenders.

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

* **Single interactive menu** — no memorising commands.
* **Auto-installation** — detects whether each tool is installed and offers to install it via `apt` on the spot.
* **Built-in knowledge base** — selecting a tool clears the screen and shows:
  * Plain-English explanation of what the tool does.
  * Real example commands ready to copy.
  * Live help output from the tool itself.
* **Full Attack Lifecycle Support** — expanded from pure OSINT to include exploitation, post-exploitation, phishing, and IoT hardware hacking.
* **Network anonymity utilities** — MAC changer, IP changer, network rollback (GOD'S FIX).
* **Audio Surveillance** — custom IoT Audio Hijack Proof of Concept (PoC) for ADB-based microphone capture.
* **Integrated integrations** — browser launcher for Aegis Cyber Gateway, OSINT Framework, and Shannon AI (LLM).
* **Robust session handling** — clean exit on `Ctrl+C` at any point.

---

## Menu Structure

```text
  [ Reconnaissance ]
  [1] Host OSINT        [2] DNS Recon
  [3] Web Scan          [4] Web Vuln
  [5] Wireless Audit

  [ Exploitation / Post-Exploit ]
  [6] Exploitation      [7] Post-Exploit & Pivot
  [8] Phishing / Social Eng

  [ IoT / Audio ]
  [9] IoT & Hardware    [10] Audio Surveillance

  [ Anonymity ]
  [11] MAC Changer      [12] IP Changer
  [13] GOD'S FIX

  [ Integrations ]
  [14] External Tools & Integrations

  [ Info ]
  [15] About / Authors
  [0]  Exit
