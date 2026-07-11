import os
from instagrapi import Client

# --- INSTAGRAM CREDENTIALS ---
USERNAME = "Digital.Alchemist9"
PASSWORD = "romeo#123"

def upload_to_instagram():
    video_path = os.path.join(os.path.dirname(__file__), "assets", "tiktok_insta.mp4")
    
    caption = (
        "Stop buying the Herman Miller Aeron 🛑 Do THIS instead. \n\n"
        "Check out the link in my bio for the full ranked list of budget ergonomic chairs! \n\n"
        "#ergonomics #desksetup #workfromhome #hermanmiller #officechair"
    )
    
    print(f"Logging into Instagram as {USERNAME}...")
    
    cl = Client()
    # Login
    try:
        cl.login(USERNAME, PASSWORD)
        print("Login successful! Uploading video to Reels...")
        
        # Upload Reel
        media = cl.clip_upload(
            video_path,
            caption
        )
        print("Upload successful! Reel URL:", media.video_url)
    except Exception as e:
        print("Error uploading to Instagram via Instagrapi:", e)

if __name__ == "__main__":
    if USERNAME == "YOUR_INSTAGRAM_USERNAME":
        print("Please edit this file and put your Instagram Username and Password in!")
    else:
        upload_to_instagram()
