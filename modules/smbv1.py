#!/usr/bin/env python3
"""Module 4 - SMB v1 Usage Detection"""

import os
import subprocess


def run(base_dir, dc_ip, target_file, username, password):
    out_dir = os.path.join(base_dir, "SMBV1")
    os.makedirs(out_dir, exist_ok=True)

    cmd = ["nxc", "smb", target_file]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    output = result.stdout + result.stderr

    all_lines = []
    ip_lines = []
    for line in output.splitlines():
        if "SMBv1:True" in line:
            all_lines.append(line)
            parts = line.split()
            if len(parts) >= 2:
                ip_lines.append(parts[1])

    all_file = os.path.join(out_dir, "all.txt")
    with open(all_file, "w", encoding="utf-8") as f:
        f.write("\n".join(all_lines) + "\n" if all_lines else "")

    ips_file = os.path.join(out_dir, "ips.txt")
    with open(ips_file, "w", encoding="utf-8") as f:
        f.write("\n".join(ip_lines) + "\n" if ip_lines else "")

    if result.returncode != 0 and not output.strip():
        raise RuntimeError(f"nxc exited with code {result.returncode}")
