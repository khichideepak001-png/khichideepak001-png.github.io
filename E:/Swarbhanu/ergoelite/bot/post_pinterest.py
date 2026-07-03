"""
Pinterest pin creator with stealth browser + human-like behavior.
Uses playwright-stealth to bypass bot detection.
"""
from playwright.sync_api import sync_playwright
import os
import sys
import time
import random

# Import our stealth utilities
sys.path.insert(0, os.path.dirname(__file__))
from stealth_utils import (
    create_stealth_browser, human_delay, human_type,
    human_scroll
)


def create_pin(image_path, title, description, link):
    state_path = os.path.join(os.path.dirname(__file__), "state_all.json")
    if not os.path.exists(state_path):
        print("Error: state_all.json not found.")
        sys.exit(1)
        
    print("[Pinterest] Navigating to Pin Creation...")
    with sync_playwright() as p:
        # Pinterest works better with Firefox
        browser, context, page = create_stealth_browser(
            p,
            browser_type="firefox",
            headless=True,
            storage_state=state_path
        )
        
        try:
            page.goto("https://www.pinterest.com/pin-creation-tool/",
                      referer="https://www.pinterest.com/")
            human_delay(3.0, 5.0)
            
            # Upload image
            print("[Pinterest] Uploading image...")
            file_input = page.locator("input[type='file']")
            file_input.wait_for(state="attached", timeout=15000)
            file_input.set_input_files(image_path)
            human_delay(2.0, 3.5)
            
            # Set Title with human typing
            print("[Pinterest] Setting title...")
            title_input = page.locator("input[placeholder*='title'], textarea[placeholder*='title']").first
            title_input.click()
            human_delay(0.3, 0.7)
            human_type(page, title, min_delay_ms=30, max_delay_ms=80)
            human_delay(0.5, 1.0)
            
            # Set Description with human typing
            print("[Pinterest] Setting description...")
            desc_input = page.locator("div[contenteditable='true'], textarea[placeholder*='description']").first
            desc_input.click()
            human_delay(0.3, 0.7)
            human_type(page, description, min_delay_ms=20, max_delay_ms=70)
            human_delay(0.5, 1.0)
            
            # Set Link
            print("[Pinterest] Setting destination link...")
            link_input = page.locator("input[placeholder*='link'], input[type='url'], input[name='link']").first
            link_input.click()
            human_delay(0.3, 0.5)
            human_type(page, link, min_delay_ms=15, max_delay_ms=50)
            human_delay(1.0, 2.0)
            
            # Click Publish with natural delay
            print("[Pinterest] Publishing Pin...")
            publish_btn = page.get_by_role("button", name="Publish").first
            if not publish_btn.is_visible():
                publish_btn = page.get_by_role("button", name="Save").first
            
            human_delay(0.5, 1.0)
            publish_btn.click()
            human_delay(4.0, 6.0)
            print("[Pinterest] Successfully published Pin! (OK)")
            
        except Exception as e:
            print(f"[Pinterest] Failed to publish Pin: {e}")
            page.screenshot(path=os.path.join(os.path.dirname(__file__), "pinterest_error.png"), full_page=True)
            print("[Pinterest] Saved debug screenshot to pinterest_error.png")
            
        finally:
            browser.close()


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print('Usage: python post_pinterest.py <image_path> "<title>" "<description>" <website_url>')
        sys.exit(1)
    create_pin(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
