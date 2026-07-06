from playwright.sync_api import sync_playwright
import os

def check_dom():
    state_path = os.path.join(os.path.dirname(__file__), "state.json")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=state_path)
        page = context.new_page()
        # Navigate to a known post
        page.goto("https://www.reddit.com/r/StandingDesk/comments/1ulfyy4/recommendations_for_a_standing_desk_under_500/")
        page.wait_for_timeout(5000)
        
        # Dump composer HTML
        try:
            html = page.locator("shreddit-composer").first.inner_html()
            with open("composer_dom.txt", "w", encoding="utf-8") as f:
                f.write(html)
            print("Successfully dumped shreddit-composer HTML")
        except Exception as e:
            print(f"Error finding composer: {e}")
            
        browser.close()

if __name__ == "__main__":
    check_dom()
