import os
import re

root_nav = """<nav class="nav">
  <div class="container">
    <div class="nav-inner">
      <a href="index.html" class="nav-logo">Ergo<span>Elite</span></a>
      <ul class="nav-links" id="navLinks">
        <li><a href="index.html">Home</a></li>
        <li><a href="reviews/best-standing-desks.html">Standing Desks</a></li>
        <li><a href="reviews/best-ergonomic-chairs.html">Chairs</a></li>
        <li><a href="reviews/accessories.html">Accessories</a></li>
        <li><a href="reviews/home-office-setup-guide.html">Setup Guide</a></li>
        <li><a href="blog.html">Blog</a></li>
      </ul>
      <div class="nav-cta" id="navCta">
        <a href="reviews/best-standing-desks.html" class="btn btn-primary btn-sm">Best Picks →</a>
      </div>
      <button class="hamburger" id="hamburger" aria-label="Toggle menu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</nav>"""

review_nav = """<nav class="nav">
  <div class="container">
    <div class="nav-inner">
      <a href="../index.html" class="nav-logo">Ergo<span>Elite</span></a>
      <ul class="nav-links" id="navLinks">
        <li><a href="../index.html">Home</a></li>
        <li><a href="best-standing-desks.html">Standing Desks</a></li>
        <li><a href="best-ergonomic-chairs.html">Chairs</a></li>
        <li><a href="accessories.html">Accessories</a></li>
        <li><a href="home-office-setup-guide.html">Setup Guide</a></li>
        <li><a href="../blog.html">Blog</a></li>
      </ul>
      <div class="nav-cta" id="navCta">
        <a href="best-standing-desks.html" class="btn btn-primary btn-sm">Best Picks →</a>
      </div>
      <button class="hamburger" id="hamburger" aria-label="Toggle menu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</nav>"""

nav_regex = re.compile(r'<nav class="nav">.*?</nav>', re.DOTALL)

for file in os.listdir('.'):
    if file.endswith('.html'):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = nav_regex.sub(root_nav, content)
        if new_content != content:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {file}")

review_dir = 'reviews'
if os.path.exists(review_dir):
    for file in os.listdir(review_dir):
        if file.endswith('.html'):
            filepath = os.path.join(review_dir, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = nav_regex.sub(review_nav, content)
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {filepath}")
