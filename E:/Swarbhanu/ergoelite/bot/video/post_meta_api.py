import os
import requests
import time
import json

def upload_to_instagram_reels(access_token, ig_user_id, video_url, caption):
    """
    Uploads a video to Instagram Reels via the official Meta Graph API.
    Note: The video MUST be hosted on a public URL for Meta to fetch it.
    """
    print(f"Uploading Reel to Instagram Account {ig_user_id}...")
    
    # Step 1: Initialize the upload container
    url = f"https://graph.facebook.com/v19.0/{ig_user_id}/media"
    payload = {
        'media_type': 'REELS',
        'video_url': video_url,
        'caption': caption,
        'access_token': access_token
    }
    
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Error initializing upload: {response.text}")
        return False
        
    creation_id = response.json().get('id')
    print(f"Upload container created. ID: {creation_id}")
    
    # Step 2: Wait for Meta to process the video (can take up to a minute)
    status_url = f"https://graph.facebook.com/v19.0/{creation_id}?fields=status_code&access_token={access_token}"
    
    for attempt in range(15):
        time.sleep(10)
        status_res = requests.get(status_url)
        status = status_res.json().get('status_code')
        print(f"Processing status: {status}...")
        
        if status == 'FINISHED':
            break
        elif status == 'ERROR':
            print("Meta encountered an error processing the video.")
            return False
            
    # Step 3: Publish the Reel
    publish_url = f"https://graph.facebook.com/v19.0/{ig_user_id}/media_publish"
    publish_payload = {
        'creation_id': creation_id,
        'access_token': access_token
    }
    
    pub_res = requests.post(publish_url, data=publish_payload)
    if pub_res.status_code == 200:
        print(f"Successfully published Reel! ID: {pub_res.json().get('id')}")
        return True
    else:
        print(f"Error publishing Reel: {pub_res.text}")
        return False

if __name__ == "__main__":
    # --- CONFIGURATION ---
    ACCESS_TOKEN = "EAAVBQC1NZBLMBR3DZBaXdGcYQJA8PhelINYTRIUXhmt74QdZBNZBIw7NoeEQmcjEKfT2GnWZAiNdNPKBZAA4SZCvx1dzW1thwKFP4VYOb0uhkBJ5NgiO0IThwnQurR7lavDO8vcOmYl3b2jiSagJO226aBIcVjejDdeqKOMP8B0iamjSIQsbvrL7bxoZCFtKTPFMG6w11oyHbqKbTZBQEgqrqZCRSZAzZAZA1nLjl60m7G3kZD"
    IG_USER_ID = "17841434096813307"
    
    # Meta Graph API requires the video to be hosted on a public URL.
    PUBLIC_VIDEO_URL = "https://khichideepak001-png.github.io/bot/video/assets/tiktok_short_1.mp4"
    
    CAPTION = (
        "Stop buying the Herman Miller Aeron 🛑 Do THIS instead. \n\n"
        "Check out the link in my bio for the full ranked list of budget ergonomic chairs! \n\n"
        "#ergonomics #desksetup #workfromhome #hermanmiller #officechair"
    )
    
    upload_to_instagram_reels(ACCESS_TOKEN, IG_USER_ID, PUBLIC_VIDEO_URL, CAPTION)
