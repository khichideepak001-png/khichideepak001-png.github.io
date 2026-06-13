from playwright.sync_api import sync_playwright
import os
import json
import time

def main():
    state_path = os.path.join(os.path.dirname(__file__), "state_all.json")
    
    # We will target common WFH and PC Setup groups.
    # In a real scenario, you'd navigate to the group's search URL.
    # e.g., https://www.facebook.com/groups/workfromhomesetups/search/?q=sciatica
    
    print("Fetching new leads from Facebook Groups...")
    leads = []
    
    queries = ["back pain", "wrist pain", "sciatica", "neck hurts"]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Using state_all.json assuming the user logged into FB using login_all.py
        context = browser.new_context(
            storage_state=state_path if os.path.exists(state_path) else None,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # Example Search on Facebook
        for q in queries:
            print(f"Scanning Facebook for: {q}...")
            page.goto(f"https://www.facebook.com/search/posts?q={q.replace(' ', '%20')}")
            page.wait_for_timeout(3000)
            
            # This is a highly simplified scraper. Facebook's DOM is complex and heavily obfuscated.
            try:
                # Look for post containers
                posts = page.locator("div[data-ad-preview='message']").all()
                for post in posts[:3]:
                    text = post.inner_text().strip()
                    if text and len(text) > 20:
                        leads.append({
                            "platform": "Facebook",
                            "query": q,
                            "text": text[:200] + "...",
                            "url": page.url
                        })
            except Exception as e:
                pass
                
        browser.close()
        
    print("\n--- NEW FACEBOOK LEADS ---")
    print(json.dumps(leads, indent=2))
    
    with open(os.path.join(os.path.dirname(__file__), "fb_leads.json"), "w", encoding='utf-8') as f:
        json.dump(leads, f, indent=2)

if __name__ == "__main__":
    main()
