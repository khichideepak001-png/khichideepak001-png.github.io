import os
import sys
import json
import subprocess
import time
import random

# Anti-Ban Settings
MAX_LEADS_PER_RUN = 2 # NEVER exceed this to protect the account
DELAY_BETWEEN_ACTIONS = (15, 30) # seconds
DELAY_BETWEEN_LEADS = (60, 120) # seconds

# Base paths
BOT_DIR = os.path.dirname(__file__)
LEADS_FILE = os.path.join(BOT_DIR, "leads.json")
HISTORY_FILE = os.path.join(BOT_DIR, "processed_leads.json")

# Product Knowledge Base
PRODUCTS = {
    "desk": {
        "url": "https://khichideepak001-png.github.io/reviews/best-standing-desks.html",
        "image": os.path.join(os.path.dirname(BOT_DIR), "assets", "standing-desk-hero.jpg"),
        "pin_title": "Top Standing Desks 2026 (No More Back Pain)",
        "responses": [
            "If you're dealing with back pain or just need an upgrade, I highly recommend looking into a solid standing desk. It completely changed my posture. Check out this guide, they test the motor noise and stability: {url}?tag=viralbraintea-20",
            "A high-quality standing desk is the absolute best investment for sciatica or lower back pain. Don't cheap out on the motors. I found this breakdown super helpful when I was shopping: {url}?tag=viralbraintea-20"
        ]
    },
    "chair": {
        "url": "https://khichideepak001-png.github.io/reviews/best-ergonomic-chairs.html",
        "image": os.path.join(os.path.dirname(BOT_DIR), "assets", "ergonomic-chair-hero.jpg"),
        "pin_title": "Best Ergonomic Office Chairs 2026",
        "responses": [
            "I went through the same thing with neck and back pain. The Herman Miller is great, but there are actually some budget clones that perform 90% as well. This ranking guide helped me decide: {url}?tag=viralbraintea-20",
            "Honestly, upgrading to a proper ergonomic chair is night and day for spine alignment. It's totally worth the investment. Here's a really solid breakdown of the best ones this year: {url}?tag=viralbraintea-20"
        ]
    }
}

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)

def safe_sleep(range_tuple):
    delay = random.randint(range_tuple[0], range_tuple[1])
    print(f"[Anti-Ban] Sleeping for {delay} seconds to mimic human behavior...")
    time.sleep(delay)

def main():
    print("=== STARTING AUTONOMOUS BOT LOOP ===")
    
    # 1. Fetch new leads
    print("\n[1/4] Running fetch_leads.py...")
    subprocess.run([sys.executable, os.path.join(BOT_DIR, "fetch_leads.py")])
    
    # 2. Read leads
    if not os.path.exists(LEADS_FILE):
        print("No leads file found. Exiting.")
        return
        
    with open(LEADS_FILE, 'r') as f:
        leads = json.load(f)
        
    history = load_history()
    
    # 3. Filter unprocessed leads
    new_leads = [l for l in leads if l['id'] not in history]
    print(f"\n[2/4] Found {len(new_leads)} unprocessed leads in queue.")
    
    if not new_leads:
        print("No new leads to process. Sleeping until next cron.")
        return
        
    # Limit to MAX_LEADS_PER_RUN to prevent spam bans
    process_queue = new_leads[:MAX_LEADS_PER_RUN]
    print(f"Limiting execution to {len(process_queue)} leads to protect account health.")
    
    for i, lead in enumerate(process_queue):
        print(f"\n--- Processing Lead {i+1}/{len(process_queue)} ---")
        print(f"Subreddit: {lead['sub']}")
        print(f"Title: {lead['title']}")
        
        # Decide product
        if "desk" in lead['sub'].lower() or "standing" in lead['title'].lower():
            prod = PRODUCTS["desk"]
            category = "Standing Desk"
        else:
            prod = PRODUCTS["chair"]
            category = "Ergonomic Chair"
            
        print(f"Assigned Category: {category}")
        
        # Pick random response and format it
        reply_msg = random.choice(prod["responses"]).replace("{url}", prod["url"])
        
        # Step A: Post to Reddit
        print("\n[A] Executing post_reply.py...")
        subprocess.run([sys.executable, os.path.join(BOT_DIR, "post_reply.py"), lead["url"], reply_msg])
        
        safe_sleep(DELAY_BETWEEN_ACTIONS)
        
        # Step B: Pin to Pinterest
        print("\n[B] Executing post_pinterest.py...")
        pin_desc = f"Just recommended this to someone on r/{lead['sub']}. If you are looking for a {category.lower()}, check this out! #workfromhome #ergo"
        subprocess.run([
            sys.executable, 
            os.path.join(BOT_DIR, "post_pinterest.py"), 
            prod["image"], 
            prod["pin_title"], 
            pin_desc, 
            prod["url"]
        ])
        
        # Mark as processed
        history.append(lead['id'])
        save_history(history)
        print(f"Lead {lead['id']} marked as processed.")
        
        if i < len(process_queue) - 1:
            safe_sleep(DELAY_BETWEEN_LEADS)
            
    print("\n=== BOT LOOP COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    main()
