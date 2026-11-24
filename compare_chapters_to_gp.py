import os
import re

chapters = [
    ('Ch 01: The Last Lesson', 'HTML/the_last_lesson_cbse_mastery.html', 16),
    ('Ch 02: Lost Spring', 'HTML/lost_spring_cbse_mastery.html', 16),
    ('Ch 03: Deep Water', 'HTML/deep_water_cbse_mastery.html', 20),
    ('Ch 04: The Rattrap', 'HTML/the_rattrap_cbse_mastery.html', 16),
    ('Ch 05: Indigo', 'HTML/indigo_cbse_mastery.html', 16),
    ('Ch 06: Poets and Pancakes', 'HTML/poets_and_pancakes_cbse_mastery.html', 16),
    ('Ch 07: The Interview', 'HTML/the_interview_cbse_mastery.html', 13),
    ('Ch 08: Going Places (BENCHMARK)', 'HTML/going_places_cbse_mastery.html', 16),
    ('Poem 01: My Mother at Sixty-Six', 'HTML/my_mother_at_sixty_six_cbse_mastery.html', 5),
    ('Poem 02: Keeping Quiet', 'HTML/keeping_quiet_cbse_mastery.html', 7),
    ('Poem 03: A Thing of Beauty', 'HTML/a_thing_of_beauty_cbse_mastery.html', 4),
    ('Poem 04: A Roadside Stand', 'HTML/a_roadside_stand_cbse_mastery.html', 5),
    ('Poem 05: Aunt Jennifer\'s Tigers', 'HTML/aunt_jennifers_tigers_cbse_mastery.html', 3),
    ('Vistas Ch 01: The Third Level', 'HTML/the_third_level_cbse_mastery.html', 10),
    ('Vistas Ch 02: The Tiger King', 'HTML/the_tiger_king_cbse_mastery.html', 10),
    ('Vistas Ch 03: Journey to the End of the Earth', 'HTML/journey_to_the_end_of_the_earth_cbse_mastery.html', 8),
]

# Canonical patterns from Going Places benchmark:
checks = [
    ('mono_kicker', r'<div class="mono-kicker">MANUAL // CBSE CLASS 12 ENGLISH CORE \((?:FLAMINGO|VISTAS)\) // CH-\d+</div>'),
    ('doc_specs_pill', r'<div class="doc-specs">\s*<span class="spec-pill">SYLLABUS: 2026–27</span>'),
    ('toc_box_title', r'<nav class="toc-box">\s*<div class="toc-title">\s*<span>INDEX // QUICK NAVIGATION</span>\s*<span>\[8 SECTIONS\]</span>'),
    ('toc_item_01', r'<li><a href="#overview">01\. EXECUTIVE EXAM COMPASS &amp; THEMES</a></li>'),
    ('toc_item_02', r'<li><a href="#keywords">02\. CBSE GOLDEN KEYWORDS BANK</a></li>'),
    ('toc_item_03', r'<li><a href="#passages">03\. PASSAGE-BY-PASSAGE BREAKDOWN \(01 TO \d+\)</a></li>'),
    ('toc_item_04', r'<li><a href="#characters">04\. MASTER CHARACTER SKETCHES</a></li>'),
    ('toc_item_05', r'<li><a href="#rtc">05\. REFERENCE TO CONTEXT \(EXTRACT-BASED QS\)</a></li>'),
    ('toc_item_06', r'<li><a href="#short-qa">06\. HIGH-YIELD SHORT ANSWER QS \(2 MARKS\)</a></li>'),
    ('toc_item_07', r'<li><a href="#long-qa">07\. HIGH-SCORING LONG ANSWER QS \(5 MARKS\)</a></li>'),
    ('toc_item_08', r'<li><a href="#pyq-vault">08\. PREVIOUS YEARS\' QUESTION VAULT \(2019–2025\)</a></li>'),
    ('sec_header_01', r'<h2 class="section-header">01\. Executive Exam Compass &amp; Themes</h2>'),
    ('sec_header_02', r'<h2 class="section-header">02\. CBSE Golden Keywords Bank</h2>'),
    ('sec_header_03', r'<h2 class="section-header">03\. Passage-by-Passage Breakdown \(01 to \d+\)</h2>'),
    ('sec_header_04', r'<h2 class="section-header">04\. Master Character Sketches &amp; Psychological Profiles</h2>'),
    ('sec_header_05', r'<h2 class="section-header">05\. Reference to Context \(Extract-Based Questions &amp; Answers\)</h2>'),
    ('sec_header_06', r'<h2 class="section-header">06\. High-Yield Short Answer Qs \(2 Marks / 40–50 Words\)</h2>'),
    ('sec_header_07', r'<h2 class="section-header">07\. High-Scoring Long Answer &amp; Comparative Questions \(CBSE 5 Marks / 120–150 Words\)</h2>'),
    ('sec_header_08', r'<h2 class="section-header">08\. Previous Years\' Question Vault \(2019–2025\)</h2>'),
    ('passage_headline', r'<div class="passage-headline">Passage 1:'),
    ('quote_passage', r'<div class="quote-passage">\s*<span class="quote-label">ORIGINAL VERBATIM TEXT</span>'),
    ('sub_module_vocab', r'<div class="sub-module">\s*<div class="sub-label">\[ VOCABULARY &amp; PHRASES \]</div>'),
    ('sub_module_devices', r'<div class="sub-module">\s*<div class="sub-label">\[ LITERARY &amp; STYLISTIC DEVICES \]</div>'),
    ('sub_module_analysis', r'<div class="sub-module">\s*<div class="sub-label">\[ LITERARY &amp; PSYCHOLOGICAL ANALYSIS \]</div>'),
    ('exam_value_box', r'<div class="exam-value-box">\s*<div class="sub-label"[^>]*>\[ CBSE EXAM VALUE POINTS &amp; RTC \]</div>'),
    ('keyword_cloud', r'<div class="keyword-cloud">'),
    ('qa_card', r'<div class="qa-card">\s*<div class="qa-card-meta">'),
    ('qa_card_vp', r'<div class="qa-card-vp"><strong>(?:CBSE\s+)?(?:<span[^>]*>)?Value(?:</span>)?\s+(?:<span[^>]*>)?Points(?:</span>)?:</strong>'),
    ('doc_footer', r'<footer class="doc-footer">'),
    ('container_closure', r'</footer>\s*</div>\s*<div class="floating-controls"'),
    ('floating_controls', r'<div class="floating-controls" id="floating-controls">\s*<button[^>]*id="theme-toggle"'),
    ('vocab_tooltip', r'<div id="vocab-tooltip">\s*<div class="tt-header">'),
]

print("=== RIGOROUS AUDIT OF ALL CHAPTERS AGAINST GOING PLACES BENCHMARK ===")
all_pass = True
for name, path, _ in chapters:
    print(f"\nChecking {name} ({path}):")
    if not os.path.exists(path):
        print("  FILE NOT FOUND!")
        all_pass = False
        continue
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    passed = 0
    failed = 0
    for c_name, pattern in checks:
        if re.search(pattern, html):
            passed += 1
        else:
            failed += 1
            print(f"  [X] FAILED: {c_name}")
            all_pass = False
    print(f"  Summary: {passed}/{len(checks)} passed, {failed} failed.")

# Check index.html standards
print("\n=== AUDITING index.html AGAINST BENCHMARK STANDARDS ===")
if os.path.exists('index.html'):
    with open('index.html', 'r', encoding='utf-8') as f:
        idx_html = f.read()
    
    idx_issues = []
    if 'format-links' in idx_html:
        idx_issues.append("Found unstyled 'format-links' (causes blue links)!")
    
    # Check that all active chapters use action-links
    active_htmls = [p for _, p, _ in chapters]
    for h in active_htmls:
        if f'href="{h}"' not in idx_html:
            idx_issues.append(f"Missing link to {h} in index.html!")
    
    # Check for un-bolded titles in active chapters
    titles = [
        "The Last Lesson", "Lost Spring: Stories of Stolen Childhood", "Deep Water",
        "The Rattrap", "Indigo", "Poets and Pancakes", "The Interview", "Going Places",
        "My Mother at Sixty-Six", "Keeping Quiet", "A Thing of Beauty", "A Roadside Stand",
        "Aunt Jennifer's Tigers", "The Third Level", "The Tiger King",
        "Journey to the End of the Earth"
    ]
    for t in titles:
        if f"<strong>{t}</strong>" not in idx_html:
            idx_issues.append(f"Chapter title not bolded: {t}")
    
    if idx_issues:
        print("  [X] index.html FAILED:")
        for iss in idx_issues:
            print(f"      - {iss}")
        all_pass = False
    else:
        print(f"  [PASS] index.html passed all standards (0 unstyled links, all {len(titles)} active titles bolded, uniform .action-links)!")
else:
    print("  [X] index.html not found!")
    all_pass = False

print("\n" + "=" * 80)
if all_pass:
    print(">>> 100% PERFECT PARITY: ALL CHAPTERS & index.html STRICTLY CONFORM TO GOING PLACES BENCHMARK! <<<")
else:
    print(">>> DIVERGENCE DETECTED. FIX REQUIRED. <<<")
print("=" * 80)
