#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Speed AD Enum Check - Internal Penetration Testing Automation Tool
Runs 15 security checks using netexec (nxc) and generates an HTML report.
"""

import os
import sys
import traceback
from datetime import datetime

from modules import asreproasting
from modules import bloodhound
from modules import signing_false
from modules import smbv1
from modules import users_description
from modules import gpp
from modules import ad_pass_pol
from modules import enum_trust
from modules import smb_shares
from modules import pre2k
from modules import sccm
from modules import laps
from modules import gmsa
from modules import entra_id
from modules import kerberoasting
from report_generator import generate_report


# ────────────────────────────────────────────────
class Colors:
    HEADER  = "\033[95m"
    BLUE    = "\033[94m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    BOLD    = "\033[1m"
    RESET   = "\033[0m"


BANNER = f"""
{Colors.CYAN}{Colors.BOLD}
  ███████╗██████╗ ███████╗███████╗██████╗      █████╗ ██████╗ 
  ██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗    ██╔══██╗██╔══██╗
  ███████╗██████╔╝█████╗  █████╗  ██║  ██║    ███████║██║  ██║
  ╚════██║██╔═══╝ ██╔══╝  ██╔══╝  ██║  ██║    ██╔══██║██║  ██║
  ███████║██║     ███████╗███████╗██████╔╝    ██║  ██║██████╔╝
  ╚══════╝╚═╝     ╚══════╝╚══════╝╚═════╝     ╚═╝  ╚═╝╚═════╝ 
{Colors.RESET}
{Colors.YELLOW}          ⚡ Speed AD Enum Check Tool ⚡{Colors.RESET}
{Colors.BLUE}       Internal Penetration Testing Automation{Colors.RESET}
"""

# ────────────────────────────────────────────────────────
MODULES = [
    ("ASREPRoasting",        asreproasting),
    ("Bloodhound",           bloodhound),
    ("Signing False",        signing_false),
    ("SMB v1",               smbv1),
    ("Users Description",    users_description),
    ("GPP Password",         gpp),
    ("AD Password Policy",   ad_pass_pol),
    ("Enum Trust",           enum_trust),
    ("SMB Shares",           smb_shares),
    ("Pre2K",                pre2k),
    ("SCCM",                 sccm),
    ("LAPS",                 laps),
    ("gMSA",                 gmsa),
    ("Entra ID",             entra_id),
    ("Kerberoasting",        kerberoasting),
]


def get_user_input():
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'═' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}  Please enter the following information:{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'═' * 60}{Colors.RESET}\n")

    customer_name = input(f"  {Colors.GREEN}[?]{Colors.RESET} Customer Name         : ").strip()
    dc_ip        = input(f"  {Colors.GREEN}[?]{Colors.RESET} DC IP Adress          : ").strip()
    target_file  = input(f"  {Colors.GREEN}[?]{Colors.RESET} Target VLANs (txt)    : ").strip()
    username     = input(f"  {Colors.GREEN}[?]{Colors.RESET} Domain User Username  : ").strip()
    password     = input(f"  {Colors.GREEN}[?]{Colors.RESET} Domain User Password  : ").strip()

    if not all([customer_name, dc_ip, target_file, username, password]):
        print(f"\n  {Colors.RED}[!] All fields must be filled in!{Colors.RESET}")
        sys.exit(1)

    if not os.path.isfile(target_file):
        print(f"\n  {Colors.RED}[!] Target VLANs file not found: {target_file}{Colors.RESET}")
        sys.exit(1)

    return customer_name, dc_ip, target_file, username, password


def log_error(base_dir, module_name, error_msg):
    error_file = os.path.join(base_dir, "error.txt")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(error_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [{module_name}] {error_msg}\n")


def main():
    print(BANNER)

    customer_name, dc_ip, target_file, username, password = get_user_input()

    base_dir = os.path.join(os.getcwd(), customer_name)
    os.makedirs(base_dir, exist_ok=True)

    print(f"\n{Colors.BOLD}{Colors.CYAN}{'═' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}  Scanning is starting — {customer_name}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'═' * 60}{Colors.RESET}\n")

    total = len(MODULES)
    completed = 0
    failed = 0

    for idx, (name, module) in enumerate(MODULES, 1):
        progress = f"[{idx}/{total}]"
        print(f"  {Colors.YELLOW}⏳ {progress} [{name} Checking...]{Colors.RESET}", flush=True)

        try:
            module.run(base_dir, dc_ip, target_file, username, password)
            completed += 1
            print(f"  {Colors.GREEN}✅ {progress} [{name} Check Completed]{Colors.RESET}\n", flush=True)
        except Exception as e:
            failed += 1
            error_detail = f"{str(e)}\n{traceback.format_exc()}"
            log_error(base_dir, name, error_detail)
            print(f"  {Colors.RED}❌ {progress} [{name} Check Failed — error is error.txt'ye kaydedildi]{Colors.RESET}\n", flush=True)

    # ──────────────────────────────────────────────────────
    print(f"{Colors.BOLD}{Colors.CYAN}{'═' * 60}{Colors.RESET}")
    print(f"  {Colors.YELLOW}📄 HTML report is being generated...{Colors.RESET}")

    try:
        generate_report(base_dir, customer_name)
        print(f"  {Colors.GREEN}✅ The report has been created: {customer_name}/report.html{Colors.RESET}")
    except Exception as e:
        log_error(base_dir, "ReportGenerator", str(e))
        print(f"  {Colors.RED}❌ An error occurred while generating the report!{Colors.RESET}")

    # ───────────────────────────────────────────────────────────────
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'═' * 60}{Colors.RESET}")
    print(f"  {Colors.BOLD}{Colors.GREEN}✅ Completed : {completed}/{total}{Colors.RESET}")
    if failed > 0:
        print(f"  {Colors.BOLD}{Colors.RED}❌ Failure   : {failed}/{total}{Colors.RESET}")
    print(f"  {Colors.BOLD}{Colors.BLUE}📁 Output Index: {base_dir}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'═' * 60}{Colors.RESET}\n")


if __name__ == "__main__":
    main()
