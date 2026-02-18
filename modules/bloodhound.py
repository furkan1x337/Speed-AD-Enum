#!/usr/bin/env python3
"""Module 2 - Bloodhound Collection Enumeration"""

import os
import subprocess


def run(base_dir, dc_ip, target_file, username, password):
    out_dir = os.path.join(base_dir, "Bloodhound")
    os.makedirs(out_dir, exist_ok=True)

    cmd = [
        "nxc", "ldap", dc_ip,
        "-u", username,
        "-p", password,
        "--bloodhound",
        "--dns-server", dc_ip,
        "--collection", "All",
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=600,
        cwd=out_dir
    )

    log_file = os.path.join(out_dir, "bloodhound_output.txt")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(result.stdout + result.stderr)

    if result.returncode != 0:
        raise RuntimeError(
            f"nxc exited with code {result.returncode}\n{result.stderr}"
        )

    return out_dir
