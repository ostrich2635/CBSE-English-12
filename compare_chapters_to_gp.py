import os
import re

chapters = [
    ('Ch 01: The Last Lesson', 'HTML/the_last_lesson_cbse_mastery.html'),
    ('Ch 02: Lost Spring', 'HTML/lost_spring_cbse_mastery.html'),
    ('Ch 03: Deep Water', 'HTML/deep_water_cbse_mastery.html'),
    ('Ch 04: The Rattrap', 'HTML/the_rattrap_cbse_mastery.html'),
    ('Ch 05: Indigo', 'HTML/indigo_cbse_mastery.html'),
    ('Ch 06: Poets and Pancakes', 'HTML/poets_and_pancakes_cbse_mastery.html'),
    ('Ch 07: The Interview', 'HTML/the_interview_cbse_mastery.html'),
    ('Ch 08: Going Places (BENCHMARK)', 'HTML/going_places_cbse_mastery.html'),
    ('Poem 01: My Mother at Sixty-Six', 'HTML/my_mother_at_sixty_six_cbse_mastery.html'),
    ('Poem 02: Keeping Quiet', 'HTML/keeping_quiet_cbse_mastery.html'),
]

# Canonical patterns from Going Places:
checks = [
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

print("=== AUDIT OF ALL CHAPTERS AGAINST GOING PLACES BENCHMARK ===")
all_pass = True
for name, path in chapters:
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

if all_pass:
    print("\n>>> ALL CHAPTERS (INCLUDING BENCHMARK) PASSED 15/15 BENCHMARK CHECKS! <<<")
else:
    print("\n>>> DIVERGENCE DETECTED. <<<")
