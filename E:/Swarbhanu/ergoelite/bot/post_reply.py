"""
Reddit reply poster with stealth browser + human-like behavior.
Uses playwright-stealth to bypass bot detection and simulates
natural typing, scrolling, and click patterns.
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
    human_scroll, human_click
)


def post_comment(url, message):
    state_path = os.path.join(os.path.dirname(__file__), "state.json")
    if not os.path.exists(state_path):
        print("Error: state.json not found.")
        sys.exit(1)
        
    print(f"[Reddit] Navigating to {url}...")
    with sync_playwright() as p:
        browser, context, page = create_stealth_browser(
            p,
            browser_type="chromium",
            headless=True,
            storage_state=state_path,
            channel="chrome"
        )
        
        try:
            # Navigate with a realistic referrer
            page.goto(url, wait_until="domcontentloaded", referer="https://www.reddit.com/")
            human_delay(2.0, 4.0)
            
            # Simulate reading the post first (scroll down a bit)
            print("[Reddit] Simulating reading the post...")
            human_scroll(page, "down", random.randint(200, 400))
            human_delay(1.5, 3.0)
            human_scroll(page, "down", random.randint(100, 300))
            human_delay(1.0, 2.0)
            
            # Scroll back up to find the comment box
            human_scroll(page, "up", random.randint(100, 200))
            human_delay(0.5, 1.0)
            
            print("[Reddit] Looking for comment box...")
            
            # Reddit's comment composer is initially collapsed.
            # We need to click the placeholder first to expand it.
            try:
                # Try clicking the collapsed placeholder to expand the editor
                placeholder = page.locator("shreddit-composer [placeholder='Join the conversation'], shreddit-composer [aria-placeholder='Join the conversation']").first
                placeholder.scroll_into_view_if_needed()
                human_delay(0.3, 0.6)
                placeholder.click()
                human_delay(1.0, 2.0)
            except Exception:
                # Alternative: click the composer wrapper itself
                try:
                    composer = page.locator("shreddit-composer").first
                    composer.scroll_into_view_if_needed()
                    human_delay(0.3, 0.6)
                    composer.click()
                    human_delay(1.0, 2.0)
                except Exception:
                    pass
            
            # Now the editor should be expanded and visible
            editor = page.locator("shreddit-composer div[contenteditable='true']").first
            editor.wait_for(state="visible", timeout=20000)
            
            # Click the editor to focus
            editor.click()
            human_delay(0.5, 1.5)
            
            print("[Reddit] Typing message with human-like speed...")
            # Type the message character by character with natural delays
            human_type(page, message, min_delay_ms=25, max_delay_ms=90)
            
            # Pause after typing (like re-reading what you wrote)
            human_delay(1.5, 3.0)
            
            print("[Reddit] Clicking submit...")
            submit_btn = page.locator("shreddit-composer button[type='submit'], shreddit-composer button:has-text('Comment')").first
            submit_btn.wait_for(state="visible", timeout=10000)
            human_delay(0.3, 0.8)
            submit_btn.click()
            
            human_delay(3.0, 5.0)
            print("[Reddit] Successfully posted comment! (OK)")
            
        except Exception as e:
            print(f"[Reddit] Failed to post: {e}")
            page.screenshot(path=os.path.join(os.path.dirname(__file__), "reddit_error.png"), full_page=True)
            print("[Reddit] Saved debug screenshot to reddit_error.png")
            
        finally:
            browser.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Usage: python post_reply.py <reddit_url> "<your message>"')
        sys.exit(1)
    post_comment(sys.argv[1], sys.argv[2])
