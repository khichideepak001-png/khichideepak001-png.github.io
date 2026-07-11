import requests

def upload_video():
    print("Uploading to bashupload.com...")
    with open("assets/tiktok_insta.mp4", "rb") as f:
        res = requests.post("https://bashupload.com", files={"file": f})
        print(res.text)

if __name__ == "__main__":
    upload_video()
