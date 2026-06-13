from playwright.sync_api import sync_playwright
import os
import sys
import time

def post_comment(url, message):
    state_path = os.path.join(os.path.dirname(__file__), "state.json")
    if not os.path.exists(state_path):
        print("Error: state.json not found.")
        sys.exit(1)
        
    print(f"Navigating to {url}...")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            storage_state=state_path,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            page.goto(url)
            print("Looking for comment box...")
            
            # Use JS to find and focus the contenteditable area inside the shadow dom of shreddit-composer
            page.evaluate('''() => {
                const composer = document.querySelector('shreddit-composer');
                if(composer) {
                    composer.style.display = 'block';
                    composer.shadowRoot.querySelector('div[contenteditable]').focus();
                }
            }''')
            time.sleep(2)
            
            print("Typing message...")
            page.keyboard.type(message)
            time.sleep(2)
            
            print("Clicking submit...")
            page.evaluate('''() => {
                const composer = document.querySelector('shreddit-composer');
                if(composer) {
                    composer.shadowRoot.querySelector('button[type="submit"]').click();
                }
            }''')
            
            time.sleep(3)
            print("Successfully posted to Reddit!")
            
        except Exception as e:
            print(f"Failed to post: {e}")
            
        finally:
            browser.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python post_reply.py <reddit_url> \"<your message>\"")
        sys.exit(1)
    post_comment(sys.argv[1], sys.argv[2])
