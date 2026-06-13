from playwright.sync_api import sync_playwright
import os
import sys

def main():
    print("Launching standard Google Chrome...")
    with sync_playwright() as p:
        # Using channel="chrome" uses your real installed Chrome instead of the bot version
        # args disables the "Chrome is being controlled by automated software" flag
        browser = p.chromium.launch(
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # Go to Reddit login page
        print("Navigating to Reddit...")
        page.goto("https://www.reddit.com/login")
        
        # Wait for the user to log in
        print("\n" + "="*50)
        print("🛑 ACTION REQUIRED IN BROWSER 🛑")
        print("Please log into your Reddit account in the browser window that just opened.")
        print("Once you are fully logged in and see the Reddit homepage...")
        print("="*50 + "\n")
        
        input("👉 PRESS ENTER HERE ONCE YOU HAVE LOGGED IN... ")
        
        # Save the authentication state
        state_path = os.path.join(os.path.dirname(__file__), "state.json")
        context.storage_state(path=state_path)
        
        print(f"\n✅ Success! Your login session has been saved to: {state_path}")
        print("You can now close the browser.")
        
        browser.close()

if __name__ == "__main__":
    main()
