from playwright.sync_api import sync_playwright
import os
import time

def capture_slides(output_dir):
    print("Capturing slides for all 7 Herman Miller Alternatives...")
    os.makedirs(output_dir, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Mobile viewport for TikTok/Reels format
        context = browser.new_context(
            viewport={'width': 1080, 'height': 1920},
            device_scale_factor=2,
            user_agent="Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        )
        page = context.new_page()
        
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        local_url = f"file:///{base_path}/reviews/herman-miller-alternatives.html".replace('\\', '/')
        page.goto(local_url)
        time.sleep(1)
        
        # 1. Hero Slide
        print("Capturing Slide: Hero")
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(0.5)
        page.screenshot(path=os.path.join(output_dir, "slide_hero.png"))
        
        # 2. Individual Chairs (We'll scroll to each .ranked-item)
        chairs = page.locator(".ranked-item")
        count = chairs.count()
        print(f"Found {count} chairs to capture.")
        
        for i in range(count):
            print(f"Capturing Chair {i+1}...")
            chair_locator = chairs.nth(i)
            chair_locator.scroll_into_view_if_needed()
            
            # Slight offset to center the block on a mobile screen
            page.evaluate("window.scrollBy(0, -100)") 
            time.sleep(1.0)
            
            page.screenshot(path=os.path.join(output_dir, f"slide_chair_{i+1}.png"))
            
        browser.close()
        print("Slides captured successfully.")

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "assets")
    capture_slides(out_dir)
