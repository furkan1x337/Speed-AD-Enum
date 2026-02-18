#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Speed AD Enum Check - HTML Report Generator
Dark-themed, terminal-style interactive report.
"""

import os
import html


# ──────────────────────────────────────────────────
MODULE_FILES = [
    ("ASREPRoasting",       "ASREPRoasting/asrep.txt"),
    ("Bloodhound",          "Bloodhound/bloodhound_output.txt"),
    ("Signing False",       "Signing_false/all.txt"),
    ("SMB v1",              "SMBV1/all.txt"),
    ("Users Description",   "UsersDescription/users.txt"),
    ("GPP Password",        "gpp/gpp_pass.txt"),
    ("AD Password Policy",  "ADPassPol/passpol.txt"),
    ("Enum Trust",          "enum_trust/trust.txt"),
    ("SMB Shares (Unauth)", "smbshares/unauth.txt"),
    ("SMB Shares (Auth)",   "smbshares/auth.txt"),
    ("Pre2K",               "pre2k/cred.txt"),
    ("SCCM",                "sccm/sccm.txt"),
    ("LAPS",                "laps/laps.txt"),
    ("gMSA",                "gmsa/dumpgmsa.txt"),
    ("Entra ID",            "EntraId/entra.txt"),
    ("Kerberoasting",       "kerberos/hashes.txt"),
]


def _read_output(base_dir, rel_path):
    fpath = os.path.join(base_dir, rel_path)
    if os.path.isfile(fpath):
        with open(fpath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        return content if content.strip() else "[No output captured]"
    return "[Output file not found]"


def generate_report(base_dir, customer_name):

    module_data = []
    for name, rel_path in MODULE_FILES:
        content = _read_output(base_dir, rel_path)
        module_data.append((name, html.escape(content)))

    error_content = ""
    error_path = os.path.join(base_dir, "error.txt")
    if os.path.isfile(error_path):
        with open(error_path, "r", encoding="utf-8", errors="replace") as f:
            error_content = html.escape(f.read())

    # ───────────────────────────────────────────
    js_data_entries = []
    for idx, (name, escaped_content) in enumerate(module_data):
        safe_content = escaped_content.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
        js_data_entries.append(f'  {{ id: {idx}, name: `{name}`, content: `{safe_content}` }}')

    safe_error = error_content.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
    js_data_block = ",\n".join(js_data_entries)

    # ─────────────────────────────────────────────────
    button_items = []
    for idx, (name, _) in enumerate(module_data):
        button_items.append(
            f'<button class="module-btn" data-id="{idx}" onclick="showModule({idx})">'
            f'<span class="btn-icon">▸</span> {name}</button>'
        )
    if error_content:
        button_items.append(
            '<button class="module-btn error-btn" data-id="error" onclick="showErrors()">'
            '<span class="btn-icon">⚠</span> Error Log</button>'
        )
    buttons_html = "\n            ".join(button_items)

    # ────────────────────────────────────────────────
    report_html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Speed AD Enum Check — {html.escape(customer_name)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
/* ── Reset & Base ─────────────────────────────────────────────── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
  font-family: 'Inter', sans-serif;
  background: #0a0a0f;
  color: #c8cad0;
  min-height: 100vh;
  overflow-x: hidden;
}}

/* ── Animated Background ──────────────────────────────────────── */
body::before {{
  content: '';
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background:
    radial-gradient(ellipse 80% 50% at 20% 40%, rgba(0, 255, 163, 0.06) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 20%, rgba(0, 168, 255, 0.05) 0%, transparent 50%),
    radial-gradient(ellipse 50% 60% at 50% 80%, rgba(138, 43, 226, 0.04) 0%, transparent 50%);
  z-index: 0;
  pointer-events: none;
  animation: bgPulse 8s ease-in-out infinite alternate;
}}

@keyframes bgPulse {{
  0%   {{ opacity: 0.6; }}
  100% {{ opacity: 1; }}
}}

/* ── Grid Layout ──────────────────────────────────────────────── */
.app {{
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 280px 1fr;
  grid-template-rows: auto 1fr;
  min-height: 100vh;
}}

/* ── Header ───────────────────────────────────────────────────── */
.header {{
  grid-column: 1 / -1;
  text-align: center;
  padding: 40px 20px 30px;
  position: relative;
}}

.header h1 {{
  font-family: 'Orbitron', sans-serif;
  font-weight: 900;
  font-size: 2.6rem;
  background: linear-gradient(135deg, #00ffa3, #00a8ff, #8a2be2);
  background-size: 200% 200%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradientShift 4s ease-in-out infinite alternate;
  letter-spacing: 3px;
  text-shadow: 0 0 40px rgba(0, 255, 163, 0.15);
}}

@keyframes gradientShift {{
  0%   {{ background-position: 0% 50%; }}
  100% {{ background-position: 100% 50%; }}
}}

.header .subtitle {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  color: #4a5568;
  margin-top: 8px;
  letter-spacing: 2px;
}}

.header .client-badge {{
  display: inline-block;
  margin-top: 14px;
  padding: 6px 20px;
  border: 1px solid rgba(0, 255, 163, 0.25);
  border-radius: 20px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  color: #00ffa3;
  background: rgba(0, 255, 163, 0.05);
  backdrop-filter: blur(4px);
}}

.header::after {{
  content: '';
  position: absolute;
  bottom: 0; left: 10%; right: 10%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0, 255, 163, 0.3), rgba(0, 168, 255, 0.3), transparent);
}}

/* ── Sidebar ──────────────────────────────────────────────────── */
.sidebar {{
  background: rgba(12, 12, 20, 0.85);
  backdrop-filter: blur(16px);
  border-right: 1px solid rgba(255, 255, 255, 0.04);
  padding: 20px 12px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 6px;
}}

.sidebar-title {{
  font-family: 'Orbitron', sans-serif;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 3px;
  color: #4a5568;
  padding: 0 8px 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
  margin-bottom: 6px;
}}

.module-btn {{
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 11px 14px;
  border: 1px solid transparent;
  border-radius: 10px;
  background: transparent;
  color: #8892a4;
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  text-align: left;
}}

.module-btn:hover {{
  background: rgba(0, 255, 163, 0.06);
  border-color: rgba(0, 255, 163, 0.15);
  color: #c8cad0;
  transform: translateX(4px);
}}

.module-btn.active {{
  background: linear-gradient(135deg, rgba(0, 255, 163, 0.1), rgba(0, 168, 255, 0.08));
  border-color: rgba(0, 255, 163, 0.3);
  color: #00ffa3;
  box-shadow: 0 0 20px rgba(0, 255, 163, 0.08),
              inset 0 0 20px rgba(0, 255, 163, 0.03);
}}

.module-btn.active .btn-icon {{
  color: #00ffa3;
  text-shadow: 0 0 8px rgba(0, 255, 163, 0.5);
}}

.btn-icon {{
  font-size: 0.7rem;
  color: #4a5568;
  transition: all 0.25s;
  flex-shrink: 0;
}}

.error-btn {{ color: #ff6b6b !important; }}
.error-btn:hover {{ border-color: rgba(255, 107, 107, 0.3) !important; background: rgba(255, 107, 107, 0.06) !important; }}
.error-btn.active {{
  background: linear-gradient(135deg, rgba(255, 107, 107, 0.1), rgba(255, 50, 50, 0.08)) !important;
  border-color: rgba(255, 107, 107, 0.3) !important;
  color: #ff6b6b !important;
  box-shadow: 0 0 20px rgba(255, 107, 107, 0.08) !important;
}}

/* ── Main Content ─────────────────────────────────────────────── */
.main {{
  padding: 24px 30px;
  overflow-y: auto;
}}

/* ── Welcome Screen ───────────────────────────────────────────── */
.welcome {{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 70vh;
  text-align: center;
  animation: fadeInUp 0.6s ease-out;
}}

.welcome .logo-icon {{
  font-size: 4rem;
  margin-bottom: 20px;
  animation: pulse 2s ease-in-out infinite;
}}

@keyframes pulse {{
  0%, 100% {{ transform: scale(1); opacity: 0.8; }}
  50%      {{ transform: scale(1.05); opacity: 1; }}
}}

.welcome h2 {{
  font-family: 'Orbitron', sans-serif;
  font-size: 1.4rem;
  color: #4a5568;
  font-weight: 400;
  letter-spacing: 2px;
}}

.welcome p {{
  color: #2d3748;
  margin-top: 10px;
  font-size: 0.9rem;
}}

/* ── Terminal Panel ───────────────────────────────────────────── */
.terminal {{
  display: none;
  animation: fadeInUp 0.4s ease-out;
}}

.terminal.visible {{
  display: block;
}}

@keyframes fadeInUp {{
  from {{ opacity: 0; transform: translateY(12px); }}
  to   {{ opacity: 1; transform: translateY(0); }}
}}

.terminal-window {{
  background: rgba(10, 10, 18, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 14px;
  overflow: hidden;
  box-shadow:
    0 4px 30px rgba(0, 0, 0, 0.4),
    0 0 60px rgba(0, 255, 163, 0.03);
}}

.terminal-header {{
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 18px;
  background: rgba(20, 20, 32, 0.95);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}}

.terminal-dot {{
  width: 12px;
  height: 12px;
  border-radius: 50%;
}}

.terminal-dot.red    {{ background: #ff5f57; box-shadow: 0 0 6px rgba(255, 95, 87, 0.4); }}
.terminal-dot.yellow {{ background: #ffbd2e; box-shadow: 0 0 6px rgba(255, 189, 46, 0.4); }}
.terminal-dot.green  {{ background: #28c840; box-shadow: 0 0 6px rgba(40, 200, 64, 0.4); }}

.terminal-title {{
  flex: 1;
  text-align: center;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.78rem;
  color: #4a5568;
  letter-spacing: 1px;
}}

.terminal-body {{
  padding: 20px 22px;
  max-height: 72vh;
  overflow-y: auto;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.82rem;
  line-height: 1.7;
  color: #00ffa3;
  white-space: pre-wrap;
  word-break: break-all;
}}

.terminal-body.error-output {{
  color: #ff6b6b;
}}

/* Terminal scrollbar */
.terminal-body::-webkit-scrollbar {{
  width: 6px;
}}
.terminal-body::-webkit-scrollbar-track {{
  background: transparent;
}}
.terminal-body::-webkit-scrollbar-thumb {{
  background: rgba(0, 255, 163, 0.15);
  border-radius: 3px;
}}
.terminal-body::-webkit-scrollbar-thumb:hover {{
  background: rgba(0, 255, 163, 0.3);
}}

/* Sidebar scrollbar */
.sidebar::-webkit-scrollbar {{
  width: 4px;
}}
.sidebar::-webkit-scrollbar-track {{
  background: transparent;
}}
.sidebar::-webkit-scrollbar-thumb {{
  background: rgba(255, 255, 255, 0.06);
  border-radius: 2px;
}}

/* ── Prompt line ──────────────────────────────────────────────── */
.prompt {{
  color: #00a8ff;
}}

.prompt-symbol {{
  color: #8a2be2;
}}

/* ── Status Bar ───────────────────────────────────────────────── */
.status-bar {{
  margin-top: 16px;
  display: flex;
  gap: 20px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  color: #2d3748;
}}

.status-item {{
  display: flex;
  align-items: center;
  gap: 6px;
}}

.status-dot {{
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #00ffa3;
  box-shadow: 0 0 6px rgba(0, 255, 163, 0.4);
}}

/* ── Responsive ───────────────────────────────────────────────── */
@media (max-width: 768px) {{
  .app {{
    grid-template-columns: 1fr;
  }}
  .sidebar {{
    flex-direction: row;
    flex-wrap: wrap;
    border-right: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    padding: 10px;
    gap: 4px;
  }}
  .sidebar-title {{ display: none; }}
  .module-btn {{ width: auto; padding: 8px 12px; font-size: 0.75rem; }}
  .header h1 {{ font-size: 1.6rem; }}
}}
</style>
</head>
<body>
<div class="app">
  <!-- Header -->
  <header class="header">
    <h1>Speed AD Enum Check</h1>
    <div class="subtitle">// INTERNAL PENETRATION TESTING REPORT</div>
    <div class="client-badge">⚡ {html.escape(customer_name)}</div>
  </header>

  <!-- Sidebar -->
  <nav class="sidebar">
    <div class="sidebar-title">Modules</div>
    {buttons_html}
  </nav>

  <!-- Main Content -->
  <main class="main">
    <!-- Welcome -->
    <div class="welcome" id="welcome">
      <div class="logo-icon">🛡️</div>
      <h2>Select a Module</h2>
      <p>Select a module from the left panel to view the results.</p>
    </div>

    <!-- Terminal Output -->
    <div class="terminal" id="terminal">
      <div class="terminal-window">
        <div class="terminal-header">
          <div class="terminal-dot red"></div>
          <div class="terminal-dot yellow"></div>
          <div class="terminal-dot green"></div>
          <div class="terminal-title" id="terminalTitle">~ output</div>
        </div>
        <div class="terminal-body" id="terminalBody"></div>
      </div>
      <div class="status-bar">
        <div class="status-item">
          <div class="status-dot"></div>
          <span>nxc output</span>
        </div>
        <div class="status-item" id="lineCount"></div>
      </div>
    </div>
  </main>
</div>

<script>
// ── Module Data ──────────────────────────────────────────────────
const modules = [
{js_data_block}
];

const errorContent = `{safe_error}`;

// ── DOM references ───────────────────────────────────────────────
const welcomeEl     = document.getElementById('welcome');
const terminalEl    = document.getElementById('terminal');
const termBodyEl    = document.getElementById('terminalBody');
const termTitleEl   = document.getElementById('terminalTitle');
const lineCountEl   = document.getElementById('lineCount');
const allBtns       = document.querySelectorAll('.module-btn');

function clearActive() {{
  allBtns.forEach(b => b.classList.remove('active'));
}}

function showModule(id) {{
  const mod = modules[id];
  if (!mod) return;

  clearActive();
  const btn = document.querySelector(`.module-btn[data-id="${{id}}"]`);
  if (btn) btn.classList.add('active');

  welcomeEl.style.display = 'none';
  terminalEl.classList.add('visible');
  terminalEl.style.display = 'block';

  termTitleEl.textContent = `~ ${{mod.name}} // output`;
  termBodyEl.className = 'terminal-body';
  termBodyEl.textContent = '';

  // Typing effect
  typeContent(mod.content);
  const lines = mod.content.split('\\n').length;
  lineCountEl.textContent = `${{lines}} lines`;
}}

function showErrors() {{
  clearActive();
  const btn = document.querySelector('.error-btn');
  if (btn) btn.classList.add('active');

  welcomeEl.style.display = 'none';
  terminalEl.classList.add('visible');
  terminalEl.style.display = 'block';

  termTitleEl.textContent = '~ error.txt // log';
  termBodyEl.className = 'terminal-body error-output';
  termBodyEl.textContent = '';

  typeContent(errorContent);
  const lines = errorContent.split('\\n').length;
  lineCountEl.textContent = `${{lines}} lines`;
}}

// ── Typing Animation ─────────────────────────────────────────────
let typingTimer = null;
function typeContent(text) {{
  if (typingTimer) clearInterval(typingTimer);

  const lines = text.split('\\n');
  let currentLine = 0;
  termBodyEl.textContent = '';

  if (lines.length > 200) {{
    // Çok uzun çıktılarda animasyon atla
    termBodyEl.textContent = text;
    return;
  }}

  typingTimer = setInterval(() => {{
    if (currentLine >= lines.length) {{
      clearInterval(typingTimer);
      typingTimer = null;
      return;
    }}
    termBodyEl.textContent += (currentLine > 0 ? '\\n' : '') + lines[currentLine];
    currentLine++;
    termBodyEl.scrollTop = termBodyEl.scrollHeight;
  }}, 30);
}}
</script>
</body>
</html>"""

    report_path = os.path.join(base_dir, "report.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_html)
