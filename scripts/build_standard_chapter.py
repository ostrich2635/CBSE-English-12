"""
scripts/build_standard_chapter.py
Canonical assembly, verification, and PDF compilation engine for CBSE Class 12 English study manuals.
Enforces 100% compliance with the Going Places (CH-08) benchmark specification.
"""

import os
import re
import json
import subprocess
from bs4 import BeautifulSoup
import pypdf

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPTS_DIR)
MASTER_CSS_PATH = os.path.join(SCRIPTS_DIR, 'master_style.css')
GP_BENCHMARK_PATH = os.path.join(ROOT_DIR, 'HTML', 'going_places_cbse_mastery.html')

CHROME_PATHS = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
]

def get_chrome_executable():
    for p in CHROME_PATHS:
        if os.path.exists(p):
            return p
    raise FileNotFoundError("Google Chrome executable not found for PDF compilation.")

# Canonical 15 checks against Going Places benchmark
BENCHMARK_CHECKS = [
    ('mono_kicker', r'<div class="mono-kicker">MANUAL // CBSE CLASS 12 ENGLISH CORE \(FLAMINGO\) // CH-\d+</div>'),
    ('doc_specs_pill', r'<div class="doc-specs">\s*<span class="spec-pill">SYLLABUS: 2026–27</span>'),
    ('toc_box', r'<nav class="toc-box">\s*<div class="toc-title">\s*<span>INDEX // QUICK NAVIGATION</span>'),
    ('section_headers', r'<h2 class="section-header">01\. Executive Exam Compass &amp; Themes</h2>'),
    ('passage_headline', r'<div class="passage-headline">Passage 1:'),
    ('quote_passage', r'<div class="quote-passage">\s*<span class="quote-label">ORIGINAL VERBATIM TEXT</span>'),
    ('sub_module_vocab', r'<div class="sub-module">\s*<div class="sub-label">\[ VOCABULARY &amp; PHRASES \]</div>'),
    ('sub_module_devices', r'<div class="sub-module">\s*<div class="sub-label">\[ LITERARY &amp; STYLISTIC DEVICES \]</div>'),
    ('sub_module_analysis', r'<div class="sub-module">\s*<div class="sub-label">\[ LITERARY &amp; PSYCHOLOGICAL ANALYSIS \]</div>'),
    ('exam_value_box', r'<div class="exam-value-box">\s*<div class="sub-label"[^>]*>\[ CBSE EXAM VALUE POINTS &amp; RTC \]</div>'),
    ('keyword_cloud', r'<div class="keyword-cloud">'),
    ('qa_card', r'<div class="qa-card">\s*<div class="qa-card-meta">'),
    ('qa_card_vp', r'<div class="qa-card-vp"><strong>(?:CBSE\s+)?(?:<span[^>]*>)?Value(?:</span>)?\s+(?:<span[^>]*>)?Points(?:</span>)?:</strong>'),
    ('floating_controls', r'<div class="floating-controls" id="floating-controls">\s*<button[^>]*id="theme-toggle"'),
    ('vocab_tooltip', r'<div id="vocab-tooltip">\s*<div class="tt-header">'),
]

def verify_html_against_benchmark(html_path):
    """
    Verifies that an HTML manual strictly matches the Going Places benchmark standard.
    Returns (True, []) if all 15 tests pass, or (False, failed_tests) if any fail.
    """
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    failed = []
    for name, pattern in BENCHMARK_CHECKS:
        if not re.search(pattern, html):
            failed.append(name)

    if failed:
        print(f"[FAIL] Benchmark verification failed for {html_path}: {failed}")
        return False, failed
    
    print(f"[PASS] 15/15 Benchmark verification checks passed for {html_path}!")
    return True, []

def compile_chapter_pdf(html_path, pdf_path):
    """
    Compiles an HTML study manual to vector PDF via headless Chrome.
    """
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
        '--run-all-compositor-stages-before-draw',
        f'--print-to-pdf={abs_pdf}',
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(abs_pdf):
        size = os.path.getsize(abs_pdf)
        r = pypdf.PdfReader(abs_pdf)
        print(f"✓ Successfully compiled vector PDF: {pdf_path} ({len(r.pages)} pages, {size:,} bytes)")
        return True
    else:
        print(f"✗ Failed to compile PDF: {res.stderr}")
        return False
