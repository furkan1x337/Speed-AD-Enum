<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/NetExec-nxc-00ffa3?style=for-the-badge&logo=gnu-bash&logoColor=white" alt="NetExec">
  <img src="https://img.shields.io/badge/Platform-Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux">
  <img src="https://img.shields.io/badge/license-%20%20GNU%20GPLv3%20-green?style=for-the-badge" alt="License">
</p>

<h1 align="center">
  ⚡ Speed AD Enum Check
</h1>

<p align="center">
  <b>Internal Penetration Testing Automation Tool</b><br>
  <sub>Fast and comprehensive security auditing for Active Directory environments</sub>
</p>

---

## 📋 Table of Contents

- [🎯 About](#-about)
- [✨ Features](#-features)
- [🛡️ Security Modules](#️-security-modules)
- [⚙️ Requirements](#️-requirements)
- [🚀 Installation](#-installation)
- [💻 Usage](#-usage)
- [📊 Report Output](#-report-output)
- [📁 Project Structure](#-project-structure)
- [⚠️ Disclaimer](#️-disclaimer)

---

## 🎯 About

**Speed AD Enum Check** is an automation tool designed to quickly scan Active Directory environments and identify security vulnerabilities during internal penetration tests.

The tool automatically runs **15 different security checks** using **netexec (nxc)** and presents the results as a sleek, dark-themed, interactive **HTML report**.

> With a **single command**, you can launch all checks using domain user credentials and a target VLAN file.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔄 **15 Automated Checks** | Scans critical AD security vulnerabilities in a single run |
| 📊 **Interactive HTML Report** | Dark-themed, terminal-style report with typing animations |
| 🎯 **Modular Architecture** | Each check runs as an independent module |
| 🛡️ **Error Handling** | Failed modules don't affect others; errors are logged to `error.txt` |
| 🎨 **Colorful Console Output** | Progress and results are displayed with colored terminal output |
| 📁 **Organized Outputs** | Each module's output is stored in its own directory |

---

## 🛡️ Security Modules

<table>
  <tr>
    <th>#</th>
    <th>Module</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>1</td>
    <td><b>ASREPRoasting</b></td>
    <td>Identifies accounts with Kerberos pre-authentication disabled</td>
  </tr>
  <tr>
    <td>2</td>
    <td><b>Kerberoasting</b></td>
    <td>Extracts TGS hashes for SPN-assigned service accounts</td>
  </tr>
  <tr>
    <td>3</td>
    <td><b>Bloodhound</b></td>
    <td>Collects AD relationship data for BloodHound ingestion</td>
  </tr>
  <tr>
    <td>4</td>
    <td><b>SMB Signing</b></td>
    <td>Detects systems with SMB signing disabled (relay attack surface)</td>
  </tr>
  <tr>
    <td>5</td>
    <td><b>SMBv1</b></td>
    <td>Finds systems running the insecure SMBv1 protocol</td>
  </tr>
  <tr>
    <td>6</td>
    <td><b>Users Description</b></td>
    <td>Searches user description fields for sensitive information</td>
  </tr>
  <tr>
    <td>7</td>
    <td><b>GPP Password</b></td>
    <td>Checks for credentials stored in Group Policy Preferences</td>
  </tr>
  <tr>
    <td>8</td>
    <td><b>AD Password Policy</b></td>
    <td>Queries and displays the domain password policy</td>
  </tr>
  <tr>
    <td>9</td>
    <td><b>Enum Trust</b></td>
    <td>Enumerates domain trust relationships</td>
  </tr>
  <tr>
    <td>10</td>
    <td><b>SMB Shares</b></td>
    <td>Scans for accessible SMB shares (authenticated & unauthenticated)</td>
  </tr>
  <tr>
    <td>11</td>
    <td><b>Pre2K</b></td>
    <td>Identifies Pre-Windows 2000 compatible accounts</td>
  </tr>
  <tr>
    <td>12</td>
    <td><b>SCCM</b></td>
    <td>Gathers SCCM/MECM configuration information</td>
  </tr>
  <tr>
    <td>13</td>
    <td><b>LAPS</b></td>
    <td>Queries Local Administrator Password Solution data</td>
  </tr>
  <tr>
    <td>14</td>
    <td><b>gMSA</b></td>
    <td>Dumps Group Managed Service Account passwords</td>
  </tr>
  <tr>
    <td>15</td>
    <td><b>Entra ID</b></td>
    <td>Collects Azure Entra ID (formerly Azure AD) information</td>
  </tr>
</table>

---

## ⚙️ Requirements

- **Python** 3.8+
- **NetExec (nxc)** — must be installed and accessible in `PATH`
- A valid **domain user account** (username & password)
- A **target file** (`.txt`) containing target VLANs/subnets

### Installing NetExec

```bash
# Recommended: install via pipx
pipx install netexec

# Or via pip
pip install netexec
```

---

## 🚀 Installation

```bash
# 1. Clone the repository
git clone https://github.com/USERNAME/Speed-AD-Enum-Check.git

# 2. Navigate to the directory
cd Speed-AD-Enum-Check

# 3. Run the tool
python3 main.py
```

---

## 💻 Usage

After launching the tool, you will be prompted for the following information interactively:

```
  ███████╗██████╗ ███████╗███████╗██████╗      █████╗ ██████╗
  ██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗    ██╔══██╗██╔══██╗
  ███████╗██████╔╝█████╗  █████╗  ██║  ██║    ███████║██║  ██║
  ╚════██║██╔═══╝ ██╔══╝  ██╔══╝  ██║  ██║    ██╔══██║██║  ██║
  ███████║██║     ███████╗███████╗██████╔╝    ██║  ██║██████╔╝
  ╚══════╝╚═╝     ╚══════╝╚══════╝╚═════╝     ╚═╝  ╚═╝╚═════╝

          ⚡ Speed AD Enum Check Tool ⚡
       Internal Penetration Testing Automation

  [?] Client Name            : AcmeCorp
  [?] DC IP Address          : 10.10.10.1
  [?] Target VLANs (txt)     : targets.txt
  [?] Domain User Username   : pentest.user
  [?] Domain User Password   : P@ssw0rd!
```

| Parameter | Description |
|-----------|-------------|
| **Client Name** | Used for the output directory name and report title |
| **DC IP Address** | IP address of the Domain Controller |
| **Target VLANs** | Path to a `.txt` file containing target IPs/subnets |
| **Username** | Domain user account username |
| **Password** | Domain user account password |

---

## 📊 Report Output

Once all scans are completed, the tool automatically generates an **interactive HTML report**.

### Report Features

- 🌙 **Dark theme** — terminal-style, eye-friendly design
- ⌨️ **Typing animation** — outputs are displayed with a terminal typing effect
- 📂 **Sidebar navigation** — easily switch between module results
- 📱 **Responsive design** — works on both mobile and desktop
- ⚠️ **Error log panel** — view error logs for failed modules

### Output Directory Structure


---

## 📁 Project Structure

```
Speed-AD-Enum-Check/
├── main.py                  # Main application entry point
├── report_generator.py      # HTML report generator
├── README.md
└── modules/
    ├── __init__.py
    ├── asreproasting.py     # ASREPRoasting check
    ├── kerberoasting.py     # Kerberoasting check
    ├── bloodhound.py        # Bloodhound collection
    ├── signing_false.py     # SMB Signing check
    ├── smbv1.py             # SMBv1 detection
    ├── users_description.py # User description scan
    ├── gpp.py               # GPP Password check
    ├── ad_pass_pol.py       # Password policy query
    ├── enum_trust.py        # Trust relationships
    ├── smb_shares.py        # SMB share enumeration
    ├── pre2k.py             # Pre-Windows 2000 check
    ├── sccm.py              # SCCM discovery
    ├── laps.py              # LAPS query
    ├── gmsa.py              # gMSA dump
    └── entra_id.py          # Entra ID check
```

---

## ⚠️ Disclaimer

> **⚠️ IMPORTANT: This tool is intended for authorized security assessments only.**
>
> - Use **only** on systems where you have **written permission**
> - **Unauthorized access** is illegal and may result in severe legal consequences
> - The **user is solely responsible** for any misuse of this tool
> - This tool is built for **professional penetration testers**

---

<p align="center">
  <sub>Made with ⚡ for penetration testers</sub><br>
  <sub>Speed AD Enum Check © 2025</sub>
</p>
