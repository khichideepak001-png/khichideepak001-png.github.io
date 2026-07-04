"""
Lead fetcher using Agent-Reach for Reddit + Quora reading.
This separates the "reading" (finding leads) from the "posting" (commenting),
so the posting browser is never associated with scraping behavior.

Strategy:
1. Try Agent-Reach's rdt-cli for Reddit (bypasses 403 blocks)
2. Fallback to feedparser-based RSS reading (bundled with Agent-Reach)
3. Quora leads via separate RSS feeds
"""

import json
import os
import subprocess
import sys
import time
import random
import urllib.request
import xml.etree.ElementTree as ET

# Agent-Reach bundles feedparser
try:
    import feedparser
    HAS_FEEDPARSER = True
    print("[Agent-Reach] feedparser loaded OK")
except ImportError:
    HAS_FEEDPARSER = False
    print("[Agent-Reach] feedparser not available, using raw XML parsing")

BOT_DIR = os.path.dirname(__file__)

# High-intent keywords — broader net to catch more leads
KEYWORDS = [
    # Product-specific (highest conversion)
    "standing desk", "sit stand desk", "adjustable desk", "motorized desk",
    "ergonomic chair", "office chair", "desk chair", "task chair",
    "herman miller", "steelcase", "flexispot", "uplift", "autonomous", "secretlab",
    "branch chair", "sihoo", "hbada", "hon ignition",
    # Pain-point keywords (high buyer intent)
    "posture", "lumbar support", "sciatica", "back pain", "neck pain",
    "wrist pain", "carpal tunnel", "monitor arm", "keyboard tray",
    "shoulder pain desk", "hip pain sitting", "tailbone pain", "coccyx",
    # Buying keywords (ready to purchase)
    "best chair under", "chair recommendation", "desk recommendation",
    "which chair", "which desk", "should i buy", "worth it",
    "chair advice", "desk advice", "upgrade my chair", "upgrade my desk",
    # Setup keywords
    "work from home setup", "home office setup", "wfh gear", "wfh setup",
    "remote work setup", "desk setup", "office setup",
    # Duration keywords (signals heavy use = high intent)
    "8 hours sitting", "10 hours", "long hours", "all day",
    "comfortable chair", "mesh chair", "gaming chair office",
    # Comparison keywords
    "aeron vs", "leap vs", "embody vs", "flexispot vs", "uplift vs",
    "chair comparison", "desk comparison",
]

# Expanded target subreddits
TARGET_SUBS = [
    "OfficeChairs", "StandingDesk", "workfromhome", "desksetup",
    "homeoffice", "Ergonomics", "BackPain", "remotework",
    "battlestations", "WFH", "pcmasterrace",
    # New high-traffic subs
    "AskMen", "AskWomen", "gaming", "buildapc", "programming",
    "sysadmin", "webdev", "cscareerquestions", "freelance",
    "digitalnomad", "Posture", "ChronicPain", "physicaltherapy",
    "buyitforlife", "Frugal", "malelivingspace",
]


def try_rdt_cli(subreddit: str) -> list:
    """
    Try using Agent-Reach's rdt-cli to fetch Reddit posts.
    This uses the user's browser cookies to bypass 403 blocks.
    Returns list of (post_id, title, url, content) tuples.
    """
    try:
        result = subprocess.run(
            ["rdt-cli", "list", f"r/{subreddit}", "--sort=new", "--limit=25", "--format=json"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            posts = json.loads(result.stdout)
            entries = []
            for post in posts:
                entries.append((
                    post.get("id", ""),
                    post.get("title", ""),
                    post.get("url", f"https://www.reddit.com/r/{subreddit}/comments/{post.get('id', '')}"),
                    post.get("selftext", "")
                ))
            return entries
    except FileNotFoundError:
        pass  # rdt-cli not installed yet
    except Exception as e:
        print(f"  [rdt-cli] Error for r/{subreddit}: {e}")
    return []


def fetch_via_feedparser(subreddit: str) -> list:
    """
    Fetch Reddit posts via RSS using Agent-Reach's bundled feedparser.
    More robust than raw XML parsing.
    """
    url = f"https://www.reddit.com/r/{subreddit}/new.rss"
    entries = []
    
    try:
        feed = feedparser.parse(url, agent=f'Mozilla/5.0 (compatible; FeedBot/{random.random():.4f})')
        for entry in feed.entries:
            post_id = getattr(entry, 'id', '')
            title = getattr(entry, 'title', '')
            link = getattr(entry, 'link', '')
            content = ''
            if hasattr(entry, 'content') and entry.content:
                content = entry.content[0].get('value', '')
            elif hasattr(entry, 'summary'):
                content = entry.summary or ''
            
            entries.append((post_id, title, link, content))
    except Exception as e:
        print(f"  [feedparser] Error for r/{subreddit}: {e}")
    
    return entries


def fetch_via_raw_rss(subreddit: str) -> list:
    """
    Legacy fallback: raw RSS parsing without feedparser.
    """
    url = f"https://www.reddit.com/r/{subreddit}/new.rss"
    entries = []
    
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0.0.0 Safari/537.36'}
        )
        response = urllib.request.urlopen(req, timeout=15).read()
        root = ET.fromstring(response)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        for entry in root.findall('atom:entry', ns):
            post_id = entry.find('atom:id', ns).text
            title = entry.find('atom:title', ns).text
            link = entry.find('atom:link', ns).attrib['href']
            content_elem = entry.find('atom:content', ns)
            content = content_elem.text if content_elem is not None else ""
            entries.append((post_id, title, link, content))
    except Exception as e:
        print(f"  [raw-rss] Error for r/{subreddit}: {e}")
    
    return entries


def match_keywords(title: str, content: str) -> str:
    """Check if any keyword matches. Returns the matched keyword or None."""
    title_lower = (title or "").lower()
    content_lower = (content or "").lower()
    
    for kw in KEYWORDS:
        if kw in title_lower or kw in content_lower:
            return kw
    return None


def main():
    leads = []
    processed_path = os.path.join(BOT_DIR, "processed_leads.json")
    processed = []
    if os.path.exists(processed_path):
        with open(processed_path) as f:
            processed = json.load(f)
    
    print("=" * 50)
    print("[Agent-Reach] Fetching leads from Reddit")
    print("=" * 50)
    
    for sub in TARGET_SUBS:
        print(f"\nScanning r/{sub}...")
        
        # Layer 1: Try rdt-cli (Agent-Reach's Reddit CLI)
        entries = try_rdt_cli(sub)
        if entries:
            print(f"  OK Got {len(entries)} posts via rdt-cli")
        else:
            # Layer 2: Try feedparser (Agent-Reach bundled)
            if HAS_FEEDPARSER:
                entries = fetch_via_feedparser(sub)
                if entries:
                    print(f"  OK Got {len(entries)} posts via feedparser")
            
            # Layer 3: Raw RSS fallback
            if not entries:
                entries = fetch_via_raw_rss(sub)
                if entries:
                    print(f"  OK Got {len(entries)} posts via raw RSS")
        
        # Filter by keywords and check if already processed
        for post_id, title, url, content in entries:
            matched_kw = match_keywords(title, content)
            if matched_kw and post_id not in processed and post_id not in [l.get('id') for l in leads]:
                leads.append({
                    "sub": sub,
                    "query": matched_kw,
                    "title": title,
                    "url": url,
                    "id": post_id
                })
        
        # Random delay between subreddits (mimics human browsing)
        time.sleep(random.uniform(2, 5))
    
    print(f"\n{'=' * 50}")
    print(f"[Agent-Reach] Found {len(leads)} new leads across {len(TARGET_SUBS)} subreddits")
    print(f"{'=' * 50}")
    
    if leads:
        print("\n--- NEW LEADS ---")
        for lead in leads[:10]:  # Show first 10
            print(f"  r/{lead['sub']} | [{lead['query']}] {lead['title'][:60]}...")
    
    with open(os.path.join(BOT_DIR, "leads.json"), "w") as f:
        json.dump(leads, f, indent=2)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[Agent-Reach] Error fetching leads: {e}")
