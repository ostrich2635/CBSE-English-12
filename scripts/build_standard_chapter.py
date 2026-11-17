"""
scripts/build_standard_chapter.py
Canonical assembly and verification engine for CBSE Class 12 English study manuals.
Enforces 100% compliance with the Going Places (CH-08) format specification.
"""

import os
import re
import json
import subprocess
from bs4 import BeautifulSoup

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPTS_DIR)
MASTER_CSS_PATH = os.path.join(SCRIPTS_DIR, 'master_style.css')

CHROME_PATHS = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
]

def get_chrome_executable():
    for p in CHROME_PATHS:
        if os.path.exists(p):
            return p
    raise FileNotFoundError("Google Chrome executable not found for PDF compilation.")

def wrap_text_tokens(text):
    tokens = re.split(r'(\b[a-zA-Z0-9_\'-]+\b)', text)
    out = []
    for t in tokens:
        if re.match(r'^[a-zA-Z0-9_\'-]+$', t) and any(c.isalpha() for c in t):
            clean = t.lower()
            out.append(f'<span class="vw" data-w="{clean}">{t}</span>')
        else:
            out.append(t)
    return "".join(out)

def compile_chapter_pdf(html_path, pdf_path):
    chrome_exe = get_chrome_executable()
    abs_html = os.path.abspath(html_path)
    abs_pdf = os.path.abspath(pdf_path)
    url = f"file:///{abs_html.replace(os.sep, '/')}"

    if os.path.exists(abs_pdf):
        os.remove(abs_pdf)

    cmd = [
        chrome_exe,
        '--headless=new',
        '--disable-gpu',
        f'--print-to-pdf={abs_pdf}',
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(abs_pdf):
        size = os.path.getsize(abs_pdf)
        print(f"✓ Successfully compiled vector PDF: {pdf_path} ({size:,} bytes)")
        return True
    else:
        print(f"✗ Failed to compile PDF: {res.stderr}")
        return False
