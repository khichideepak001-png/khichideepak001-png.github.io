from playwright.sync_api import sync_playwright
import os
import time

def main():
    print("Launching standard Firefox...")
    with sync_playwright() as p:
        state_path = os.path.join(os.path.dirname(__file__), "state_all.json")
        
        # Load existing state if it exists (so we don't lose Pinterest!)
        browser = p.firefox.launch(headless=False)
        if os.path.exists(state_path):
            context = browser.new_context(storage_state=state_path, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0")
        else:
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0")
            
        page = context.new_page()
        
        try:
            # 1. Quora
            print("\n" + "="*50)
            print("🛑 1/2: QUORA LOGIN 🛑")
            print("="*50)
            page.goto("https://www.quora.com/")
            input("👉 PRESS ENTER HERE ONCE YOU ARE LOGGED INTO QUORA... ")
            # Wait a second to ensure no weird redirects happen
            time.sleep(2) 
            # SAVE IMMEDIATELY
            context.storage_state(path=state_path)
            print("✅ Quora saved successfully!")
            
            # 2. Twitter
            print("\n" + "="*50)
            print("🛑 2/2: X (TWITTER) LOGIN 🛑")
            print("="*50)
            page.goto("https://twitter.com/login")
            input("👉 PRESS ENTER HERE ONCE YOU ARE LOGGED INTO TWITTER... ")
            time.sleep(2)
            
            # Save the master authentication state
            context.storage_state(path=state_path)
            print(f"\n✅ Success! Quora and Twitter completely saved to: {state_path}")
            
        except Exception as e:
            print(f"\n❌ Error during login: {e}")
            
        finally:
            browser.close()

if __name__ == "__main__":
    main()
