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
            file_input.wait_for(state="attached", timeout=10000)
            file_input.set_input_files(image_path)
            time.sleep(2)
            
            # Set Title
            print("Setting title...")
            title_input = page.locator("input[placeholder*='title'], textarea[placeholder*='title']").first
            title_input.fill(title)
            
            # Set Description
            print("Setting description...")
            desc_input = page.locator("div[contenteditable='true'], textarea[placeholder*='description']").first
            desc_input.fill(description)
            
            # Set Link
            print("Setting destination link...")
            link_input = page.locator("input[placeholder*='link'], input[type='url'], input[name='link']").first
            link_input.fill(link)
            time.sleep(1)
            
            # Click Publish
            print("Publishing Pin...")
            publish_btn = page.get_by_role("button", name="Publish").first
            if not publish_btn.is_visible():
                publish_btn = page.get_by_role("button", name="Save").first
            
            publish_btn.click()
            time.sleep(5)
            print("Successfully published Pin to Pinterest!")
            
        except Exception as e:
            print(f"[Error] Failed to publish Pin: {e}")
            page.screenshot(path="pinterest_error.png", full_page=True)
            print("Saved debug screenshot to pinterest_error.png")
            
        finally:
            browser.close()

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python post_pinterest.py <absolute_image_path> \"<title>\" \"<description>\" <website_url>")
        sys.exit(1)
    create_pin(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
