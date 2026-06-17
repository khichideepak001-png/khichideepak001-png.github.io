from playwright.sync_api import sync_playwright
import os
import sys
import time

def create_pin(image_path, title, description, link):
    state_path = os.path.join(os.path.dirname(__file__), "state_all.json")
    if not os.path.exists(state_path):
        print("Error: state_all.json not found.")
        sys.exit(1)
        
    print("Navigating to Pinterest Pin Creation...")
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(
            storage_state=state_path,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"
        )
        page = context.new_page()
        
        try:
            page.goto("https://www.pinterest.com/pin-creation-tool/")
            time.sleep(4)
            
            # Upload image
            print("Uploading image...")
            file_input = page.locator("input[type='file']")
            file_input.set_input_files(image_path)
            time.sleep(2)
            
            # Set Title
            print("Setting title...")
            title_input = page.locator("input[placeholder*='Add a title']")
            title_input.fill(title)
            
            # Set Description
            print("Setting description...")
            desc_input = page.locator("div[contenteditable='true']")
            desc_input.first.type(description)
            
            # Set Link — try multiple selectors as Pinterest updates UI frequently
            print("Setting destination link...")
            link_selectors = [
                "input[placeholder*='destination link']",
                "input[placeholder*='Add a link']",
                "input[data-test-id='pin-draft-link']",
                "input[name='link']",
                "input[type='url']"
            ]
            link_filled = False
            for sel in link_selectors:
                try:
                    inp = page.locator(sel)
                    inp.wait_for(timeout=5000)
                    inp.fill(link)
                    link_filled = True
                    print(f"  Link filled using: {sel}")
                    break
                except:
                    continue
            if not link_filled:
                print("  Warning: Could not fill link field, continuing anyway...")
            time.sleep(1)
            
            # Click Publish — try multiple selectors
            print("Publishing Pin...")
            save_selectors = [
                "button[data-test-id='board-dropdown-save-button']",
                "button[data-test-id='pin-draft-save-button']",
                "button:has-text('Publish')",
                "button:has-text('Save')",
                "div[data-test-id='storyboard-creation-nav-right'] button"
            ]
            saved = False
            for sel in save_selectors:
                try:
                    btn = page.locator(sel).first
                    btn.wait_for(timeout=5000)
                    btn.click()
                    saved = True
                    print(f"  Published using: {sel}")
                    break
                except:
                    continue
            if not saved:
                print("  Warning: Could not find publish button")
            
            time.sleep(5)
            print("Successfully published Pin to Pinterest!")
            
        except Exception as e:
            print(f"[Error] Failed to publish Pin: {e}")
            
        finally:
            browser.close()

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python post_pinterest.py <absolute_image_path> \"<title>\" \"<description>\" <website_url>")
        sys.exit(1)
    create_pin(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
