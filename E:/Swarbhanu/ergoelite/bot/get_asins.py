from playwright.sync_api import sync_playwright
import re

queries = [
    "Vertical Ergonomic Mouse",
    "Large Felt Desk Pad",
    "Under Desk Clamp Keyboard Tray",
    "Coccyx Orthopedic Gel Seat Cushion",
    "Anti Fatigue Standing Desk Mat",
    "Blue Light Blocking Glasses",
    "Adjustable Gooseneck Desk Lamp",
    "Clamp on Monitor Mount Arm",
    "Posture Corrector Brace",
    "Under Desk Cable Management Tray",
    "Headphone Stand with USB Hub"
]

def main():
    print("Fetching live ASINs for 11 new products from Amazon...")
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"
        )
        page = context.new_page()
        
        for q in queries:
            print(f"Searching for: {q}")
            page.goto(f"https://www.amazon.com/s?k={q.replace(' ', '+')}")
            page.wait_for_selector("div[data-asin]", timeout=5000)
            
            # Find the first item that has an actual ASIN starting with B0
            items = page.locator("div[data-asin]").all()
            found = False
            for item in items:
                asin = item.get_attribute("data-asin")
                if asin and asin.startswith("B0") and len(asin) == 10:
                    print(f"Found ASIN for '{q}': {asin}")
                    found = True
                    break
            if not found:
                print(f"Could not find ASIN for '{q}'")
                
        browser.close()

if __name__ == "__main__":
    main()
