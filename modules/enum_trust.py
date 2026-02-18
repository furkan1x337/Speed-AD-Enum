#!/usr/bin/env python3
"""Module 8 - Enumerate Domain Trusts"""

import os
import subprocess


def run(base_dir, dc_ip, target_file, username, password):
    out_dir = os.path.join(base_dir, "enum_trust")
    os.makedirs(out_dir, exist_ok=True)

    cmd = [
        "nxc", "ldap", dc_ip,
        "-u", username,
        "-p", password,
        "--dc-list",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    output = result.stdout + result.stderr

    out_file = os.path.join(out_dir, "trust.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(output)

    if result.returncode != 0 and not output.strip():
        raise RuntimeError(f"nxc exited with code {result.returncode}")
