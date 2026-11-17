# CBSE English 12 — Standard Study Manual Formatting Specification
> **Ground Truth & Reference Anchor**: [Going Places (CH-08)](file:///c:/Users/aishw/Downloads/CBSE%20Eng/HTML/going_places_cbse_mastery.html) and [Going Places PDF](file:///c:/Users/aishw/Downloads/CBSE%20Eng/PDF/Going_Places_CBSE_Guide.pdf).
> **Rule**: Under NO circumstances may the layout, DOM IDs, typography, or styling deviate from this specification in any existing or upcoming chapter.

---

## 1. Document Architecture & Head Hierarchy

### Head Elements (Mandatory Sequence)
```html
<!DOCTYPE html>
<html lang="en">
<head>
<script>
(function() {
  const saved = localStorage.getItem('cbse_theme');
  if (saved === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
  } else {
    document.documentElement.setAttribute('data-theme', 'light');
  }
})();
</script>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0, maximum-scale=5.0" name="viewport"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Google+Sans:ital,opsz,wght@0,14..32,400..700;1,14..32,400..700&amp;display=swap" rel="stylesheet"/>
<title>{Chapter Title} — {Author} | CBSE Class 12 English Study Manual</title>
<style>
/* Exact 12,936-byte Master Stylesheet from scripts/master_style.css */
</style>
</head>
```

---

## 2. Body Structure & Top-Level Containers

```html
<body>
<div class="container" id="top">
  <!-- 1. Header -->
  <!-- 2. Table of Contents -->
  <!-- 3. Section #overview -->
  <!-- 4. Section #keywords -->
  <!-- 5. Section #passages -->
  <!-- 6. Section #characters -->
  <!-- 7. Section #rtc -->
  <!-- 8. Section #short-qa -->
  <!-- 9. Section #long-qa -->
  <!-- 10. Section #pyq-vault -->
  <!-- 11. Footer -->
</div>

<!-- Floating Controls (OUTSIDE #top container, before scripts) -->
<div class="floating-controls" id="floating-controls">
  <button aria-label="Toggle theme" class="floating-btn" id="theme-toggle" title="Toggle Light/Dark Theme">[ ☾ DARK ]</button>
  <a class="floating-btn back-top-btn" href="#top" title="Scroll to top">↑ TOP</a>
</div>

<!-- Tooltip Element -->
<div id="vocab-tooltip">
  <div class="tt-header">
    <span class="tt-word" id="tt-word-el"></span>
    <div class="tt-meta">
      <span class="tt-pos" id="tt-pos-el"></span>
      <span class="tt-cycle-badge" id="tt-cycle-btn" title="Click to see another meaning">1 of 1 ↻</span>
    </div>
  </div>
  <div class="tt-def" id="tt-def-el"></div>
</div>

<script>
/* Master Client-Side JS with DICT, cycle, hover, and theme toggle */
</script>
</body>
```

---

## 3. Standard Header Specifications

```html
<header class="doc-header">
  <div class="mono-kicker">MANUAL // CBSE CLASS 12 ENGLISH CORE (FLAMINGO) // CH-{XX}</div>
  <h1>{CHAPTER TITLE IN UPPERCASE}</h1>
  <div class="doc-subtitle">{Subtitle} by <strong>{Author}</strong></div>
  <div class="doc-specs">
    <span class="spec-pill">SYLLABUS: 2026–27</span>
    <span class="spec-pill">FORMAT: PASSAGE-BY-PASSAGE MANUAL</span>
    <span class="spec-pill">SOURCES: NCERT + LITCHART + CBSE PYQS</span>
    <span class="spec-pill">TARGET: 100/100 BOARDS</span>
  </div>
</header>
```

---

## 4. Standard Table of Contents (`.toc-box`)

```html
<nav class="toc-box">
  <div class="toc-title">
    <span>INDEX // QUICK NAVIGATION</span>
    <span>[8 SECTIONS]</span>
  </div>
  <ul class="toc-list">
    <li><a href="#overview">01. EXECUTIVE EXAM COMPASS &amp; THEMES</a></li>
    <li><a href="#keywords">02. CBSE GOLDEN KEYWORDS BANK</a></li>
    <li><a href="#passages">03. PASSAGE-BY-PASSAGE BREAKDOWN (01 TO {N})</a></li>
    <li><a href="#characters">04. MASTER CHARACTER SKETCHES</a></li>
    <li><a href="#rtc">05. REFERENCE TO CONTEXT (EXTRACT-BASED QS)</a></li>
    <li><a href="#short-qa">06. HIGH-YIELD SHORT ANSWER QS (2 MARKS)</a></li>
    <li><a href="#long-qa">07. HIGH-SCORING LONG ANSWER QS (5 MARKS)</a></li>
    <li><a href="#pyq-vault">08. PREVIOUS YEARS' QUESTION VAULT (2019–2025)</a></li>
  </ul>
</nav>
```

---

## 5. Section Specifications (Strict IDs & Layouts)

| Section | ID | Direct Header Element | Interior Layout / Grid Requirement |
| :--- | :--- | :--- | :--- |
| **01** | `overview` | `<h2 class="section-header">01. Executive Exam Compass & Themes</h2>` | `<div class="desktop-grid-2">` wrapping thematic cards (`.bw-card.accent` and `.bw-card`); optional `<div class="table-wrapper">` for motifs |
| **02** | `keywords` | `<h2 class="section-header">02. CBSE Golden Keywords Bank</h2>` | `<div class="keyword-cloud">` with `<span class="keyword-tag">` items |
| **03** | `passages` | `<h2 class="section-header">03. Passage-by-Passage Breakdown (01 to {N})</h2>` | Sequence of `<article class="passage-card" id="passage-1">` through `passage-{N}` with exact sub-modules (see below) |
| **04** | `characters` | `<h2 class="section-header">04. Master Character Sketches & Psychological Profiles</h2>` | `<div class="desktop-grid-2">` wrapping character cards (`.bw-card.accent` and `.bw-card`) |
| **05** | `rtc` | `<h2 class="section-header">05. Reference to Context (Extract-Based Questions & Answers)</h2>` | Sequence of `<div class="qa-card">` with `.quote-passage` (`<span class="quote-label">EXTRACT</span>`), `.qa-card-q`, and `.qa-card-a` |
| **06** | `short-qa` | `<h2 class="section-header">06. High-Yield Short Answer Qs (2 Marks / 40–50 Words)</h2>` | `<div class="desktop-grid-2">` wrapping 2M `<div class="qa-card">` with `<div class="qa-card-vp"><strong>Value Points:</strong> ...</div>` |
| **07** | `long-qa` | `<h2 class="section-header">07. High-Scoring Long Answer & Comparative Questions (CBSE 5 Marks / 120–150 Words)</h2>` | Sequence of 5M `<div class="qa-card">` with `<div class="qa-card-vp"><strong>CBSE Value Points:</strong> ...</div>` |
| **08** | `pyq-vault` | `<h2 class="section-header">08. Previous Years' Question Vault (2019–2025)</h2>` | `<div class="table-wrapper">` with 3 columns (`Year / Marks`, `Question Asked in Board Exam`, `Key Scoring Criteria`) |

### Section 03 Sub-Module Exact Labels
Every `<article class="passage-card">` MUST contain the four sub-modules with these exact labels:
1. Vocabulary: `<div class="sub-module"><div class="sub-label">[ VOCABULARY &amp; PHRASES ]</div>...</div>`
2. Literary Devices: `<div class="sub-module"><div class="sub-label">[ LITERARY &amp; STYLISTIC DEVICES ]</div>...</div>`
3. Psychological Analysis: `<div class="sub-module"><div class="sub-label">[ LITERARY &amp; PSYCHOLOGICAL ANALYSIS ]</div>...</div>`
4. Exam Value Box: `<div class="exam-value-box"><div class="sub-label" style="margin-bottom:6px;">[ CBSE EXAM VALUE POINTS &amp; RTC ]</div>...</div>`

---

## 6. Standard Footer

```html
<footer class="doc-footer">
  <div>END OF MANUAL // CBSE CLASS 12 ENGLISH CORE // CHAPTER {N}: {TITLE}</div>
  <div style="margin-top:6px; font-size:0.75rem;">
    Synthesized from Official NCERT Text, LitCharts Analysis, SuccessCDs, and CBSE Board Marking Schemes.
  </div>
</footer>
```

---

## 7. Mandatory 15-Point Benchmark Verification Engine
Before finalizing any chapter (existing or coming), the automated benchmark verification script MUST be executed and pass 15/15 checks:
```bash
python compare_chapters_to_gp.py
```
If any check fails, the chapter must NOT be compiled to PDF or committed to git until resolved.

---

## 7. Vector PDF Generation Pipeline

All PDFs MUST be generated using headless Chrome with vector Google Sans font embedding:
```bash
chrome --headless=new --disable-gpu --print-to-pdf="PDF/{Chapter_Name}_CBSE_Guide.pdf" "HTML/{chapter_name}_cbse_mastery.html"
```
This guarantees identical typography, page numbering, and publication-ready vector rendering matching `Going_Places_CBSE_Guide.pdf`.
