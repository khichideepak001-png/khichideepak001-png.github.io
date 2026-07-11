import requests
import json

def upload_video():
    print("Uploading to tmpfiles.org...")
    url = "https://tmpfiles.org/api/v1/upload"
    with open("assets/tiktok_insta.mp4", "rb") as f:
        res = requests.post(url, files={"file": f})
        
    data = res.json()
    if data.get("status") == "success":
        # URL is like https://tmpfiles.org/12345/vid.mp4
        # Direct DL link is https://tmpfiles.org/dl/12345/vid.mp4
        orig_url = data["data"]["url"]
        direct_url = orig_url.replace("tmpfiles.org/", "tmpfiles.org/dl/")
        print(f"DIRECT_URL={direct_url}")
    else:
        print("Upload failed:", data)

if __name__ == "__main__":
    upload_video()
