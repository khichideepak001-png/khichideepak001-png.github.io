from playwright.sync_api import sync_playwright
import os
import json
import sys

def main():
    queries = [
        "wrist pain typing", 
        "eye strain monitor", 
        "lumbar support office chair",
        "cheap way to fix posture",
        "sciatica sitting all day",
        "tailbone pain office chair",
        "neck pain from laptop",
        "hide desk cables",
        "mouse for carpal tunnel"
    ]
    state_path = os.path.join(os.path.dirname(__file__), "state_all.json")
    
    if not os.path.exists(state_path):
        print("Error: state_all.json not found.")
        sys.exit(1)
        
    print("Fetching new leads from Quora...")
    leads = []
    
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(
            storage_state=state_path,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"
        )
        page = context.new_page()
        
        for query in queries:
            print(f"Searching Quora for: {query}...")
            # Quora search URL
            page.goto(f"https://www.quora.com/search?q={query.replace(' ', '+')}&time=month&type=question")
            page.wait_for_timeout(3000)
            
            # Extract links that look like questions
            links = page.locator("a").all()
            for link in links:
                try:
                    href = link.get_attribute("href") or ""
                    text = link.inner_text().strip()
                    # Clean URL — strip query params for dedup but keep full URL
                    base_href = href.split("?")[0]
                    if (href.startswith("https://www.quora.com/") 
                            and "-" in base_href 
                            and len(text) > 15
                            and base_href not in [l['url'].split('?')[0] for l in leads]
                            and not any(x in base_href for x in ["/profile/", "/topic/", "/search"])):
                        leads.append({
                            "platform": "Quora",
                            "title": text,
                            "url": base_href
                        })
                        if len(leads) >= 5:  # Get top 5 per run to avoid spam
                            break
                except:
                    continue
        
        browser.close()
        
    print("\n--- NEW QUORA LEADS ---")
    print(json.dumps(leads, indent=2))
    
    with open(os.path.join(os.path.dirname(__file__), "quora_leads.json"), "w", encoding='utf-8') as f:
        json.dump(leads, f, indent=2)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error fetching Quora leads: {e}")
