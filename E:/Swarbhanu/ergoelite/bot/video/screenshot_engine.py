from playwright.sync_api import sync_playwright
import os
import time

def capture_slides(output_dir):
    print("Capturing multiple slides for the video...")
    os.makedirs(output_dir, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Mobile viewport
        context = browser.new_context(
            viewport={'width': 1080, 'height': 1920},
            device_scale_factor=2,
            user_agent="Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        )
        page = context.new_page()
        
        # SLIDE 1: Our Website (Accessories)
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        local_url = f"file:///{base_path}/reviews/accessories.html".replace('\\', '/')
        print("Capturing Slide 1 (Website Top)...")
        page.goto(local_url)
        time.sleep(1)
        page.screenshot(path=os.path.join(output_dir, "slide1.png"))
        
        # SLIDE 2: Our Website (Scrolled down to the Vertical Mouse)
        print("Capturing Slide 2 (Product Card)...")
        page.evaluate("window.scrollBy(0, 500)")
        time.sleep(1)
        page.screenshot(path=os.path.join(output_dir, "slide2.png"))
        
        # SLIDE 3: Amazon Product Page
        amazon_url = "https://www.amazon.com/dp/B0FX2QJ6B4"
        print("Capturing Slide 3 (Amazon Product)...")
        try:
            # wait_until="domcontentloaded" prevents timeout from background trackers
            page.goto(amazon_url, wait_until="domcontentloaded", timeout=15000) 
            time.sleep(3) # Let images load
            
            # Hide banner if present
            page.evaluate("""
                const banner = document.querySelector('#nav-bb-button');
                if(banner) banner.click();
            """)
            time.sleep(1)
            page.screenshot(path=os.path.join(output_dir, "slide3.png"))
        except Exception as e:
            print(f"Error capturing Amazon: {e}")
            # Fallback to taking another screenshot of our site if Amazon blocks headless
            page.goto(local_url)
            page.evaluate("window.scrollBy(0, 1000)")
            time.sleep(1)
            page.screenshot(path=os.path.join(output_dir, "slide3.png"))
            
        browser.close()
        print("Slides captured successfully.")

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "assets")
    capture_slides(out_dir)
