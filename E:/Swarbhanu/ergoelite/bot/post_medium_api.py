import requests
import json
import os

def post_to_medium(integration_token, title, content_html, tags):
    """
    Publish an article to Medium using the official API to rank quickly on Google.
    """
    print("Connecting to Medium API...")
    headers = {
        "Authorization": f"Bearer {integration_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Accept-Charset": "utf-8"
    }
    
    # 1. Get the User ID
    user_url = "https://api.medium.com/v1/me"
    user_res = requests.get(user_url, headers=headers)
    
    if user_res.status_code != 200:
        print(f"Error authenticating with Medium: {user_res.text}")
        return False
        
    author_id = user_res.json()['data']['id']
    print(f"Authenticated as Author ID: {author_id}")
    
    # 2. Publish the Post
    post_url = f"https://api.medium.com/v1/users/{author_id}/posts"
    
    # The payload uses our existing HTML structure and includes the canonical URL
    payload = {
        "title": title,
        "contentFormat": "html",
        "content": content_html,
        "canonicalUrl": "https://khichideepak001-png.github.io/reviews/herman-miller-alternatives.html",
        "tags": tags,
        "publishStatus": "public" 
    }
    
    pub_res = requests.post(post_url, headers=headers, json=payload)
    
    if pub_res.status_code in [200, 201]:
        data = pub_res.json().get('data', {})
        print(f"SUCCESS! Article published to Medium.")
        print(f"URL: {data.get('url')}")
        return True
    else:
        print(f"Failed to publish: {pub_res.text}")
        return False

if __name__ == "__main__":
    # You will need to fill this in from Medium Settings -> Security and Apps
    MEDIUM_TOKEN = "YOUR_MEDIUM_INTEGRATION_TOKEN_HERE"
    
    # Read the HTML we generated earlier to use as the Medium post body
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    html_file = os.path.join(base_path, "reviews", "herman-miller-alternatives.html")
    
    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    # We want to inject the raw HTML, but Medium API handles standard HTML tags well.
    # We'll just pass the body contents.
    body_start = html_content.find("<body>")
    body_end = html_content.find("</body>")
    if body_start != -1 and body_end != -1:
        clean_html = html_content[body_start:body_end]
    else:
        clean_html = html_content
        
    # Add a CTA at the very top for affiliate clicks
    cta_header = (
        "<h1>7 Herman Miller Alternatives That Are Just As Good (2026)</h1>"
        "<p><i>This article originally appeared on <a href='https://khichideepak001-png.github.io'>ErgoElite</a>.</i></p>"
        "<hr>"
    )
    final_content = cta_header + clean_html

    tags = ["Ergonomics", "Work From Home", "Office Setup", "Productivity", "Tech"]
    
    if MEDIUM_TOKEN != "YOUR_MEDIUM_INTEGRATION_TOKEN_HERE":
        post_to_medium(MEDIUM_TOKEN, "7 Herman Miller Alternatives That Will Save Your Back and Your Wallet", final_content, tags)
    else:
        print("Please configure your MEDIUM_TOKEN in the script.")
