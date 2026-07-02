from playwright.sync_api import sync_playwright
import os
import sys
import time

def post_quora_answer(url, message):
    state_path = os.path.join(os.path.dirname(__file__), "state_all.json")
    if not os.path.exists(state_path):
        print("Error: state_all.json not found.")
        sys.exit(1)
        
    print(f"Navigating to {url}...")
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(
            storage_state=state_path,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"
        )
        page = context.new_page()
        
        try:
            page.goto(url, wait_until="domcontentloaded")
            time.sleep(2)
            print("Looking for 'Answer' button...")
            
            # Click the "Answer" button to open the editor
            answer_btn = page.get_by_role("button", name="Answer").first
            if not answer_btn.is_visible():
                answer_btn = page.locator("button:has-text('Answer')").first
            answer_btn.click()
            time.sleep(3)
            
            print("Typing message into editor...")
            editor = page.locator("div[contenteditable='true']").first
            editor.wait_for(state="visible", timeout=10000)
            editor.click()
            page.keyboard.type(message)
            time.sleep(2)
            
            print("Clicking Post...")
            post_btn = page.get_by_role("button", name="Post").first
            if not post_btn.is_visible():
                post_btn = page.locator("button:has-text('Post')").first
            post_btn.click()
            
            time.sleep(4)
            print("Successfully posted answer to Quora!")
            
        except Exception as e:
            print(f"Failed to post to Quora: {e}")
            page.screenshot(path="quora_error.png", full_page=True)
            print("Saved debug screenshot to quora_error.png")
            
        finally:
            browser.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python post_quora_reply.py <quora_url> \"<your message>\"")
        sys.exit(1)
    post_quora_answer(sys.argv[1], sys.argv[2])
