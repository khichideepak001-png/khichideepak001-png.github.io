import os
import sys
import json
import subprocess
import time
import random

# Anti-Ban Settings
MAX_LEADS_PER_RUN = 4 # Increased from 2 to process more leads per cycle
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
            "A high-quality standing desk is the absolute best investment for sciatica or lower back pain. Don't cheap out on the motors. I found this breakdown super helpful when I was shopping: {url}?tag=viralbraintea-20",
            "I switched to a standing desk about 6 months ago and my lower back pain is basically gone. The key is getting one with a quiet motor and good stability. This comparison helped me narrow it down: {url}?tag=viralbraintea-20",
            "Went through this exact same decision last year. Ended up going with a dual-motor setup and it's been rock solid. If you want to compare specs and real measurements, this guide breaks it all down: {url}?tag=viralbraintea-20",
            "My PT actually recommended I try alternating between sitting and standing throughout the day. Game changer for my herniated disc. Here's the guide I used to pick mine, they actually measure wobble and noise: {url}?tag=viralbraintea-20",
            "One thing people don't realize is how much motor quality varies between brands. Some are whisper-quiet, others sound like a blender. This breakdown compares them all with actual dB readings: {url}?tag=viralbraintea-20",
            "Standing desks saved my sanity working from home. I was getting terrible hip flexor tightness from sitting 10+ hours. If you want honest rankings (not sponsored), this one's pretty good: {url}?tag=viralbraintea-20"
        ]
    },
    "chair": {
        "url": "https://khichideepak001-png.github.io/reviews/best-ergonomic-chairs.html",
        "image": os.path.join(os.path.dirname(BOT_DIR), "assets", "ergonomic-chair-hero.jpg"),
        "pin_title": "Best Ergonomic Office Chairs 2026",
        "responses": [
            "I went through the same thing with neck and back pain. The Herman Miller is great, but there are actually some budget clones that perform 90% as well. This ranking guide helped me decide: {url}?tag=viralbraintea-20",
            "Honestly, upgrading to a proper ergonomic chair is night and day for spine alignment. It's totally worth the investment. Here's a really solid breakdown of the best ones this year: {url}?tag=viralbraintea-20",
            "Spent 3 months researching ergonomic chairs before pulling the trigger. The difference in lumbar support between a $200 and $500 chair is massive. This guide compares them all side by side: {url}?tag=viralbraintea-20",
            "As someone who sits 8-10 hours a day coding, investing in a proper chair was the best decision I made. Mesh backs are a must if you run hot. Here's a solid comparison: {url}?tag=viralbraintea-20",
            "I had the same question! Ended up going with a chair that has adjustable lumbar depth (not just height). Makes a huge difference. This guide ranks them by actual ergonomic features: {url}?tag=viralbraintea-20",
            "My chiropractor literally told me to stop using my gaming chair and get something with proper lumbar support. This comparison helped me find one without breaking the bank: {url}?tag=viralbraintea-20",
            "Don't sleep on seat depth adjustment \u2014 it's the most underrated feature for people under 5'8. This breakdown covers all the adjustability features for each chair: {url}?tag=viralbraintea-20"
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
    print("\n[1/4] Running fetch_leads.py (Reddit)...")
    subprocess.run([sys.executable, os.path.join(BOT_DIR, "fetch_leads.py")])
    
    print("\n[1/4] Running fetch_quora_leads.py (Quora)...")
    subprocess.run([sys.executable, os.path.join(BOT_DIR, "fetch_quora_leads.py")])
    
    # 2. Read leads
    leads = []
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, 'r') as f:
            reddit_leads = json.load(f)
            # Tag Reddit leads explicitly if not tagged
            for l in reddit_leads:
                l['platform'] = 'Reddit'
                l['id'] = l.get('id', l.get('url'))
            leads.extend(reddit_leads)
            
    QUORA_FILE = os.path.join(BOT_DIR, "quora_leads.json")
    if os.path.exists(QUORA_FILE):
        with open(QUORA_FILE, 'r', encoding='utf-8') as f:
            quora_leads = json.load(f)
            for l in quora_leads:
                l['id'] = l.get('id', l.get('url')) # Quora leads use URL as ID
            leads.extend(quora_leads)
            
    if not leads:
        print("No leads found. Exiting.")
        return
        
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
        
        # Step A: Post to Platform
        platform = lead.get('platform', 'Reddit')
        if platform == 'Quora':
            print("\n[A] Executing post_quora_reply.py...")
            subprocess.run([sys.executable, os.path.join(BOT_DIR, "post_quora_reply.py"), lead["url"], reply_msg])
        else:
            print("\n[A] Executing post_reply.py (Reddit)...")
            subprocess.run([sys.executable, os.path.join(BOT_DIR, "post_reply.py"), lead["url"], reply_msg])
        
        safe_sleep(DELAY_BETWEEN_ACTIONS)
        
        # Step B: Pin to Pinterest
        print("\n[B] Executing post_pinterest.py...")
        source_context = f"r/{lead['sub']}" if platform == 'Reddit' else "Quora"
        pin_desc = f"Just recommended this to someone on {source_context}. If you are looking for a {category.lower()}, check this out! #workfromhome #ergo"
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
