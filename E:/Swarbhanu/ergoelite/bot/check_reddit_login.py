from playwright.sync_api import sync_playwright
import os

def check_login():
    state_path = os.path.join(os.path.dirname(__file__), "state.json")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=state_path)
        page = context.new_page()
        page.goto("https://www.reddit.com/")
        page.wait_for_timeout(3000)
        
        is_logged_in = page.locator("shreddit-profile-button").count() > 0 or page.locator("button:has-text('Log In')").count() == 0
        print(f"Logged in: {is_logged_in}")
        
        page.screenshot(path="reddit_login_debug.png", full_page=True)
        browser.close()

if __name__ == "__main__":
    check_login()
