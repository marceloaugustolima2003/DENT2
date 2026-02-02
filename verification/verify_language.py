from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8080/index.html")

        # Wait for app to load
        try:
            page.wait_for_selector("#current-language-btn", state="visible", timeout=5000)
        except:
            print("Timeout waiting for language button")
            page.screenshot(path="verification/error.png")
            return

        # Initial screenshot
        page.screenshot(path="verification/verification_initial.png")

        # Verify text is Portuguese
        auth_title = page.locator("#auth-title")
        print(f"Initial Title: {auth_title.inner_text()}")

        # Click language button to open menu
        page.click("#current-language-btn")
        time.sleep(1) # Wait for animation
        page.screenshot(path="verification/verification_menu_open.png")

        # Click English option
        # The options might be hidden if logic fails, but let's try
        try:
            page.click("button[data-lang='en']")
            time.sleep(1) # Wait for update
            print(f"Updated Title: {auth_title.inner_text()}")
            page.screenshot(path="verification/verification_english.png")
        except Exception as e:
            print(f"Error clicking english option: {e}")
            page.screenshot(path="verification/error_click.png")

        browser.close()

if __name__ == "__main__":
    run()
