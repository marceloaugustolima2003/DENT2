
import asyncio
from playwright.async_api import async_playwright

async def verify_flag_fill():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Load the page via local server
        await page.goto("http://localhost:8000/index.html")

        # Wait for the button to be present and SVG to be injected
        btn_selector = "#current-language-btn"
        svg_selector = "#current-language-btn svg"

        try:
            await page.wait_for_selector(svg_selector, timeout=10000)
        except Exception as e:
            print("Timeout waiting for SVG. Checking console logs...")
            print(f"Error: {e}")
            await browser.close()
            return

        # Get the button element
        btn = page.locator(btn_selector)

        # Get the SVG inside the button
        svg = btn.locator("svg")

        # Get bounding box of button and SVG
        btn_box = await btn.bounding_box()
        svg_box = await svg.bounding_box()

        print(f"Button Box: {btn_box}")
        print(f"SVG Box: {svg_box}")

        # Check if dimensions match (allowing for border)
        # Button has 1px border, so content box is 2px smaller.
        # w-12 is 48px. Border 1px. Content 46px.
        # SVG w-full fills content (46px).
        # So SVG should be around 46px. Button 48px. Diff around 2px.

        width_diff = abs(btn_box['width'] - svg_box['width'])
        height_diff = abs(btn_box['height'] - svg_box['height'])

        print(f"Width Diff: {width_diff}")
        print(f"Height Diff: {height_diff}")

        if width_diff <= 3 and height_diff <= 3:
            print("SUCCESS: SVG fills the button content box.")
        else:
            print("FAILURE: SVG does not fill the button content box.")

        # Take a screenshot for visual confirmation
        await page.screenshot(path="verification/flag_fill_check.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify_flag_fill())
