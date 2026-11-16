import os
import subprocess
import tempfile
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def test_e2e():
    html_path = r"c:\Users\aishw\Downloads\CBSE Eng\HTML\going_places_cbse_mastery.html"
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    soup = BeautifulSoup(content, "html.parser")

    # 1. CSS Braces Check
    style_content = soup.find("style").string or ""
    assert style_content.count("{") == style_content.count("}"), (
        f"CSS braces mismatch: {style_content.count('{')} vs {style_content.count('}')}"
    )
    print(f"✓ CSS braces balanced: {style_content.count('{')}/{style_content.count('}')}")

    # 2. JS Syntax Check
    for i, s in enumerate(soup.find_all("script")):
        js_code = s.string or ""
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as tf:
            tf.write(js_code)
            tname = tf.name
        try:
            res = subprocess.run(["node", "--check", tname], capture_output=True, text=True)
            assert res.returncode == 0, f"JS syntax error in script {i}: {res.stderr}"
            print(f"✓ Script {i} JS syntax check passed!")
        finally:
            os.remove(tname)

    # 3. Playwright Headless Browser Check
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=True
        )
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        
        errors = []
        page.on("pageerror", lambda err: errors.append(f"PAGEERROR: {err}"))
        page.on("console", lambda msg: errors.append(f"CONSOLE: {msg.text}") if msg.type == "error" else None)

        url = r"file:///c:/Users/aishw/Downloads/CBSE%20Eng/HTML/going_places_cbse_mastery.html"
        page.goto(url, wait_until="load")

        # Verify 16 audio buttons
        audio_btns = page.locator(".audio-btn")
        count = audio_btns.count()
        assert count == 16, f"Expected 16 audio buttons, got {count}"
        print(f"✓ Found {count} audio buttons!")

        # Verify initial dock is hidden
        dock = page.locator("#audio-dock")
        assert not dock.is_visible(), "Audio dock should be hidden initially"
        print("✓ Audio dock initially hidden")

        # Click first audio button
        btn1 = audio_btns.first
        assert "[ ▶ LISTEN ]" in btn1.inner_text(), f"Unexpected button text: {btn1.inner_text()}"
        btn1.click()
        page.wait_for_timeout(500)

        # Check button state updated
        assert "[ ❚❚ PAUSE ]" in btn1.inner_text(), f"Expected PAUSE, got {btn1.inner_text()}"
        assert dock.is_visible(), "Audio dock should be visible after clicking Listen"
        print("✓ Button switched to [ ❚❚ PAUSE ] and audio dock is visible!")

        # Check dock title
        dock_title = page.locator("#dock-title").inner_text()
        assert "Passage 1" in dock_title, f"Unexpected dock title: {dock_title}"
        print(f"✓ Dock title: '{dock_title}'")

        # Test speed button
        btn_125 = page.locator(".dock-speed-btn[data-speed='1.25']")
        btn_125.click()
        assert "active" in btn_125.get_attribute("class"), "1.25x should be active"
        print("✓ Speed toggle to 1.25x working!")

        # Test next passage button
        page.locator("#dock-next").click()
        page.wait_for_timeout(300)
        dock_title2 = page.locator("#dock-title").inner_text()
        assert "Passage 2" in dock_title2, f"Expected Passage 2 in dock, got {dock_title2}"
        print(f"✓ Next passage control switched to: '{dock_title2}'")

        # Test close button
        page.locator("#dock-close").click()
        page.wait_for_timeout(300)
        assert not dock.is_visible(), "Dock should close on click close"
        print("✓ Audio dock closed successfully!")

        # Verify dark mode toggle still works
        page.evaluate("window.scrollTo(0, 500)")
        page.wait_for_timeout(300)
        toggle = page.locator("#theme-toggle")
        toggle.click()
        theme = page.evaluate("document.documentElement.getAttribute('data-theme')")
        assert theme == "dark", f"Expected dark theme, got {theme}"
        print("✓ Dark mode toggle working!")

        browser.close()
        assert len(errors) == 0, f"Encountered errors: {errors}"
        print("\nALL AUDIO E2E TESTS PASSED PERFECTLY WITH ZERO ERRORS!")

if __name__ == "__main__":
    test_e2e()
