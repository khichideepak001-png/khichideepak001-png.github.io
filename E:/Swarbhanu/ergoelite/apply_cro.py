import os
from bs4 import BeautifulSoup

def process_html_file(filepath):
    print(f"Processing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    modified = False
    
    # 1. Update Comparison Tables
    tables = soup.find_all('table', class_='comparison-table')
    for table in tables:
        # Check if we already added it
        thead_tr = table.find('thead').find('tr')
        if thead_tr and "Check Price" not in thead_tr.text:
            new_th = soup.new_tag("th")
            new_th.string = "Action"
            thead_tr.append(new_th)
            
            tbody_trs = table.find('tbody').find_all('tr')
            for tr in tbody_trs:
                new_td = soup.new_tag("td")
                new_a = soup.new_tag("a", href="https://amazon.com?tag=viralbraintea-20", target="_blank", rel="nofollow noopener")
                new_a['class'] = "btn btn-primary btn-sm"
                new_a.string = "Check Price"
                new_td.append(new_a)
                tr.append(new_td)
            modified = True
            
    # 2. Early Link Injection
    article = soup.find('article')
    if article:
        fade_ins = article.find_all('div', class_='fade-in')
        # Find the first fade-in that has a paragraph (this is usually the intro)
        for fade_in in fade_ins:
            first_p = fade_in.find('p')
            if first_p and "In a hurry?" not in str(first_p):
                # We found the intro paragraph. Inject the early link.
                early_link_html = BeautifulSoup(' <br><br><strong>⏳ In a hurry? <a href="https://amazon.com?tag=viralbraintea-20" target="_blank" rel="nofollow noopener">Check out our #1 Top Pick on Amazon.</a></strong>', 'html.parser')
                first_p.append(early_link_html)
                modified = True
                break # Only inject once
                
    # 3. Make Images Clickable
    if article:
        images = article.find_all('img')
        for img in images:
            # Check if parent is an 'a' tag
            if img.parent.name != 'a':
                # Skip tiny icons or avatars if they exist, but we assume article images are product images
                if "hero" in img.get('src', '') or "photo" in img.get('src', ''):
                    new_a = soup.new_tag("a", href="https://amazon.com?tag=viralbraintea-20", target="_blank", rel="nofollow noopener")
                    # Replace img with the wrapper
                    img.wrap(new_a)
                    modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Updated {filepath}")

def main():
    reviews_dir = os.path.join(os.path.dirname(__file__), 'reviews')
    for filename in os.listdir(reviews_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(reviews_dir, filename)
            process_html_file(filepath)

if __name__ == "__main__":
    main()
