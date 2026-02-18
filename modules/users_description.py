#!/usr/bin/env python3
"""Module 5 - Domain Users Description Enumeration"""

import os
import subprocess
import re


def run(base_dir, dc_ip, target_file, username, password):
    out_dir = os.path.join(base_dir, "UsersDescription")
    os.makedirs(out_dir, exist_ok=True)

    cmd = [
        "nxc", "smb", dc_ip,
        "-u", username,
        "-p", password,
        "--users",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    output = result.stdout + result.stderr

    users_file = os.path.join(out_dir, "users.txt")
    with open(users_file, "w", encoding="utf-8") as f:
        f.write(output)

    usernames = []
    flag = False
    for line in output.splitlines():
        if "-Username-" in line:
            flag = True
            continue
        if flag:
            parts = line.split()
            if len(parts) >= 5:
                usernames.append(parts[4])

    all_users_file = os.path.join(out_dir, "allusernames.txt")
    with open(all_users_file, "w", encoding="utf-8") as f:
        f.write("\n".join(usernames) + "\n" if usernames else "")

    if result.returncode != 0 and not output.strip():
        raise RuntimeError(f"nxc exited with code {result.returncode}")
