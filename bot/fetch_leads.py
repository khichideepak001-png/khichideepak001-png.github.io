from playwright.sync_api import sync_playwright
import os
import json
import sys

def main():
    target_subs = ["OfficeChairs", "StandingDesk"]
    state_path = os.path.join(os.path.dirname(__file__), "state.json")
    
    if not os.path.exists(state_path):
        print("Error: state.json not found. Please run login.py first.")
        sys.exit(1)
        
    print("Fetching new leads from Reddit...")
    leads = []
    
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
        
        # Scan subreddits for specific pain points instead of just 'new'
        search_queries = [
            "wrist pain", "eye strain", "neck pain", "lower back pain",
            "cheap upgrade", "lumbar support", "sciatica sitting", 
            "tailbone pain", "carpal tunnel typing", "desk clutter",
            "cable management", "slouching at desk"
        ]
        
        for sub in target_subs:
            for query in search_queries:
                print(f"Scanning r/{sub} for '{query}'...")
                page.goto(f"https://www.reddit.com/r/{sub}/search/?q={query.replace(' ', '%20')}&restrict_sr=1&sort=new")
                try:
                    page.wait_for_selector("shreddit-post", timeout=5000)
                    posts = page.locator("shreddit-post").all()
                    for post in posts[:3]:  # Get top 3 per query
                        title = post.get_attribute("post-title")
                        permalink = post.get_attribute("permalink")
                        post_id = post.get_attribute("id")
                        
                        if title and permalink and post_id not in [l['id'] for l in leads]:
                            leads.append({
                                "sub": sub,
                                "query": query,
                                "title": title,
                                "url": f"https://www.reddit.com{permalink}",
                                "id": post_id
                            })
                            
                    if len(leads) >= 10:
                        break
                except:
                    continue
            if len(leads) >= 10:
                break
        
        browser.close()
        
    print("\n--- NEW LEADS ---")
    print(json.dumps(leads, indent=2))
    
    with open(os.path.join(os.path.dirname(__file__), "leads.json"), "w") as f:
        json.dump(leads, f, indent=2)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error fetching leads: {e}")
