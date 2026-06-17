from playwright.sync_api import sync_playwright
import os
import json
import time

def post_facebook_reply(lead, reply_text):
    state_path = os.path.join(os.path.dirname(__file__), "state_all.json")
    if not os.path.exists(state_path):
        print("Error: state_all.json not found. Run login_all.py first.")
        return False
        
    print(f"Attempting to post reply to Facebook post: {lead['url']}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # Headless=False helps avoid FB bot detection
        context = browser.new_context(
            storage_state=state_path,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            page.goto(lead['url'])
            page.wait_for_timeout(3000)
            
            # Click the comment box
            comment_box = page.locator("div[aria-label='Write a comment']")
            if comment_box.count() > 0:
                comment_box.first.click()
                page.wait_for_timeout(1000)
                
                # Type the reply
                comment_box.first.fill(reply_text)
                page.wait_for_timeout(2000)
                
                # Press Enter to post
                page.keyboard.press("Enter")
                page.wait_for_timeout(3000)
                print("Successfully posted to Facebook!")
                return True
            else:
                print("Could not find the comment box. You might not have permission to comment.")
                return False
                
        except Exception as e:
            print(f"Error posting to FB: {e}")
            return False
        finally:
            browser.close()

if __name__ == "__main__":
    # Test script with dummy lead
    dummy_lead = {"url": "https://www.facebook.com/"}
    # post_facebook_reply(dummy_lead, "Test comment")
    print("Facebook poster ready.")
