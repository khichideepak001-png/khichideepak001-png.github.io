from playwright.sync_api import sync_playwright
import os

def main():
    print("Launching Firefox to bypass Google's Chrome-specific blocks...")
    with sync_playwright() as p:
        # Launching Firefox instead of Chrome to bypass Google's Chrome bot detection
        browser = p.firefox.launch(
            headless=False
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"
        )
        page = context.new_page()
        
        print("\n!!! IMPORTANT: DO NOT CLOSE THE BROWSER WINDOW !!!")

        try:
            # 1. Pinterest
            print("\n" + "="*50)
            print("[!] 1/1: PINTEREST LOGIN [!]")
            print("="*50)
            page.goto("https://www.pinterest.com/login/")
            input("> PRESS ENTER HERE ONCE YOU ARE LOGGED INTO PINTEREST... ")
            
            # Save the master authentication state
            state_path = os.path.join(os.path.dirname(__file__), "state_all.json")
            context.storage_state(path=state_path)
            
            print(f"\n[OK] Success! All your login sessions have been saved to: {state_path}")
            print("You can now close the browser.")
            
        except Exception as e:
            print(f"\n[X] Error during login: {e}")
            
        finally:
            browser.close()

if __name__ == "__main__":
    main()
