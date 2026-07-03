"""
Quora answer poster with stealth browser + human-like behavior.
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


def post_quora_answer(url, message):
    state_path = os.path.join(os.path.dirname(__file__), "state_all.json")
    if not os.path.exists(state_path):
        print("Error: state_all.json not found.")
        sys.exit(1)
        
    print(f"[Quora] Navigating to {url}...")
    with sync_playwright() as p:
        browser, context, page = create_stealth_browser(
            p,
            browser_type="firefox",
            headless=True,
            storage_state=state_path
        )
        
        try:
            page.goto(url, wait_until="domcontentloaded", referer="https://www.quora.com/")
            human_delay(2.0, 4.0)
            
            # Simulate reading the question
            print("[Quora] Simulating reading the question...")
            human_scroll(page, "down", random.randint(200, 400))
            human_delay(2.0, 4.0)
            human_scroll(page, "up", random.randint(100, 200))
            human_delay(1.0, 2.0)
            
            print("[Quora] Looking for 'Answer' button...")
            
            # Click the "Answer" button to open the editor
            answer_btn = page.get_by_role("button", name="Answer").first
            if not answer_btn.is_visible():
                answer_btn = page.locator("button:has-text('Answer')").first
            
            human_delay(0.5, 1.0)
            answer_btn.click()
            human_delay(2.0, 4.0)
            
            print("[Quora] Typing message with human-like speed...")
            editor = page.locator("div[contenteditable='true']").first
            editor.wait_for(state="visible", timeout=15000)
            editor.click()
            human_delay(0.5, 1.0)
            
            # Type with natural human speed
            human_type(page, message, min_delay_ms=30, max_delay_ms=100)
            
            # Pause like re-reading your answer
            human_delay(2.0, 4.0)
            
            print("[Quora] Clicking Post...")
            post_btn = page.get_by_role("button", name="Post").first
            if not post_btn.is_visible():
                post_btn = page.locator("button:has-text('Post')").first
            
            human_delay(0.5, 1.0)
            post_btn.click()
            
            human_delay(3.0, 5.0)
            print("[Quora] Successfully posted answer! (OK)")
            
        except Exception as e:
            print(f"[Quora] Failed to post: {e}")
            page.screenshot(path=os.path.join(os.path.dirname(__file__), "quora_error.png"), full_page=True)
            print("[Quora] Saved debug screenshot to quora_error.png")
            
        finally:
            browser.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Usage: python post_quora_reply.py <quora_url> "<your message>"')
        sys.exit(1)
    post_quora_answer(sys.argv[1], sys.argv[2])
