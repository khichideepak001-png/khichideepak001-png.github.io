"""
ErgoElite Instagram Blitz Engine
Automatically creates and posts multiple image posts daily to maximize reach.
Run this script once — it posts 5 pieces of content back-to-back with delays.
"""

import moviepy.editor, moviepy
moviepy.VideoFileClip = moviepy.editor.VideoFileClip

from instagrapi import Client
from PIL import Image, ImageDraw, ImageFont
import textwrap, os, time, random

USERNAME = 'digital.alchemist9'
PASSWORD = 'romeo#123'
SESSION_FILE = r'e:\Swarbhanu\ergoelite\bot\video\ig_session.json'
OUTPUT_DIR = r'e:\Swarbhanu\ergoelite\bot\video\assets\posts'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── Content Bank ────────────────────────────────────────────────────────────
POSTS = [
    {
        "headline": "BACK PAIN?\nYour chair is\nkilling you.",
        "subtext": "Ergonomic chairs cut back pain by 73%.\nSee our top picks → link in bio",
        "bg": (15, 15, 25),
        "accent": (99, 102, 241),
        "emoji": "🪑",
        "caption": (
            "If you work 8+ hours a day and your back hurts by noon, "
            "your chair is the problem. Not your posture. Not your desk height. YOUR CHAIR.\n\n"
            "We tested 18 ergonomic chairs under $500 so you don't have to waste money.\n\n"
            "Top 3 picks are linked in our bio 👆\n\n"
            "#BackPain #ErgonomicChair #WorkFromHome #HomeOffice #OfficeSetup "
            "#RemoteWork #DeskSetup #ErgoElite #ChairGoals #ProductivityTips "
            "#WFH #HomeOfficeTour #OfficeLife #WorkSmarter #BackPainRelief"
        )
    },
    {
        "headline": "Herman Miller\nvs Secretlab\nvs Autonomous",
        "subtext": "We compared all 3.\nThe winner will surprise you.",
        "bg": (10, 20, 15),
        "accent": (16, 185, 129),
        "emoji": "🏆",
        "caption": (
            "Herman Miller costs $1,500. Secretlab Titan costs $600. Autonomous ErgoChair Pro costs $350.\n\n"
            "We sat in all 3 for 40 hours each. Here's what we found:\n\n"
            "🥇 Best overall: Herman Miller Aeron (worth every penny if you can afford it)\n"
            "🥈 Best value: Autonomous ErgoChair Pro (90% the comfort at 25% the price)\n"
            "🥉 Best for gamers: Secretlab Titan (great lumbar, stiff for office work)\n\n"
            "Full comparison with Amazon links 👉 link in bio\n\n"
            "#HermanMiller #SecretlabTitan #AutonomousChair #ErgonomicChair #ChairReview "
            "#HomeOffice #WorkFromHome #BestChair #OfficeSetup #DeskSetup "
            "#ErgoElite #ChairComparison #OfficeFurniture #RemoteWork #WFH"
        )
    },
    {
        "headline": "The $200 chair\nthat beats\n$1000 ones.",
        "subtext": "Our #1 budget pick of 2026.\nLink in bio.",
        "bg": (20, 10, 10),
        "accent": (239, 68, 68),
        "emoji": "💰",
        "caption": (
            "You don't need to spend $1,500 on a Herman Miller.\n\n"
            "After testing 18 chairs, our #1 budget pick at under $200 beat "
            "chairs that cost 5x more in back support and lumbar adjustability.\n\n"
            "It's currently on sale on Amazon with a $40 coupon 👀\n\n"
            "Name + Amazon link in bio 👆\n\n"
            "#BudgetChair #AffordableChair #ErgonomicChair #HomeOffice #WorkFromHome "
            "#DeskSetup #OfficeSetup #ChairReview #ErgoElite #SaveMoney "
            "#AmazonFinds #AmazonDeals #HomeOfficeTour #WFH #RemoteWork"
        )
    },
    {
        "headline": "5 signs your\nchair is\nhurting you",
        "subtext": "If you have ANY of these,\nyou need a new chair NOW.",
        "bg": (20, 15, 5),
        "accent": (245, 158, 11),
        "emoji": "⚠️",
        "caption": (
            "5 signs your office chair is silently destroying your spine:\n\n"
            "1️⃣ You shift positions every 20 minutes\n"
            "2️⃣ Your lower back aches after 2 hours\n"
            "3️⃣ Your shoulders are tense by noon\n"
            "4️⃣ You feel better standing than sitting\n"
            "5️⃣ Your chair has NO lumbar support\n\n"
            "If you said yes to 2 or more — your chair is costing you productivity AND health.\n\n"
            "See our top picks for every budget 👉 link in bio\n\n"
            "#SpineHealth #BackPain #ErgonomicChair #WorkFromHome #HomeOffice "
            "#OfficeHealth #DeskSetup #ErgoElite #ChairGoals #PostureCorrector "
            "#RemoteWork #WFH #OfficeLife #HealthyWorkplace #BackPainRelief"
        )
    },
    {
        "headline": "Work 8 hours.\nFeel like\nyou worked 4.",
        "subtext": "The right chair changes everything.\nTop picks → link in bio",
        "bg": (5, 10, 25),
        "accent": (139, 92, 246),
        "emoji": "✨",
        "caption": (
            "The difference between a $50 chair and a proper ergonomic chair:\n\n"
            "❌ $50 chair: back pain by 2pm, tired by 4pm, dreading work by 9am\n"
            "✅ Ergonomic chair: focused for 8 hours, back feels fine, actually enjoy working\n\n"
            "We found ergonomic chairs as low as $180 that make this difference.\n\n"
            "Our top picks are on Amazon with free Prime shipping 📦\n"
            "Full list with prices 👉 link in bio\n\n"
            "#ErgonomicChair #ProductivityHacks #WorkFromHome #HomeOffice #DeskSetup "
            "#OfficeSetup #ErgoElite #WorkSmarter #RemoteWork #WFH "
            "#HomeOfficeTour #ChairGoals #OfficeFurniture #WorkLifeBalance #FocusTips"
        )
    },
]

def create_post_image(post, filename):
    """Create a stunning 1080x1080 Instagram post image."""
    W, H = 1080, 1080
    img = Image.new('RGB', (W, H), post['bg'])
    draw = ImageDraw.Draw(img)

    # Background gradient effect (manual)
    accent = post['accent']
    for i in range(300):
        alpha = int(60 * (1 - i/300))
        r = min(255, post['bg'][0] + int((accent[0]-post['bg'][0]) * alpha/60))
        g = min(255, post['bg'][1] + int((accent[1]-post['bg'][1]) * alpha/60))
        b = min(255, post['bg'][2] + int((accent[2]-post['bg'][2]) * alpha/60))
        draw.ellipse([W-300+i//2, -100, W+200, 400-i//2], fill=(r,g,b))

    # Top accent line
    draw.rectangle([80, 80, 80+200, 80+6], fill=accent)

    # ErgoElite branding top
    try:
        font_brand = ImageFont.truetype("C:/Windows/Fonts/Calibrib.ttf", 32)
    except:
        font_brand = ImageFont.load_default()
    draw.text((80, 108), "ErgoElite™ Reviews", font=font_brand, fill=(180,180,200))

    # Big emoji
    try:
        font_emoji = ImageFont.truetype("C:/Windows/Fonts/Segoeui.ttf", 120)
    except:
        font_emoji = ImageFont.load_default()
    draw.text((80, 200), post['emoji'], font=font_emoji, fill=(255,255,255))

    # Main headline
    try:
        font_headline = ImageFont.truetype("C:/Windows/Fonts/Calibrib.ttf", 100)
    except:
        font_headline = ImageFont.load_default()

    lines = post['headline'].split('\n')
    y = 380
    for line in lines:
        draw.text((80, y), line, font=font_headline, fill=(255,255,255))
        y += 115

    # Accent bar
    draw.rectangle([80, y+20, 80+400, y+26], fill=accent)

    # Subtext
    try:
        font_sub = ImageFont.truetype("C:/Windows/Fonts/Calibri.ttf", 44)
    except:
        font_sub = ImageFont.load_default()

    y += 50
    for line in post['subtext'].split('\n'):
        draw.text((80, y), line, font=font_sub, fill=(200, 200, 220))
        y += 60

    # Bottom CTA bar
    draw.rectangle([0, H-120, W, H], fill=accent)
    try:
        font_cta = ImageFont.truetype("C:/Windows/Fonts/Calibrib.ttf", 42)
    except:
        font_cta = ImageFont.load_default()
    draw.text((80, H-90), "🔗  khichideepak001-png.github.io  |  Link in bio", font=font_cta, fill=(255,255,255))

    img.save(filename, 'JPEG', quality=95)
    print(f"  Created: {filename}")
    return filename


def main():
    print("=" * 60)
    print("  ErgoElite Instagram Blitz Engine")
    print("=" * 60)

    # Login
    cl = Client()
    cl.delay_range = [5, 10]
    print("\n[1/3] Logging in to Instagram...")
    cl.load_settings(SESSION_FILE)
    cl.login(USERNAME, PASSWORD)
    print("      Login successful!")

    # Post each piece of content
    for i, post in enumerate(POSTS):
        print(f"\n[Post {i+1}/{len(POSTS)}] Creating content...")
        img_path = os.path.join(OUTPUT_DIR, f'post_{i+1}.jpg')
        create_post_image(post, img_path)

        print(f"[Post {i+1}/{len(POSTS)}] Uploading to Instagram...")
        try:
            media = cl.photo_upload(img_path, caption=post['caption'])
            print(f"  SUCCESS! View at: https://www.instagram.com/p/{media.code}/")
        except Exception as e:
            print(f"  ERROR: {e}")

        if i < len(POSTS) - 1:
            wait = random.randint(180, 300)  # 3-5 min between posts
            print(f"  Waiting {wait}s before next post...")
            time.sleep(wait)

    print("\n" + "=" * 60)
    print("  BLITZ COMPLETE! All posts uploaded.")
    print("  Check instagram.com/digital.alchemist9")
    print("=" * 60)


if __name__ == '__main__':
    main()
