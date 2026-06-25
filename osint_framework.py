#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                          O S I N T   F R A M E W O R K                       ║
║                                                                              ║
║  LEGEND                                                                      ║
║   (T) Tool must be installed locally                                         ║
║   (D) Google Dork                                                            ║
║   (R) Requires registration                                                  ║
║   (M) Manual URL editing required                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

Usage:
    python3 osint_framework.py              → interactive menu
    python3 osint_framework.py --query "domain names"
    python3 osint_framework.py --export json
    python3 osint_framework.py --export csv
    python3 osint_framework.py --list-categories
"""

import os
import sys
import json
import csv
import textwrap
import argparse
import webbrowser

# ─────────────────────────────────────────────────────────────────────────────
# COLOUR HELPERS  (gracefully degrade on Windows without colour support)
# ─────────────────────────────────────────────────────────────────────────────
def _c(code: str, text: str) -> str:
    """Wrap text in an ANSI escape code if stdout is a tty."""
    if sys.stdout.isatty():
        return f"\033[{code}m{text}\033[0m"
    return text

RED    = lambda t: _c("31;1", t)
GREEN  = lambda t: _c("32;1", t)
YELLOW = lambda t: _c("33;1", t)
CYAN   = lambda t: _c("36;1", t)
BLUE   = lambda t: _c("34;1", t)
BOLD   = lambda t: _c("1",    t)
DIM    = lambda t: _c("2",    t)
MAGENTA = lambda t: _c("35;1", t)

# ─────────────────────────────────────────────────────────────────────────────
# THE FRAMEWORK DATA
# Each category is a dict:
#   { "desc": str, "subcategories": {...} | None, "tools": [...] }
# Each tool entry:
#   { "name": str, "url": str, "flags": list[str],
#     "purpose": str, "usage": str, "notes": str }
# flags ∈ {"T","D","R","M"}
# ─────────────────────────────────────────────────────────────────────────────

FRAMEWORK: dict = {
    "Usernames": {
        "desc": "Search for usernames across social networks and sites.",
        "tools": [],
        "subcategories": {
            "Username Search Engines": {
                "desc": "Multi-site username lookup tools.",
                "tools": [
                    {"name": "Sherlock (T)", "url": "https://github.com/sherlock-project/sherlock",
                     "flags": ["T"],
                     "purpose": "Hunt usernames across 400+ social networks from the command line.",
                     "usage": "pip install sherlock-project\nsherlock <username>",
                     "notes": "Requires Python 3.6+. One of the most comprehensive username tools available."},
                    {"name": "Maigret (T)", "url": "https://github.com/soxoj/maigret",
                     "flags": ["T"],
                     "purpose": "Collect a dossier on a person by username; checks 3000+ sites.",
                     "usage": "pip install maigret\nmaigret <username>",
                     "notes": "Actively maintained fork/successor to Sherlock with more sites."},
                    {"name": "WhatsMyName", "url": "https://whatsmyname.app",
                     "flags": [],
                     "purpose": "Enumerate usernames across many websites via a simple web UI.",
                     "usage": "Visit site → enter username → review results.",
                     "notes": "Also available as a CLI tool on GitHub (webbreacher/WhatsMyName)."},
                    {"name": "Namechk", "url": "https://namechk.com",
                     "flags": [],
                     "purpose": "Check username/domain availability across social networks & domains.",
                     "usage": "Enter desired username → see availability heat-map.",
                     "notes": "Useful for brand monitoring and squatting detection."},
                    {"name": "UserSearch.org", "url": "https://usersearch.org",
                     "flags": [],
                     "purpose": "Search for a username across 2000+ websites.",
                     "usage": "Enter username → browse categorised results.",
                     "notes": "Web-based; no account required."},
                    {"name": "KnowEm", "url": "https://knowem.com",
                     "flags": [],
                     "purpose": "Check username across 500+ social networks.",
                     "usage": "Enter username → get full availability report.",
                     "notes": "Handy for brand/trademark OSINT."},
                    {"name": "Namecheckr", "url": "https://www.namecheckr.com",
                     "flags": [],
                     "purpose": "Check social media username availability across platforms.",
                     "usage": "Enter username → get colour-coded results.",
                     "notes": "Fast, free, no login needed."},
                    {"name": "Instant Username Search", "url": "https://instantusername.com",
                     "flags": [],
                     "purpose": "Real-time username availability check across platforms.",
                     "usage": "Type username → results appear instantly.",
                     "notes": "Good for rapid checks; less comprehensive than Sherlock."},
                ],
                "subcategories": {}
            },
            "Specific Sites": {
                "desc": "Look up profiles on individual social platforms.",
                "tools": [
                    {"name": "GitHub Profile (M)", "url": "https://github.com/<username>",
                     "flags": ["M"],
                     "purpose": "Direct URL to a GitHub profile.",
                     "usage": "Replace <username> in URL.",
                     "notes": "Check repos, gists, stars, contributions."},
                    {"name": "Twitter/X Profile (M)", "url": "https://twitter.com/<username>",
                     "flags": ["M"],
                     "purpose": "Direct URL to a Twitter/X profile.",
                     "usage": "Replace <username> in URL.",
                     "notes": "Check tweets, follows, media."},
                    {"name": "Reddit User (M)", "url": "https://www.reddit.com/user/<username>",
                     "flags": ["M"],
                     "purpose": "View all posts and comments by a Reddit user.",
                     "usage": "Replace <username> in URL.",
                     "notes": "Reddit public API also returns full history."},
                    {"name": "Instagram (M)", "url": "https://www.instagram.com/<username>",
                     "flags": ["M"],
                     "purpose": "View a public Instagram profile.",
                     "usage": "Replace <username> in URL.",
                     "notes": "Private accounts require a follow request."},
                ],
                "subcategories": {}
            }
        }
    },
    "Email Addresses": {
        "desc": "Tools to investigate, validate, and enumerate email addresses.",
        "tools": [],
        "subcategories": {
            "Email Verification": {
                "desc": "Verify whether an email address is valid/live.",
                "tools": [
                    {"name": "Hunter.io (R)", "url": "https://hunter.io",
                     "flags": ["R"],
                     "purpose": "Find and verify professional email addresses by domain.",
                     "usage": "Enter domain → get list of emails + confidence score.",
                     "notes": "Free tier: 25 searches/month. Also has API."},
                    {"name": "EmailHippo", "url": "https://tools.emailhippo.com",
                     "flags": [],
                     "purpose": "Verify if an email address exists and is deliverable.",
                     "usage": "Enter email → get status (valid / invalid / unknown).",
                     "notes": "Does not send an actual email; uses SMTP probing."},
                    {"name": "Verify Email Address", "url": "https://verify-email.org",
                     "flags": [],
                     "purpose": "Checks MX records and SMTP to validate email delivery.",
                     "usage": "Enter email → check result.",
                     "notes": "Free, simple, no registration."},
                    {"name": "MailTester", "url": "https://www.mailtester.com",
                     "flags": [],
                     "purpose": "Validate email syntax and MX record existence.",
                     "usage": "Enter email → get validation result.",
                     "notes": "Lightweight; does not do SMTP connection."},
                ],
                "subcategories": {}
            },
            "Breach / Paste Search": {
                "desc": "Check if an email appeared in known data breaches.",
                "tools": [
                    {"name": "Have I Been Pwned", "url": "https://haveibeenpwned.com",
                     "flags": [],
                     "purpose": "Check if an email appeared in publicly known data breaches.",
                     "usage": "Enter email → see breach list with dates and data types exposed.",
                     "notes": "Run by Troy Hunt. Very reliable and comprehensive."},
                    {"name": "DeHashed (R)", "url": "https://dehashed.com",
                     "flags": ["R"],
                     "purpose": "Search leaked credentials (email, username, password, IP).",
                     "usage": "Log in → search by email / domain / IP.",
                     "notes": "Paid after free trial. Very large breach database."},
                    {"name": "Leak-Lookup (R)", "url": "https://leak-lookup.com",
                     "flags": ["R"],
                     "purpose": "Check emails/usernames against known breach datasets.",
                     "usage": "Enter email or username → see matched datasets.",
                     "notes": "Freemium; limited free queries."},
                    {"name": "IntelX", "url": "https://intelx.io",
                     "flags": ["R"],
                     "purpose": "Search engine for leaked data, dark web, pastes, emails.",
                     "usage": "Enter email → see results across pastes and breaches.",
                     "notes": "Free tier available; advanced features require subscription."},
                    {"name": "Snusbase (R)", "url": "https://snusbase.com",
                     "flags": ["R"],
                     "purpose": "Search through data breaches by email, username, IP, hash.",
                     "usage": "Enter search term → get matched breach data.",
                     "notes": "Subscription-based."},
                ],
                "subcategories": {}
            },
            "Email Header Analysis": {
                "desc": "Analyse raw email headers for routing and metadata.",
                "tools": [
                    {"name": "MXToolbox Email Headers", "url": "https://mxtoolbox.com/EmailHeaders.aspx",
                     "flags": [],
                     "purpose": "Parse and visualise email headers to trace routing path.",
                     "usage": "Paste raw email header → get timeline and hop analysis.",
                     "notes": "Also shows SPF/DKIM/DMARC alignment."},
                    {"name": "Google Admin Toolbox", "url": "https://toolbox.googleapps.com/apps/messageheader/",
                     "flags": [],
                     "purpose": "Analyse Gmail/Google Workspace email headers.",
                     "usage": "Paste header → see message routing delays.",
                     "notes": "Official Google tool; great for GSuite environments."},
                ],
                "subcategories": {}
            }
        }
    },
    "Domain Names": {
        "desc": "Tools to investigate domain ownership, history, DNS, and infrastructure.",
        "tools": [],
        "subcategories": {
            "WHOIS": {
                "desc": "Domain registration and ownership lookups.",
                "tools": [
                    {"name": "WHOIS Lookup", "url": "https://www.whois.com/whois/",
                     "flags": [],
                     "purpose": "Query WHOIS database for domain registration details.",
                     "usage": "Enter domain → see registrant, dates, nameservers.",
                     "notes": "GDPR redaction applies to many .com/.net domains."},
                    {"name": "DomainTools (R)", "url": "https://www.domaintools.com",
                     "flags": ["R"],
                     "purpose": "Advanced WHOIS, DNS, and domain history research.",
                     "usage": "Enter domain → get current + historical WHOIS, hosting history.",
                     "notes": "Industry-leading; paid subscription for full data."},
                    {"name": "ViewDNS.info", "url": "https://viewdns.info",
                     "flags": [],
                     "purpose": "Collection of DNS/IP lookup tools in one place.",
                     "usage": "Choose tool (Reverse IP, WHOIS, DNS report, etc.) → enter target.",
                     "notes": "Free; no registration required. Very useful collection."},
                    {"name": "Who.is", "url": "https://who.is",
                     "flags": [],
                     "purpose": "Simple WHOIS lookup with clean interface.",
                     "usage": "Enter domain → view registration info.",
                     "notes": "Good fallback when other tools are gated."},
                    {"name": "Whoxy (R)", "url": "https://www.whoxy.com",
                     "flags": ["R"],
                     "purpose": "Reverse WHOIS: find all domains registered by an email or name.",
                     "usage": "Enter email/name/phone → get domain list.",
                     "notes": "Freemium; paid for bulk reverse WHOIS."},
                ],
                "subcategories": {}
            },
            "DNS Records": {
                "desc": "Query and analyse DNS records.",
                "tools": [
                    {"name": "MXToolbox", "url": "https://mxtoolbox.com",
                     "flags": [],
                     "purpose": "DNS lookup, MX records, blacklist check, SMTP diagnostics.",
                     "usage": "Enter domain → choose record type (MX, A, AAAA, TXT, etc.).",
                     "notes": "Go-to for email infrastructure OSINT."},
                    {"name": "DNSdumpster", "url": "https://dnsdumpster.com",
                     "flags": [],
                     "purpose": "Passive DNS recon — discover subdomains and DNS records.",
                     "usage": "Enter domain → get DNS map with graph visualisation.",
                     "notes": "Free; does not actively scan target. Great for passive recon."},
                    {"name": "SecurityTrails (R)", "url": "https://securitytrails.com",
                     "flags": ["R"],
                     "purpose": "Historical DNS and WHOIS data for domain intelligence.",
                     "usage": "Search domain → view current/historical A, MX, NS records.",
                     "notes": "Free account gives limited history; paid for full depth."},
                    {"name": "Shodan (R)", "url": "https://www.shodan.io",
                     "flags": ["R"],
                     "purpose": "Search engine for internet-connected devices; find open ports/services.",
                     "usage": "Search domain or IP → see exposed services, ports, banners.",
                     "notes": "Freemium. Extremely powerful for infrastructure OSINT."},
                    {"name": "Censys (R)", "url": "https://censys.io",
                     "flags": ["R"],
                     "purpose": "Internet-wide scanning data: certificates, hosts, ports.",
                     "usage": "Search domain or IP → see TLS certs, open ports.",
                     "notes": "Free researcher accounts available."},
                    {"name": "Robtex", "url": "https://www.robtex.com",
                     "flags": [],
                     "purpose": "DNS and network intelligence with graph relationships.",
                     "usage": "Enter domain or IP → see linked domains, ASN, routing.",
                     "notes": "Great for visualising infrastructure connections."},
                ],
                "subcategories": {}
            },
            "Subdomains": {
                "desc": "Discover subdomains of a target domain.",
                "tools": [
                    {"name": "Sublist3r (T)", "url": "https://github.com/aboul3la/Sublist3r",
                     "flags": ["T"],
                     "purpose": "Fast passive subdomain enumeration using multiple sources.",
                     "usage": "pip install sublist3r\npython sublist3r.py -d example.com",
                     "notes": "Uses Google, Bing, Virustotal, Netcraft, Shodan, etc."},
                    {"name": "crt.sh", "url": "https://crt.sh",
                     "flags": [],
                     "purpose": "Search Certificate Transparency logs to find subdomains.",
                     "usage": "Enter %.domain.com → get all subdomains in SSL certs.",
                     "notes": "100% passive. Gold standard for cert-based subdomain discovery."},
                    {"name": "Amass (T)", "url": "https://github.com/owasp-amass/amass",
                     "flags": ["T"],
                     "purpose": "In-depth attack surface mapping and subdomain enumeration.",
                     "usage": "go install github.com/owasp-amass/amass/v4/...\namass enum -d example.com",
                     "notes": "OWASP project. Most comprehensive open-source subdomain tool."},
                    {"name": "Pentest-Tools Subdomain Finder (R)", "url": "https://pentest-tools.com/information-gathering/find-subdomains-of-domain",
                     "flags": ["R"],
                     "purpose": "Web-based subdomain scanner.",
                     "usage": "Enter domain → receive subdomain list.",
                     "notes": "Limited free scans; paid for full results."},
                ],
                "subcategories": {}
            },
            "Domain History": {
                "desc": "View archived or historical domain states.",
                "tools": [
                    {"name": "Wayback Machine", "url": "https://web.archive.org",
                     "flags": [],
                     "purpose": "View archived snapshots of websites over time.",
                     "usage": "Enter URL → navigate calendar to choose snapshot date.",
                     "notes": "Invaluable for investigating deleted/changed content."},
                    {"name": "Archive.ph", "url": "https://archive.ph",
                     "flags": [],
                     "purpose": "Create and retrieve saved snapshots of web pages.",
                     "usage": "Enter URL → get permanent snapshot link.",
                     "notes": "Great for preserving evidence before it disappears."},
                    {"name": "DomainHistory (M)", "url": "https://www.domainhistory.net",
                     "flags": ["M"],
                     "purpose": "View historical WHOIS records and DNS changes.",
                     "usage": "Enter domain → browse registration timeline.",
                     "notes": "Shows ownership changes over years."},
                ],
                "subcategories": {}
            }
        }
    },
    "IP Addresses": {
        "desc": "Investigate IP addresses — geolocation, ownership, reputation.",
        "tools": [],
        "subcategories": {
            "Geolocation": {
                "desc": "Map an IP address to a geographic location.",
                "tools": [
                    {"name": "ipinfo.io (M)", "url": "https://ipinfo.io/<ip>",
                     "flags": ["M"],
                     "purpose": "IP geolocation, ASN, hostname, and carrier info.",
                     "usage": "Replace <ip> in URL or use API: curl ipinfo.io/<ip>",
                     "notes": "Very accurate; free tier 50k requests/month."},
                    {"name": "MaxMind GeoIP", "url": "https://www.maxmind.com/en/geoip-demo",
                     "flags": [],
                     "purpose": "Industry-standard IP geolocation database demo.",
                     "usage": "Enter IP → see city, region, country, ASN.",
                     "notes": "Used by most security tools under the hood."},
                    {"name": "IP-API", "url": "http://ip-api.com",
                     "flags": [],
                     "purpose": "Free JSON IP geolocation API.",
                     "usage": "curl http://ip-api.com/json/<ip>",
                     "notes": "45 requests/min free; no key needed."},
                    {"name": "WhatIsMyIPAddress", "url": "https://whatismyipaddress.com",
                     "flags": [],
                     "purpose": "Lookup an IP with geolocation and reverse DNS.",
                     "usage": "Enter IP in search bar.",
                     "notes": "Good fallback for quick manual lookups."},
                ],
                "subcategories": {}
            },
            "Reputation / Blacklist": {
                "desc": "Check if an IP is malicious or blacklisted.",
                "tools": [
                    {"name": "VirusTotal", "url": "https://www.virustotal.com",
                     "flags": [],
                     "purpose": "Scan IP/domain/file against 70+ antivirus and reputation engines.",
                     "usage": "Paste IP or URL → see detections and community reports.",
                     "notes": "Free; also has an API for automation."},
                    {"name": "AbuseIPDB (R)", "url": "https://www.abuseipdb.com",
                     "flags": ["R"],
                     "purpose": "Community database of IPs reported for malicious activity.",
                     "usage": "Enter IP → see abuse confidence score and report history.",
                     "notes": "Free account gives API access (1000 checks/day)."},
                    {"name": "Talos Intelligence", "url": "https://talosintelligence.com/reputation_center",
                     "flags": [],
                     "purpose": "Cisco Talos IP and domain reputation lookup.",
                     "usage": "Enter IP/domain → see reputation score and category.",
                     "notes": "Backed by Cisco's global threat telemetry."},
                    {"name": "MXToolbox Blacklist Check", "url": "https://mxtoolbox.com/blacklists.aspx",
                     "flags": [],
                     "purpose": "Check if an IP is on any major email blacklist (DNSBL).",
                     "usage": "Enter IP → check against 100+ blacklists at once.",
                     "notes": "Critical for email infrastructure investigations."},
                    {"name": "Shodan (R)", "url": "https://www.shodan.io",
                     "flags": ["R"],
                     "purpose": "Find open ports and services on an IP address.",
                     "usage": "Search <ip> → see exposed banners, ports, vulns.",
                     "notes": "The definitive tool for IP/device fingerprinting."},
                ],
                "subcategories": {}
            },
            "BGP / ASN": {
                "desc": "Autonomous System Number and routing intelligence.",
                "tools": [
                    {"name": "BGP.he.net", "url": "https://bgp.he.net",
                     "flags": [],
                     "purpose": "BGP routing, ASN info, prefix ownership, peering.",
                     "usage": "Enter IP/ASN/domain → see routing relationships.",
                     "notes": "Hurricane Electric's BGP toolkit. Industry standard."},
                    {"name": "RIPEstat", "url": "https://stat.ripe.net",
                     "flags": [],
                     "purpose": "RIPE NCC data for IP routing, prefix, and ASN analysis.",
                     "usage": "Enter IP or prefix → see routing history and allocation.",
                     "notes": "Authoritative for RIPE region (Europe/Middle East)."},
                    {"name": "ARIN Whois (M)", "url": "https://search.arin.net/rdap/",
                     "flags": ["M"],
                     "purpose": "IP address registration lookup for North America (ARIN).",
                     "usage": "Enter IP → get allocation and organisation info.",
                     "notes": "Use for IPs in the ARIN region."},
                ],
                "subcategories": {}
            }
        }
    },
    "Social Networks": {
        "desc": "OSINT tools for major social media platforms.",
        "tools": [],
        "subcategories": {
            "Twitter / X": {
                "desc": "Search and analyse Twitter/X content and accounts.",
                "tools": [
                    {"name": "Twitter Advanced Search (M)", "url": "https://twitter.com/search-advanced",
                     "flags": ["M"],
                     "purpose": "Advanced query filtering: by user, date, location, words.",
                     "usage": "Use operators: from:user, since:date, near:city, etc.",
                     "notes": "Free; very powerful for targeted tweet discovery."},
                    {"name": "TweetDeck", "url": "https://tweetdeck.twitter.com",
                     "flags": ["R"],
                     "purpose": "Multi-column Twitter dashboard for monitoring accounts/hashtags.",
                     "usage": "Add columns for lists, searches, accounts.",
                     "notes": "Now requires Twitter Blue subscription."},
                    {"name": "Twitonomy (R)", "url": "https://www.twitonomy.com",
                     "flags": ["R"],
                     "purpose": "Twitter analytics: tweet patterns, mentions, hashtags, followers.",
                     "usage": "Log in with Twitter → analyse any public account.",
                     "notes": "Free account gives basic stats."},
                    {"name": "Social Bearing", "url": "https://socialbearing.com",
                     "flags": [],
                     "purpose": "Twitter analytics and search with geographic mapping.",
                     "usage": "Search by keyword, hashtag, or username.",
                     "notes": "Good for event-based monitoring."},
                ],
                "subcategories": {}
            },
            "Facebook": {
                "desc": "Search and investigate Facebook content.",
                "tools": [
                    {"name": "Facebook Search (D)", "url": "https://www.google.com/search?q=site:facebook.com",
                     "flags": ["D"],
                     "purpose": "Use Google to search within Facebook's public pages.",
                     "usage": 'Google dork: site:facebook.com "<target name>"',
                     "notes": "Workaround for Facebook's limited public search."},
                    {"name": "Lookup-ID.com", "url": "https://lookup-id.com",
                     "flags": [],
                     "purpose": "Find the numeric Facebook ID behind a profile URL.",
                     "usage": "Paste Facebook profile URL → get numeric ID.",
                     "notes": "Useful for tracking renamed/vanity URL profiles."},
                    {"name": "IntelTechniques Facebook", "url": "https://inteltechniques.com/tools/Facebook.html",
                     "flags": [],
                     "purpose": "Curated collection of Facebook OSINT search tools.",
                     "usage": "Select search type → enter query → execute.",
                     "notes": "By Michael Bazzell — excellent for structured FB investigation."},
                ],
                "subcategories": {}
            },
            "LinkedIn": {
                "desc": "Professional network intelligence.",
                "tools": [
                    {"name": "LinkedIn People Search (D)", "url": "https://www.google.com/search?q=site:linkedin.com/in/",
                     "flags": ["D"],
                     "purpose": "Use Google to search LinkedIn profiles without logging in.",
                     "usage": 'site:linkedin.com/in/ "<name>" "<company>"',
                     "notes": "Bypasses LinkedIn's paywall for viewing profiles."},
                    {"name": "Recruitin.net", "url": "https://recruitin.net",
                     "flags": [],
                     "purpose": "Build Google X-ray search queries for LinkedIn profiles.",
                     "usage": "Enter job title/skills/location → copy generated query.",
                     "notes": "Great for finding LinkedIn profiles without a paid subscription."},
                    {"name": "ContactOut (R)", "url": "https://contactout.com",
                     "flags": ["R"],
                     "purpose": "Find emails and phone numbers from LinkedIn profiles.",
                     "usage": "Install extension → browse LinkedIn → see contact data.",
                     "notes": "Freemium; limited free credits."},
                ],
                "subcategories": {}
            },
            "Instagram": {
                "desc": "Instagram profile and content OSINT.",
                "tools": [
                    {"name": "Instalooter (T)", "url": "https://github.com/althonos/instalooter",
                     "flags": ["T"],
                     "purpose": "Download all media from an Instagram account (public).",
                     "usage": "pip install instalooter\ninstalooter user <username> ./output",
                     "notes": "Works on public profiles; no API key needed."},
                    {"name": "Imginn", "url": "https://imginn.com",
                     "flags": [],
                     "purpose": "View and download Instagram posts/stories without an account.",
                     "usage": "Enter Instagram username → browse content.",
                     "notes": "Public profiles only."},
                    {"name": "Picuki", "url": "https://www.picuki.com",
                     "flags": [],
                     "purpose": "Browse and download Instagram profile content anonymously.",
                     "usage": "Enter username in search → view posts, reels, stories.",
                     "notes": "No account required."},
                ],
                "subcategories": {}
            },
            "Reddit": {
                "desc": "Search and analyse Reddit users and content.",
                "tools": [
                    {"name": "Pushshift.io (R)", "url": "https://pushshift.io",
                     "flags": ["R"],
                     "purpose": "Historical Reddit data: search deleted posts and comments.",
                     "usage": "Use API: https://api.pushshift.io/reddit/search/comment/?author=<user>",
                     "notes": "Access now restricted; check current API availability."},
                    {"name": "Reddit User Analyser", "url": "https://redditmetis.com",
                     "flags": [],
                     "purpose": "Analyse posting patterns, sentiment, and activity of a Reddit user.",
                     "usage": "Enter username → view subreddit breakdown and timeline.",
                     "notes": "Useful for behavioural profiling."},
                    {"name": "Subreddit Stats", "url": "https://subredditstats.com",
                     "flags": [],
                     "purpose": "Statistics and trends for subreddits.",
                     "usage": "Enter subreddit name → see growth and activity graphs.",
                     "notes": "Good for community-level OSINT."},
                ],
                "subcategories": {}
            }
        }
    },
    "People Search": {
        "desc": "Search engines and aggregators that compile personal data.",
        "tools": [],
        "subcategories": {
            "People Search Engines": {
                "desc": "Aggregators that compile public records, social data, etc.",
                "tools": [
                    {"name": "Pipl (R)", "url": "https://pipl.com",
                     "flags": ["R"],
                     "purpose": "Deep web people search — aggregates public records, social, professional data.",
                     "usage": "Enter name/email/username/phone → get comprehensive profile.",
                     "notes": "Paid; considered one of the best people-search tools. Used by investigators."},
                    {"name": "Spokeo (R)", "url": "https://www.spokeo.com",
                     "flags": ["R"],
                     "purpose": "Aggregate public data: address, relatives, social profiles.",
                     "usage": "Enter name/address/phone/email → view profile.",
                     "notes": "US-focused; freemium model."},
                    {"name": "TruthFinder (R)", "url": "https://www.truthfinder.com",
                     "flags": ["R"],
                     "purpose": "Background check using public records.",
                     "usage": "Enter name and location → get background report.",
                     "notes": "US only; subscription required."},
                    {"name": "Intelius (R)", "url": "https://www.intelius.com",
                     "flags": ["R"],
                     "purpose": "People search: address, phone, relatives, criminal records.",
                     "usage": "Enter name → choose from results → purchase report.",
                     "notes": "US-focused; pay-per-report or subscription."},
                    {"name": "BeenVerified (R)", "url": "https://www.beenverified.com",
                     "flags": ["R"],
                     "purpose": "Background check on individuals using public data.",
                     "usage": "Enter name, email, or phone → view report.",
                     "notes": "Subscription-based; unlimited searches."},
                    {"name": "PeekYou", "url": "https://www.peekyou.com",
                     "flags": [],
                     "purpose": "Find someone's social profiles, usernames, and web presence.",
                     "usage": "Enter name → browse linked social accounts.",
                     "notes": "Free; good for social media footprint mapping."},
                ],
                "subcategories": {}
            },
            "Public Records": {
                "desc": "Government and judicial public records.",
                "tools": [
                    {"name": "PACER (R)", "url": "https://pacer.uscourts.gov",
                     "flags": ["R"],
                     "purpose": "US federal court case records access.",
                     "usage": "Register → search by name or case number → download documents.",
                     "notes": "$.10/page; registration required. Essential for US legal OSINT."},
                    {"name": "BlackBookOnline", "url": "https://www.blackbookonline.info",
                     "flags": [],
                     "purpose": "Directory of free public records databases by US state.",
                     "usage": "Select state → choose record type → use linked resource.",
                     "notes": "Free; aggregates links to state/county databases."},
                ],
                "subcategories": {}
            }
        }
    },
    "Phone Numbers": {
        "desc": "Investigate phone numbers — carrier, owner, spam reports.",
        "tools": [],
        "subcategories": {
            "Number Lookup": {
                "desc": "Identify phone number carrier and geographic data.",
                "tools": [
                    {"name": "Twilio Lookup (R)", "url": "https://www.twilio.com/lookup",
                     "flags": ["R"],
                     "purpose": "Validate phone numbers and get carrier/line type info via API.",
                     "usage": "API: GET /Lookups/v1/PhoneNumbers/<number>",
                     "notes": "Requires Twilio account. Pay-as-you-go pricing."},
                    {"name": "Truecaller (R)", "url": "https://www.truecaller.com",
                     "flags": ["R"],
                     "purpose": "Crowdsourced phone book — identify unknown callers.",
                     "usage": "Search phone number → see name if registered.",
                     "notes": "Registration required; widely used in India and Africa."},
                    {"name": "SpyDialer", "url": "https://www.spydialer.com",
                     "flags": [],
                     "purpose": "Reverse phone lookup — name, carrier, voicemail.",
                     "usage": "Enter phone number → view linked name/voicemail.",
                     "notes": "Free and no registration needed for basic lookups."},
                    {"name": "NumLookup", "url": "https://www.numlookup.com",
                     "flags": [],
                     "purpose": "Free reverse phone lookup for name and carrier.",
                     "usage": "Enter phone number → see owner info.",
                     "notes": "US numbers work best."},
                    {"name": "PhoneInfoga (T)", "url": "https://github.com/sundowndev/phoneinfoga",
                     "flags": ["T"],
                     "purpose": "Scan phone numbers for available information from public sources.",
                     "usage": "docker run sundowndev/phoneinfoga scan -n <number>\nor: go install + phoneinfoga scan -n +1XXXXXXXXXX",
                     "notes": "Open-source; supports multiple scanners. Great OSINT CLI tool."},
                    {"name": "Reverse Phone Lookup (M)", "url": "https://www.whitepages.com/reverse-phone/<number>",
                     "flags": ["M"],
                     "purpose": "White Pages reverse phone lookup.",
                     "usage": "Replace <number> in URL with target phone.",
                     "notes": "Free basic results; paid for detailed report."},
                ],
                "subcategories": {}
            }
        }
    },
    "Images / Video / Docs": {
        "desc": "Reverse image search, metadata extraction, and video analysis.",
        "tools": [],
        "subcategories": {
            "Reverse Image Search": {
                "desc": "Find where an image appears or who is in it.",
                "tools": [
                    {"name": "Google Images (M)", "url": "https://images.google.com",
                     "flags": ["M"],
                     "purpose": "Reverse image search across the web.",
                     "usage": "Click camera icon → upload image or paste URL.",
                     "notes": "Strongest general-purpose reverse image engine."},
                    {"name": "TinEye", "url": "https://tineye.com",
                     "flags": [],
                     "purpose": "Find where an image first appeared and where it has been used.",
                     "usage": "Upload image or paste URL → get list of matches with dates.",
                     "notes": "40+ billion indexed images. Best for first-seen analysis."},
                    {"name": "Yandex Images (M)", "url": "https://yandex.com/images/",
                     "flags": ["M"],
                     "purpose": "Russian reverse image search — excellent for facial recognition.",
                     "usage": "Click camera icon → upload image.",
                     "notes": "Often finds matches that Google/TinEye miss. Great for faces."},
                    {"name": "Bing Visual Search (M)", "url": "https://www.bing.com/visualsearch",
                     "flags": ["M"],
                     "purpose": "Microsoft's reverse image search with product recognition.",
                     "usage": "Upload image or paste URL.",
                     "notes": "Good complementary tool alongside Google."},
                ],
                "subcategories": {}
            },
            "Metadata / EXIF": {
                "desc": "Extract hidden metadata from images and documents.",
                "tools": [
                    {"name": "ExifTool (T)", "url": "https://exiftool.org",
                     "flags": ["T"],
                     "purpose": "Read, write, and edit metadata in images, audio, video, PDFs.",
                     "usage": "exiftool <filename>",
                     "notes": "The definitive metadata tool. GPS coords can reveal location."},
                    {"name": "Jeffrey's Exif Viewer", "url": "https://exif.regex.info/exif.cgi",
                     "flags": [],
                     "purpose": "Web-based EXIF viewer — see camera data, GPS, timestamps.",
                     "usage": "Upload image or paste URL → view full EXIF data.",
                     "notes": "Easy web alternative to ExifTool. Shows GPS map if present."},
                    {"name": "Metagoofil (T)", "url": "https://github.com/laramies/metagoofil",
                     "flags": ["T"],
                     "purpose": "Extract metadata from public documents (PDF, DOC, XLS, PPT).",
                     "usage": "python metagoofil.py -d example.com -t pdf -l 20 -o output/",
                     "notes": "Finds documents via Google and extracts author/software metadata."},
                    {"name": "Foca (T)", "url": "https://github.com/ElevenPaths/FOCA",
                     "flags": ["T"],
                     "purpose": "Fingerprint organisations via document metadata (Windows tool).",
                     "usage": "Windows GUI: enter domain → scan → extract metadata.",
                     "notes": "Finds internal hostnames, usernames, software versions in docs."},
                ],
                "subcategories": {}
            },
            "Video Analysis": {
                "desc": "Analyse and verify video content.",
                "tools": [
                    {"name": "InVID / WeVerify", "url": "https://weverify.eu/verification-plugin/",
                     "flags": [],
                     "purpose": "Verify video authenticity; extract keyframes for reverse image search.",
                     "usage": "Install browser extension → paste video URL → analyse frames.",
                     "notes": "Essential tool for journalists and OSINT investigators."},
                    {"name": "YouTube DataViewer", "url": "https://www.amnestytech.org/yt-dataviewer/",
                     "flags": [],
                     "purpose": "Extract metadata and thumbnails from YouTube videos for reverse searching.",
                     "usage": "Paste YouTube URL → get exact upload time and thumbnail links.",
                     "notes": "Amnesty International tool for video verification."},
                ],
                "subcategories": {}
            }
        }
    },
    "Threat Intelligence": {
        "desc": "Malware databases, CVE lookups, and threat actor tracking.",
        "tools": [],
        "subcategories": {
            "Malware": {
                "desc": "Analyse suspicious files and URLs for malware.",
                "tools": [
                    {"name": "VirusTotal", "url": "https://www.virustotal.com",
                     "flags": [],
                     "purpose": "Scan files, URLs, IPs, and domains against 70+ security engines.",
                     "usage": "Upload file or paste URL → see detection results.",
                     "notes": "Industry standard. Also has an API for automation."},
                    {"name": "Any.run (R)", "url": "https://any.run",
                     "flags": ["R"],
                     "purpose": "Interactive online sandbox — run malware and watch behaviour live.",
                     "usage": "Upload sample → see process tree, network calls, registry changes.",
                     "notes": "Free public analysis; paid for private sandboxing."},
                    {"name": "Hybrid Analysis", "url": "https://www.hybrid-analysis.com",
                     "flags": [],
                     "purpose": "Free malware analysis sandbox with detailed reports.",
                     "usage": "Upload file → choose environment → view full sandbox report.",
                     "notes": "Powered by CrowdStrike Falcon Sandbox. No registration for basic use."},
                    {"name": "MalwareBazaar", "url": "https://bazaar.abuse.ch/browse/",
                     "flags": [],
                     "purpose": "Repository of malware samples for threat intelligence.",
                     "usage": "Search by hash, tag, or signature → download sample or report.",
                     "notes": "Abuse.ch project; free access."},
                ],
                "subcategories": {}
            },
            "CVE / Vulnerabilities": {
                "desc": "Look up known vulnerabilities by CVE identifier.",
                "tools": [
                    {"name": "NVD - NIST", "url": "https://nvd.nist.gov/vuln/search",
                     "flags": [],
                     "purpose": "Official US National Vulnerability Database CVE lookup.",
                     "usage": "Search CVE-YYYY-NNNNN → view severity, CVSS, references.",
                     "notes": "Authoritative source for CVE data."},
                    {"name": "CVE Details", "url": "https://www.cvedetails.com",
                     "flags": [],
                     "purpose": "Browse CVE data with statistics and vendor breakdowns.",
                     "usage": "Search CVE or browse by vendor/product.",
                     "notes": "Good for comparing vulnerability history of vendors."},
                    {"name": "Exploit-DB", "url": "https://www.exploit-db.com",
                     "flags": [],
                     "purpose": "Archive of public exploits and proof-of-concept code.",
                     "usage": "Search CVE or product → download PoC if available.",
                     "notes": "Maintained by Offensive Security."},
                    {"name": "Shodan CVE Search (R)", "url": "https://cvedb.shodan.io",
                     "flags": ["R"],
                     "purpose": "Link CVEs to exposed vulnerable hosts on the internet.",
                     "usage": "Search CVE → see how many internet-facing hosts are vulnerable.",
                     "notes": "Shodan account required."},
                ],
                "subcategories": {}
            },
            "Threat Feeds": {
                "desc": "Live feeds of IOCs and threat actor intelligence.",
                "tools": [
                    {"name": "AlienVault OTX", "url": "https://otx.alienvault.com",
                     "flags": [],
                     "purpose": "Open Threat Exchange — community threat intelligence sharing.",
                     "usage": "Search IOC (IP/domain/hash) or browse pulses.",
                     "notes": "Free; huge community-contributed dataset."},
                    {"name": "ThreatFox", "url": "https://threatfox.abuse.ch",
                     "flags": [],
                     "purpose": "IOC sharing platform for malware C2, domains, IPs.",
                     "usage": "Search IOC → see malware family and threat actor association.",
                     "notes": "Abuse.ch project; free."},
                    {"name": "URLhaus", "url": "https://urlhaus.abuse.ch",
                     "flags": [],
                     "purpose": "Database of malicious URLs used for malware distribution.",
                     "usage": "Search URL or domain → see threat classification.",
                     "notes": "Abuse.ch project; also has an API."},
                    {"name": "MISP (T)", "url": "https://www.misp-project.org",
                     "flags": ["T"],
                     "purpose": "Open-source threat intelligence platform for sharing IOCs.",
                     "usage": "Self-hosted: docker-compose up\nThen import/export events via UI or API.",
                     "notes": "Standard in enterprise and government SOC environments."},
                ],
                "subcategories": {}
            }
        }
    },
    "Dark Web": {
        "desc": "Tools and resources for dark web OSINT (use Tor / ethical use only).",
        "tools": [],
        "subcategories": {
            "Search Engines": {
                "desc": "Search engines that index .onion content.",
                "tools": [
                    {"name": "Ahmia", "url": "https://ahmia.fi",
                     "flags": [],
                     "purpose": "Search engine for Tor hidden services (accessible via clearnet).",
                     "usage": "Search term → browse indexed .onion results.",
                     "notes": "Filters out CSAM. Accessible without Tor."},
                    {"name": "Hunchly Dark Web (R)", "url": "https://www.hunch.ly",
                     "flags": ["R"],
                     "purpose": "Dark web OSINT collection and monitoring tool.",
                     "usage": "Install → set up monitoring → capture dark web content.",
                     "notes": "Paid tool; used by professional investigators."},
                    {"name": "IntelX (Dark Web)", "url": "https://intelx.io",
                     "flags": ["R"],
                     "purpose": "Search dark web, pastes, and leaked data from clearnet.",
                     "usage": "Enter search term → filter by data source.",
                     "notes": "Freemium; premium for full results."},
                ],
                "subcategories": {}
            }
        }
    },
    "Geolocation Tools": {
        "desc": "Identify and verify geographic locations from images, videos, or metadata.",
        "tools": [],
        "subcategories": {
            "Mapping": {
                "desc": "Map services and street-level imagery for location verification.",
                "tools": [
                    {"name": "Google Maps", "url": "https://maps.google.com",
                     "flags": [],
                     "purpose": "Street view, satellite imagery, business information.",
                     "usage": "Search address or coordinates → switch to Street View.",
                     "notes": "Best overall mapping tool. Historic Street View available."},
                    {"name": "Bing Maps", "url": "https://www.bing.com/maps",
                     "flags": [],
                     "purpose": "Bird's eye view and street-level imagery.",
                     "usage": "Enter address → switch views.",
                     "notes": "Bird's eye 45-degree view sometimes better than Google."},
                    {"name": "Yandex Maps", "url": "https://yandex.com/maps",
                     "flags": [],
                     "purpose": "Best mapping for Russia, Eastern Europe, Central Asia.",
                     "usage": "Enter address → view panoramas.",
                     "notes": "Street-level imagery often more recent than Google for Russia."},
                    {"name": "GeoHints", "url": "https://www.geohints.com",
                     "flags": [],
                     "purpose": "Reference for identifying country/region from visual clues.",
                     "usage": "Browse categories (road signs, licence plates, vegetation).",
                     "notes": "Very useful for GeoGuessr-style OSINT geolocation challenges."},
                ],
                "subcategories": {}
            },
            "Geolocation from Images": {
                "desc": "Extract or infer location from images.",
                "tools": [
                    {"name": "GeoCreepy (T)", "url": "https://www.geocreepy.com",
                     "flags": ["T"],
                     "purpose": "Collect geolocation data from social network posts.",
                     "usage": "Install → select platform → enter username → map results.",
                     "notes": "Linux/Windows GUI app; plots geotagged post locations on map."},
                    {"name": "Pic2Map", "url": "https://www.pic2map.com",
                     "flags": [],
                     "purpose": "Extract GPS coordinates from image EXIF and show on map.",
                     "usage": "Upload image → see GPS location on map.",
                     "notes": "Only works if image has GPS EXIF data embedded."},
                    {"name": "SunCalc", "url": "https://www.suncalc.org",
                     "flags": [],
                     "purpose": "Calculate sun position and shadow direction for geolocation.",
                     "usage": "Move map to location → set date/time → check shadow direction.",
                     "notes": "Matches shadow angles in photos to confirm location/time."},
                ],
                "subcategories": {}
            }
        }
    },
    "Search Engines": {
        "desc": "Alternative and specialised search engines for OSINT queries.",
        "tools": [],
        "subcategories": {
            "General": {
                "desc": "Standard and privacy-focused search engines.",
                "tools": [
                    {"name": "Google", "url": "https://www.google.com",
                     "flags": [],
                     "purpose": "Largest index; best for dorking and deep web surface scraping.",
                     "usage": "Use advanced operators: site:, filetype:, inurl:, intitle:, cache:",
                     "notes": "Essential. Pair with Google Dork cheatsheet for maximum output."},
                    {"name": "Bing", "url": "https://www.bing.com",
                     "flags": [],
                     "purpose": "Alternative index — sometimes indexes what Google does not.",
                     "usage": "Use site:, ip:, filetype: operators.",
                     "notes": "Useful for pages de-indexed from Google."},
                    {"name": "DuckDuckGo", "url": "https://duckduckgo.com",
                     "flags": [],
                     "purpose": "Privacy-focused search; does not personalise results.",
                     "usage": "Use !bangs for instant redirection: !g, !so, !wiki etc.",
                     "notes": "Less tracking noise in results; bangs are very powerful."},
                    {"name": "Yandex", "url": "https://yandex.com",
                     "flags": [],
                     "purpose": "Russian search engine — strongest for CIS region content.",
                     "usage": "Standard search; also supports image reverse search.",
                     "notes": "Often indexes content not found elsewhere. Excellent for faces."},
                    {"name": "Baidu", "url": "https://www.baidu.com",
                     "flags": [],
                     "purpose": "Dominant Chinese search engine — best for Chinese-language OSINT.",
                     "usage": "Search in Chinese characters for best results.",
                     "notes": "Essential for targets with China connections."},
                ],
                "subcategories": {}
            },
            "Specialised / IoT": {
                "desc": "Search engines indexing devices, code, and technical data.",
                "tools": [
                    {"name": "Shodan (R)", "url": "https://www.shodan.io",
                     "flags": ["R"],
                     "purpose": "Internet-of-Things search engine for exposed devices and services.",
                     "usage": "Search: apache country:IN\nFilters: port:, os:, org:, hostname:, city:",
                     "notes": "Free account limited to 2 pages. Paid for full API."},
                    {"name": "Censys (R)", "url": "https://censys.io",
                     "flags": ["R"],
                     "purpose": "Search internet-wide scan data for hosts, certs, and protocols.",
                     "usage": "Search IP/domain → view certificates, protocols, ports.",
                     "notes": "Free researcher tier available via application."},
                    {"name": "Fofa", "url": "https://fofa.info",
                     "flags": ["R"],
                     "purpose": "Chinese IoT/infrastructure search engine (similar to Shodan).",
                     "usage": "Use query syntax: domain='example.com' && country='CN'",
                     "notes": "Excellent for China-based infrastructure. Free tier limited."},
                    {"name": "ZoomEye (R)", "url": "https://www.zoomeye.org",
                     "flags": ["R"],
                     "purpose": "Another Chinese cyberspace search engine.",
                     "usage": "Enter domain or IP → see exposed services.",
                     "notes": "Useful alternative to Shodan, especially for Asia Pacific."},
                    {"name": "GreyNoise (R)", "url": "https://www.greynoise.io",
                     "flags": ["R"],
                     "purpose": "Identify mass-scanning internet noise vs targeted attacks.",
                     "usage": "Enter IP → see if it is a scanner, crawler, or targeted attacker.",
                     "notes": "Free community API. Extremely useful for filtering threat data."},
                    {"name": "GitHub Code Search (D)", "url": "https://github.com/search",
                     "flags": ["D"],
                     "purpose": "Search public GitHub repositories for exposed secrets and code.",
                     "usage": "Search: 'api_key' 'example.com'\nFilter by language, repo, user.",
                     "notes": "Find accidentally exposed credentials, API keys, config files."},
                ],
                "subcategories": {}
            }
        }
    },
    "Encoding / Decoding": {
        "desc": "Tools to encode, decode, and analyse data formats.",
        "tools": [],
        "subcategories": {
            "Online Tools": {
                "desc": "Browser-based encoding and crypto utilities.",
                "tools": [
                    {"name": "CyberChef", "url": "https://gchq.github.io/CyberChef/",
                     "flags": [],
                     "purpose": "GCHQ's 'Cyber Swiss Army Knife' — encode, decode, encrypt, analyse.",
                     "usage": "Drag operations into recipe → paste input → see output.",
                     "notes": "Supports 300+ operations: Base64, XOR, regex, hashing, hex..."},
                    {"name": "Base64 Decode", "url": "https://www.base64decode.org",
                     "flags": [],
                     "purpose": "Encode/decode Base64 strings.",
                     "usage": "Paste Base64 → click Decode.",
                     "notes": "Simple; good for quick email header or token decoding."},
                    {"name": "URL Decoder/Encoder", "url": "https://meyerweb.com/eric/tools/dencoder/",
                     "flags": [],
                     "purpose": "URL-encode or decode strings.",
                     "usage": "Paste string → click Decode or Encode.",
                     "notes": "Useful for decoding obfuscated URLs in phishing analysis."},
                    {"name": "DCode.fr", "url": "https://www.dcode.fr/en",
                     "flags": [],
                     "purpose": "Large collection of cipher tools — Caesar, ROT, substitution, etc.",
                     "usage": "Select cipher type → paste ciphertext → decode.",
                     "notes": "Useful for CTF and basic steganography challenges."},
                ],
                "subcategories": {}
            }
        }
    },
    "Network / OSINT Frameworks": {
        "desc": "All-in-one OSINT and recon frameworks.",
        "tools": [],
        "subcategories": {
            "Recon Frameworks": {
                "desc": "Automated multi-source intelligence gathering platforms.",
                "tools": [
                    {"name": "Maltego (R)", "url": "https://www.maltego.com",
                     "flags": ["R", "T"],
                     "purpose": "Visual link analysis and data mining platform.",
                     "usage": "Install → create graph → run transforms on entities (domain, email, person).",
                     "notes": "Industry standard for relationship mapping. Free Community Edition available."},
                    {"name": "SpiderFoot (T)", "url": "https://github.com/smicallef/spiderfoot",
                     "flags": ["T"],
                     "purpose": "OSINT automation framework — 200+ modules, web UI.",
                     "usage": "pip install spiderfoot\nspiderfoot -l 127.0.0.1:5001\nBrowse to UI → start scan.",
                     "notes": "One of the most comprehensive open-source OSINT tools."},
                    {"name": "Recon-ng (T)", "url": "https://github.com/lanmaster53/recon-ng",
                     "flags": ["T"],
                     "purpose": "Metasploit-style web recon framework with workspaces and modules.",
                     "usage": "python recon-ng\nworkspaces create <name>\nmarketplace install all\nmodules load <module>",
                     "notes": "Modular; integrates with APIs for email, domains, social data."},
                    {"name": "theHarvester (T)", "url": "https://github.com/laramies/theHarvester",
                     "flags": ["T"],
                     "purpose": "Gather emails, subdomains, hosts, IPs from public sources.",
                     "usage": "theHarvester -d example.com -b all",
                     "notes": "Pre-installed in Kali Linux. Essential first-pass recon tool."},
                    {"name": "OSINT Framework", "url": "https://osintframework.com",
                     "flags": [],
                     "purpose": "The original web-based directory of OSINT resources (this framework).",
                     "usage": "Browse tree → click tool node → follow link.",
                     "notes": "By @jnordine. Source: github.com/lockfale/osint-framework"},
                ],
                "subcategories": {}
            }
        }
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# FLAG RENDERING
# ─────────────────────────────────────────────────────────────────────────────
FLAG_LABELS = {
    "T": RED("[T] LOCAL INSTALL"),
    "D": YELLOW("[D] GOOGLE DORK"),
    "R": CYAN("[R] REGISTRATION"),
    "M": MAGENTA("[M] EDIT URL"),
}

FLAG_DESC = {
    "T": "Must be installed and run locally on your machine.",
    "D": "Uses a Google Dork (advanced search query).",
    "R": "Requires account registration.",
    "M": "The URL itself must be edited manually with your target.",
}


def flag_badge(flag: str) -> str:
    return FLAG_LABELS.get(flag, f"[{flag}]")


# ─────────────────────────────────────────────────────────────────────────────
# DISPLAY HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    lines = [
        BOLD(CYAN("╔══════════════════════════════════════════════════════════════╗")),
        BOLD(CYAN("║") + BOLD("        OSINT FRAMEWORK  —  Python CLI Replication             ") + BOLD(CYAN("║"))),
        BOLD(CYAN("║") + DIM("        Source: https://osintframework.com                     ") + BOLD(CYAN("║"))),
        BOLD(CYAN("╚══════════════════════════════════════════════════════════════╝")),
        "",
        f"  {RED('[T]')} Local Install    {YELLOW('[D]')} Google Dork    "
        f"{CYAN('[R]')} Registration    {MAGENTA('[M]')} Edit URL",
        "",
    ]
    print("\n".join(lines))


def print_tool(tool: dict, indent: int = 4) -> None:
    pad = " " * indent
    flags = "  ".join(flag_badge(f) for f in tool.get("flags", []))
    print(f"\n{pad}{GREEN('●')} {BOLD(tool['name'])}")
    if flags:
        print(f"{pad}  {flags}")
    print(f"{pad}  {DIM('URL    :')} {tool['url']}")
    print(f"{pad}  {DIM('Purpose:')} {tool['purpose']}")
    # Wrap usage to terminal width
    usage_lines = tool["usage"].split("\n")
    print(f"{pad}  {DIM('Usage  :')}", end="")
    for i, line in enumerate(usage_lines):
        prefix = f"\n{pad}           " if i > 0 else " "
        print(f"{prefix}{YELLOW(line)}", end="")
    print()
    if tool.get("notes"):
        print(f"{pad}  {DIM('Notes  :')} {tool['notes']}")


def print_tree_line(label: str, depth: int, is_last: bool, prefix: str = "") -> str:
    connector = "└── " if is_last else "├── "
    return f"{prefix}{connector}{label}"


# ─────────────────────────────────────────────────────────────────────────────
# TREE PRINTER (visual, like the website)
# ─────────────────────────────────────────────────────────────────────────────

def _render_tree(node: dict, prefix: str = "", is_last: bool = True) -> list[str]:
    lines = []
    connector = "└── " if is_last else "├── "
    child_prefix = prefix + ("    " if is_last else "│   ")

    subcats = node.get("subcategories") or {}
    tools   = node.get("tools") or []

    # Print sub-categories
    subcat_items = list(subcats.items())
    for i, (sub_name, sub_node) in enumerate(subcat_items):
        is_last_sub = (i == len(subcat_items) - 1) and not tools
        icon = "📁"
        lines.append(f"{prefix}{'└── ' if is_last_sub else '├── '}{icon} {BOLD(sub_name)}"
                     + DIM(f"  ({sub_node.get('desc','')})" if sub_node.get('desc') else ""))
        lines.extend(_render_tree(sub_node, child_prefix if not is_last_sub else prefix + "    ", True))

    # Print tools
    for j, tool in enumerate(tools):
        is_last_tool = (j == len(tools) - 1)
        flag_str = " ".join(f"({f})" for f in tool.get("flags", []))
        label = f"{tool['name']} {DIM(flag_str)}" if flag_str else tool["name"]
        lines.append(f"{child_prefix}{'└── ' if is_last_tool else '├── '}🔧 {label}")

    return lines


def show_full_tree():
    banner()
    print(BOLD("OSINT FRAMEWORK TREE\n"))
    top_items = list(FRAMEWORK.items())
    for i, (cat_name, cat_node) in enumerate(top_items):
        is_last = (i == len(top_items) - 1)
        connector = "└── " if is_last else "├── "
        child_prefix = "    " if is_last else "│   "
        print(f"{connector}{CYAN('📂')} {BOLD(CYAN(cat_name))}"
              + DIM(f"  — {cat_node.get('desc','')}"))
        lines = _render_tree(cat_node, child_prefix, True)
        for line in lines:
            print(line)
    print()


# ─────────────────────────────────────────────────────────────────────────────
# NAVIGATION
# ─────────────────────────────────────────────────────────────────────────────

def _collect_all_tools() -> list[dict]:
    """Flatten all tools into a list with their category path."""
    result = []
    def _walk(node: dict, path: list[str]):
        for t in node.get("tools", []):
            result.append({"tool": t, "path": path[:]})
        for sub_name, sub_node in (node.get("subcategories") or {}).items():
            _walk(sub_node, path + [sub_name])
    for cat_name, cat_node in FRAMEWORK.items():
        _walk(cat_node, [cat_name])
    return result


def query_framework(query: str):
    """Search all categories, subcategories, and tool names."""
    q = query.lower()
    results = []
    all_tools = _collect_all_tools()
    for entry in all_tools:
        path_str = " > ".join(entry["path"]).lower()
        tool = entry["tool"]
        if (q in tool["name"].lower() or
                q in path_str or
                q in tool.get("purpose", "").lower()):
            results.append(entry)

    if not results:
        print(f"\n{YELLOW('No results found for:')} {query}\n")
        return

    print(f"\n{GREEN('Results for:')} {BOLD(query)}  ({len(results)} tool(s) found)\n")
    for entry in results:
        path_display = " > ".join(entry["path"])
        print(f"  {DIM('Category:')} {CYAN(path_display)}")
        print_tool(entry["tool"])
        print()


def navigate_category(cat_name: str, cat_node: dict):
    """Drill into a top-level category."""
    while True:
        clear()
        banner()
        print(f"{BOLD(CYAN(cat_name))}\n{DIM(cat_node.get('desc',''))}\n")

        subcats  = list((cat_node.get("subcategories") or {}).items())
        top_tools = cat_node.get("tools") or []

        options = []
        for sub_name, sub_node in subcats:
            tool_count = len(sub_node.get("tools") or [])
            options.append(("subcategory", sub_name, sub_node, tool_count))

        for t in top_tools:
            options.append(("tool", t, None, 0))

        # Display options
        for idx, opt in enumerate(options, 1):
            if opt[0] == "subcategory":
                print(f"  {BOLD(str(idx)+'.')} {CYAN('📁')} {opt[1]}  "
                      + DIM(f"({opt[3]} tools)  {(opt[2] or {}).get('desc','')}"))
            else:
                t = opt[1]
                flags = " ".join(f"({f})" for f in t.get("flags",[]))
                print(f"  {BOLD(str(idx)+'.')} 🔧 {t['name']} {DIM(flags)}")

        print(f"\n  {BOLD('0.')} ← Back")
        choice = input(f"\n{BOLD('Select')} [0-{len(options)}]: ").strip()

        if choice == "0":
            break
        if not choice.isdigit() or not (1 <= int(choice) <= len(options)):
            continue

        selected = options[int(choice) - 1]

        if selected[0] == "subcategory":
            navigate_subcategory(selected[1], selected[2])
        else:
            clear()
            banner()
            print_tool(selected[1])
            action = input(f"\n  {BOLD('[O]')}pen in browser  {BOLD('[B]')}ack: ").strip().lower()
            if action == "o":
                webbrowser.open(selected[1]["url"])
            # loop back regardless


def navigate_subcategory(sub_name: str, sub_node: dict):
    """Drill into a subcategory and show its tools."""
    while True:
        clear()
        banner()
        print(f"{BOLD(CYAN(sub_name))}\n{DIM(sub_node.get('desc',''))}\n")

        tools = sub_node.get("tools") or []
        inner_subs = list((sub_node.get("subcategories") or {}).items())

        options = []
        for inner_sub_name, inner_sub_node in inner_subs:
            options.append(("subcategory", inner_sub_name, inner_sub_node))
        for t in tools:
            options.append(("tool", t, None))

        for idx, opt in enumerate(options, 1):
            if opt[0] == "subcategory":
                print(f"  {BOLD(str(idx)+'.')} {CYAN('📁')} {opt[1]}")
            else:
                t = opt[1]
                flags = " ".join(f"({f})" for f in t.get("flags", []))
                print(f"  {BOLD(str(idx)+'.')} 🔧 {t['name']}  {DIM(flags)}")

        print(f"\n  {BOLD('0.')} ← Back")
        choice = input(f"\n{BOLD('Select')} [0-{len(options)}]: ").strip()

        if choice == "0":
            break
        if not choice.isdigit() or not (1 <= int(choice) <= len(options)):
            continue

        selected = options[int(choice) - 1]
        if selected[0] == "subcategory":
            navigate_subcategory(selected[1], selected[2])
        else:
            clear()
            banner()
            print_tool(selected[1])
            action = input(f"\n  {BOLD('[O]')}pen in browser  {BOLD('[B]')}ack: ").strip().lower()
            if action == "o":
                webbrowser.open(selected[1]["url"])


# ─────────────────────────────────────────────────────────────────────────────
# EXPORT
# ─────────────────────────────────────────────────────────────────────────────

def export_json(filename: str = "osint_framework_export.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(FRAMEWORK, f, indent=2, ensure_ascii=False)
    print(f"{GREEN('Exported JSON:')} {filename}")


def export_csv(filename: str = "osint_framework_export.csv"):
    all_tools = _collect_all_tools()
    fieldnames = ["category_path", "name", "url", "flags", "purpose", "usage", "notes"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for entry in all_tools:
            t = entry["tool"]
            writer.writerow({
                "category_path": " > ".join(entry["path"]),
                "name": t["name"],
                "url": t["url"],
                "flags": ",".join(t.get("flags", [])),
                "purpose": t.get("purpose", ""),
                "usage": t.get("usage", "").replace("\n", " | "),
                "notes": t.get("notes", ""),
            })
    print(f"{GREEN('Exported CSV:')} {filename}")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN INTERACTIVE LOOP
# ─────────────────────────────────────────────────────────────────────────────

def main_menu():
    while True:
        clear()
        banner()
        cats = list(FRAMEWORK.items())
        print(BOLD("TOP-LEVEL CATEGORIES\n"))
        for i, (cat_name, cat_node) in enumerate(cats, 1):
            sub_count = len(cat_node.get("subcategories") or {})
            print(f"  {BOLD(str(i)+'.')} {CYAN('📂')} {cat_name}  "
                  + DIM(f"[{sub_count} subcategories]  {cat_node.get('desc','')}"))

        print(f"\n  {BOLD('T.')} Show Full Tree")
        print(f"  {BOLD('Q.')} Query / Search tools")
        print(f"  {BOLD('E.')} Export (JSON/CSV)")
        print(f"  {BOLD('X.')} Exit")

        choice = input(f"\n{BOLD('Select')} [1-{len(cats)}/T/Q/E/X]: ").strip().lower()

        if choice == "x":
            print(f"\n{DIM('Happy Hunting. Stay legal. Stay ethical.')}\n")
            sys.exit(0)
        elif choice == "t":
            clear()
            show_full_tree()
            input(f"{DIM('Press Enter to return...')}")
        elif choice == "q":
            q = input(f"\n{BOLD('Search query:')} ").strip()
            if q:
                clear()
                banner()
                query_framework(q)
                input(f"\n{DIM('Press Enter to return...')}")
        elif choice == "e":
            fmt = input(f"\n{BOLD('Format')} [json/csv]: ").strip().lower()
            if fmt == "json":
                export_json()
            elif fmt == "csv":
                export_csv()
            else:
                print(YELLOW("Unknown format. Use 'json' or 'csv'."))
            input(f"\n{DIM('Press Enter to return...')}")
        elif choice.isdigit() and 1 <= int(choice) <= len(cats):
            idx = int(choice) - 1
            navigate_category(cats[idx][0], cats[idx][1])


# ─────────────────────────────────────────────────────────────────────────────
# CLI ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def cli():
    parser = argparse.ArgumentParser(
        description="OSINT Framework — Python CLI Replication",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              python3 osint_framework.py
              python3 osint_framework.py --tree
              python3 osint_framework.py --query "email breach"
              python3 osint_framework.py --export json
              python3 osint_framework.py --export csv
              python3 osint_framework.py --list-categories
        """)
    )
    parser.add_argument("--tree",   action="store_true", help="Print the full OSINT Framework tree and exit.")
    parser.add_argument("--query",  metavar="TERM",       help="Search for tools matching TERM.")
    parser.add_argument("--export", choices=["json","csv"], help="Export framework data.")
    parser.add_argument("--list-categories", action="store_true", help="List all top-level categories.")
    args = parser.parse_args()

    if args.tree:
        show_full_tree()
        return
    if args.list_categories:
        banner()
        for i, cat in enumerate(FRAMEWORK, 1):
            print(f"  {i:2}. {cat}")
        return
    if args.query:
        banner()
        query_framework(args.query)
        return
    if args.export == "json":
        export_json()
        return
    if args.export == "csv":
        export_csv()
        return

    # Default: interactive
    main_menu()


if __name__ == "__main__":
    cli()
