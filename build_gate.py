#!/usr/bin/env python3
"""Combines three GATE HTML files into a single responsive GATE.html"""

import os

DIR = os.path.dirname(os.path.abspath(__file__))

# Read source files
def read(name):
    with open(os.path.join(DIR, name), 'r', encoding='utf-8') as f:
        return f.read()

file1 = read('gate_cs_master_topicwise_reference.html')
file2 = read('gate_cs_optimal_preparation_strategy.html')
file3 = read('gate_cs_youtube_channel_guide.html')

# Extract style blocks
def extract_style(html):
    styles = []
    rest = html
    while '<style>' in rest:
        start = rest.index('<style>') + 7
        end = rest.index('</style>')
        styles.append(rest[start:end].strip())
        rest = rest[:rest.index('<style>')] + rest[end+8:]
    return '\n'.join(styles), rest.strip()

# Extract script blocks
def extract_script(html):
    scripts = []
    rest = html
    while '<script>' in rest:
        start = rest.index('<script>') + 8
        end = rest.index('</script>')
        scripts.append(rest[start:end].strip())
        rest = rest[:rest.index('<script>')] + rest[end+9:]
    return '\n'.join(scripts), rest.strip()

style1, body1 = extract_style(file1)
style2, body2 = extract_style(file2)
style3, body3 = extract_style(file3)

script1, body1 = extract_script(body1)
script2, body2 = extract_script(body2)
script3, body3 = extract_script(body3)

# Rename conflicting classes between files
# File 1 uses: .root, .tip, .pills, .pill, .pnl, .tbl, .ot, .oa
# File 2 uses: .wrap, .tab, .sec, .tip, .card, .step, .scard, .ot
# File 3 uses: .root, .ftab, .card, .tip, .scard, .strategy, .ot

# We'll scope each section's content with unique wrapper classes
# and rename conflicting class names

# Prefix file1 classes to avoid conflicts
replacements_style1 = {
    '.root': '.s1-root',
    '.tip{': '.s1-tip{',
    '.tip ': '.s1-tip ',
}

replacements_body1 = {
    'class="root"': 'class="s1-root"',
}

# For tips in file1, they use inline style with --ac
# We need to be careful - tips in body1
body1 = body1.replace('class="tip"', 'class="s1-tip"')
style1 = style1.replace('.tip{', '.s1-tip{')

replacements_style2 = {
    '.wrap{': '.s2-wrap{',
    '.tab{': '.s2-tab{',
    '.tab.on{': '.s2-tab.on{',
    '.sec{': '.s2-sec{',
    '.sec.on{': '.s2-sec.on{',
    '.card{': '.s2-card{',
    '.card:last-child{': '.s2-card:last-child{',
    '.scard{': '.s2-scard{',
    '.tip{': '.s2-tip{',
    '.tip ': '.s2-tip ',
    '.ot{': '.s2-ot{',
}

body2 = body2.replace('class="wrap"', 'class="s2-wrap"')
body2 = body2.replace('class="tab ', 'class="s2-tab ')
body2 = body2.replace('class="tab"', 'class="s2-tab"')
body2 = body2.replace('class="sec ', 'class="s2-sec ')
body2 = body2.replace('class="sec"', 'class="s2-sec"')
body2 = body2.replace('class="card"', 'class="s2-card"')
body2 = body2.replace('class="scard"', 'class="s2-scard"')
body2 = body2.replace('class="tip ', 'class="s2-tip ')
body2 = body2.replace('class="tip"', 'class="s2-tip"')

for old, new in replacements_style2.items():
    style2 = style2.replace(old, new)

replacements_style3 = {
    '.root{': '.s3-root{',
    '.card{': '.s3-card{',
    '.card.open': '.s3-card.open',
    '.card-head{': '.s3-card-head{',
    '.card-body{': '.s3-card-body{',
    '.scard{': '.s3-scard{',
    '.tip{': '.s3-tip{',
}

body3 = body3.replace('class="root"', 'class="s3-root"')
body3 = body3.replace('class="card"', 'class="s3-card"')
body3 = body3.replace('class="card ', 'class="s3-card ')
body3 = body3.replace('class="scard ', 'class="s3-scard ')
body3 = body3.replace('class="tip"', 'class="s3-tip"')

for old, new in replacements_style3.items():
    style3 = style3.replace(old, new)

# Fix script references
script2 = script2.replace("'.sec'", "'.s2-sec'").replace("'.tab'", "'.s2-tab'")
script3 = script3.replace("'.card'", "'.s3-card'")

# Build the final HTML
html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GATE CS 2026 — Complete Preparation Guide</title>
  <meta name="description" content="Complete GATE CS 2026 preparation guide with topic-wise reference, optimal study strategy, and curated YouTube channel recommendations.">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* ===== GLOBAL RESET & DESIGN SYSTEM ===== */
    :root {{
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --color-background-primary: #ffffff;
      --color-background-secondary: #F7F7F5;
      --color-text-primary: #1a1a1a;
      --color-text-secondary: #6b6b6b;
      --color-text-tertiary: #999;
      --color-border-tertiary: #e5e5e3;
      --accent: #534AB7;
      --accent-bg: #EEEDFE;
    }}
    @media (prefers-color-scheme: dark) {{
      :root {{
        --color-background-primary: #1a1a1a;
        --color-background-secondary: #242424;
        --color-text-primary: #e8e8e8;
        --color-text-secondary: #a0a0a0;
        --color-text-tertiary: #777;
        --color-border-tertiary: #333;
      }}
    }}
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; font-size: 16px; }}
    body {{
      font-family: var(--font-sans);
      background: var(--color-background-secondary);
      color: var(--color-text-primary);
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
    }}

    /* ===== MAIN NAV ===== */
    .main-nav {{
      position: sticky; top: 0; z-index: 100;
      background: rgba(255,255,255,0.85);
      backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--color-border-tertiary);
      padding: 0;
    }}
    @media (prefers-color-scheme: dark) {{
      .main-nav {{ background: rgba(26,26,26,0.85); }}
    }}
    .nav-inner {{
      max-width: 960px; margin: 0 auto;
      display: flex; align-items: center; gap: 0.25rem;
      padding: 0.6rem 1.25rem;
      overflow-x: auto; -webkit-overflow-scrolling: touch;
    }}
    .nav-inner::-webkit-scrollbar {{ display: none; }}
    .main-btn {{
      padding: 0.5rem 1rem; border-radius: 10px;
      font-size: 0.8125rem; font-weight: 500; white-space: nowrap;
      cursor: pointer; border: 1.5px solid transparent;
      background: transparent; color: var(--color-text-secondary);
      transition: all 0.2s ease;
    }}
    .main-btn:hover {{ background: var(--color-background-secondary); }}
    .main-btn.active {{
      background: var(--accent-bg); color: var(--accent);
      border-color: var(--accent);
    }}

    /* ===== HERO ===== */
    .hero {{
      text-align: center;
      padding: 3rem 1.25rem 2rem;
      background: linear-gradient(135deg, #EEEDFE 0%, #E6F1FB 50%, #E1F5EE 100%);
    }}
    .hero h1 {{
      font-size: clamp(1.5rem, 4vw, 2.25rem);
      font-weight: 700; color: var(--color-text-primary);
      margin-bottom: 0.5rem;
    }}
    .hero p {{
      font-size: clamp(0.875rem, 2vw, 1rem);
      color: var(--color-text-secondary);
      max-width: 600px; margin: 0 auto;
    }}

    /* ===== SECTION CONTAINERS ===== */
    .main-section {{ display: none; }}
    .main-section.active {{ display: block; animation: fadeIn 0.25s ease; }}
    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    .section-wrap {{
      max-width: 960px; margin: 0 auto;
      padding: 1.5rem 1.25rem 3rem;
    }}
    .section-title {{
      font-size: clamp(1.125rem, 3vw, 1.5rem);
      font-weight: 600; margin-bottom: 0.25rem;
      color: var(--color-text-primary);
    }}
    .section-desc {{
      font-size: 0.875rem; color: var(--color-text-secondary);
      margin-bottom: 1.25rem;
    }}

    /* ===== RESPONSIVE ===== */
    @media (max-width: 640px) {{
      .nav-inner {{ padding: 0.5rem 0.75rem; }}
      .main-btn {{ padding: 0.4rem 0.75rem; font-size: 0.75rem; }}
      .section-wrap {{ padding: 1rem 0.75rem 2rem; }}
    }}

    /* ===== FILE 1 STYLES (Topic-wise Reference) ===== */
    {style1}

    /* ===== FILE 2 STYLES (Preparation Strategy) ===== */
    {style2}

    /* ===== FILE 3 STYLES (YouTube Guide) ===== */
    {style3}
  </style>
</head>
<body>

  <!-- HERO -->
  <header class="hero" id="top">
    <h1>GATE CS 2026 — Complete Guide</h1>
    <p>Topic-wise reference · Optimal preparation strategy · Curated YouTube channels — all in one place.</p>
  </header>

  <!-- MAIN NAVIGATION -->
  <nav class="main-nav" id="mainNav">
    <div class="nav-inner">
      <button class="main-btn active" onclick="switchMain(0)" id="navBtn0">📚 Topic Reference</button>
      <button class="main-btn" onclick="switchMain(1)" id="navBtn1">🎯 Prep Strategy</button>
      <button class="main-btn" onclick="switchMain(2)" id="navBtn2">▶ YouTube Guide</button>
    </div>
  </nav>

  <!-- SECTION 1: Topic-wise Reference -->
  <div class="main-section active" id="mainSec0">
    <div class="section-wrap">
      <h2 class="section-title">Master Topic-wise Reference</h2>
      <p class="section-desc">Detailed breakdown of all 11 GATE CS subjects — weightage, difficulty, time estimates, and insights.</p>
      {body1}
    </div>
  </div>

  <!-- SECTION 2: Preparation Strategy -->
  <div class="main-section" id="mainSec1">
    <div class="section-wrap">
      <h2 class="section-title">Optimal Preparation Strategy</h2>
      <p class="section-desc">Subject analysis, dependencies, study order, pairings, and alternative strategies.</p>
      {body2}
    </div>
  </div>

  <!-- SECTION 3: YouTube Channel Guide -->
  <div class="main-section" id="mainSec2">
    <div class="section-wrap">
      <h2 class="section-title">YouTube Channel Guide</h2>
      <p class="section-desc">Curated, ranked YouTube channels for every GATE CS subject — with playlist links.</p>
      {body3}
    </div>
  </div>

  <!-- FOOTER -->
  <footer style="text-align:center;padding:2rem 1rem;font-size:0.75rem;color:var(--color-text-tertiary);border-top:1px solid var(--color-border-tertiary);background:var(--color-background-primary);">
    GATE CS 2026 Preparation Guide · Built for focused, structured preparation.
  </footer>

  <script>
    /* === Main section switcher === */
    function switchMain(n) {{
      document.querySelectorAll('.main-section').forEach((s, i) => s.classList.toggle('active', i === n));
      document.querySelectorAll('.main-btn').forEach((b, i) => b.classList.toggle('active', i === n));
    }}

    /* === File 1: Subject pill switcher === */
    {script1}

    /* === File 2: Strategy tab switcher === */
    {script2}

    /* === File 3: Card toggle & filter === */
    {script3}
  </script>
</body>
</html>
'''

output_path = os.path.join(DIR, 'GATE.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ GATE.html created successfully at: {output_path}")
print(f"   File size: {os.path.getsize(output_path):,} bytes")
