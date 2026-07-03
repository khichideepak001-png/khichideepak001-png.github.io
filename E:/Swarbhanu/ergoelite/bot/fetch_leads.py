import urllib.request
import xml.etree.ElementTree as ET
import json
import os
import sys
import time

def main():
    target_subs = [
        "OfficeChairs", "StandingDesk", "workfromhome", "desksetup",
        "homeoffice", "Ergonomics", "BackPain", "remotework",
        "battlestations", "WFH", "pcmasterrace"
    ]
    leads = []
    
    # High-intent keywords targeting actual purchase/pain queries
    keywords = [
        "standing desk", "sit stand desk", "adjustable desk", "motorized desk",
        "ergonomic chair", "office chair", "desk chair", "task chair",
        "herman miller", "steelcase", "flexispot", "uplift", "autonomous", "secretlab",
        "posture", "lumbar support", "sciatica", "back pain sitting", "neck pain desk",
        "wrist pain typing", "carpal tunnel", "monitor arm", "keyboard tray",
        "best chair under", "chair recommendation", "desk recommendation",
        "work from home setup", "home office setup", "wfh gear",
        "8 hours sitting", "comfortable chair", "mesh chair"
    ]
    
    print("Fetching new leads via RSS backdoor...")
    
    for sub in target_subs:
        url = f"https://www.reddit.com/r/{sub}/new.rss"
        print(f"Scanning r/{sub} feed...")
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 ErgoBot/{sub}'}
        )
        try:
            time.sleep(5)
            response = urllib.request.urlopen(req).read()
            root = ET.fromstring(response)
            
            # XML namespace for atom
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            for entry in root.findall('atom:entry', ns):
                title = entry.find('atom:title', ns).text
                link = entry.find('atom:link', ns).attrib['href']
                post_id = entry.find('atom:id', ns).text
                content_elem = entry.find('atom:content', ns)
                content = content_elem.text if content_elem is not None else ""
                
                title_lower = (title or "").lower()
                content_lower = (content or "").lower()
                
                # Check if any broad keyword matches
                matched_query = None
                for kw in keywords:
                    if kw in title_lower or kw in content_lower:
                        matched_query = kw
                        break
                        
                if matched_query and post_id not in [l.get('id') for l in leads]:
                    leads.append({
                        "sub": sub,
                        "query": matched_query,
                        "title": title,
                        "url": link,
                        "id": post_id
                    })
                    
        except Exception as e:
            print(f"Failed to fetch r/{sub}: {e}")
            
    print("\n--- NEW LEADS ---")
    print(json.dumps(leads, indent=2))
    
    with open(os.path.join(os.path.dirname(__file__), "leads.json"), "w") as f:
        json.dump(leads, f, indent=2)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error fetching leads: {e}")
