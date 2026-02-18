#!/usr/bin/env python3
"""Module 9 - SMB Shares Enumeration (Unauth + Auth)"""

import os
import subprocess


def run(base_dir, dc_ip, target_file, username, password):
    out_dir = os.path.join(base_dir, "smbshares")
    os.makedirs(out_dir, exist_ok=True)

    # ── 1) Unauthenticated share enumeration ────────────────────
    cmd_unauth = [
        "nxc", "smb", target_file,
        "-u", "",
        "-p", "",
        "--shares",
    ]

    result_unauth = subprocess.run(cmd_unauth, capture_output=True, text=True, timeout=600)
    output_unauth = result_unauth.stdout + result_unauth.stderr

    unauth_file = os.path.join(out_dir, "unauth.txt")
    with open(unauth_file, "w", encoding="utf-8") as f:
        f.write(output_unauth)

    # ── 2) Authenticated share enumeration ──────────────────────
    cmd_auth = [
        "nxc", "smb", target_file,
        "-u", username,
        "-p", password,
        "--shares",
    ]

    result_auth = subprocess.run(cmd_auth, capture_output=True, text=True, timeout=600)
    output_auth = result_auth.stdout + result_auth.stderr

    auth_file = os.path.join(out_dir, "auth.txt")
    with open(auth_file, "w", encoding="utf-8") as f:
        f.write(output_auth)

    if (result_unauth.returncode != 0 and not output_unauth.strip()) and \
       (result_auth.returncode != 0 and not output_auth.strip()):
        raise RuntimeError("Both unauth and auth share scans failed")
