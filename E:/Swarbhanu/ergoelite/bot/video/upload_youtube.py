import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

scopes = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    # Use the renamed client_secrets file
    client_secrets_file = os.path.join(os.path.dirname(__file__), "client_secrets.json")
    token_file = os.path.join(os.path.dirname(__file__), "token.json")
    
    credentials = None
    # Load existing credentials if available
    if os.path.exists(token_file):
        credentials = Credentials.from_authorized_user_file(token_file, scopes)
        
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            print("Opening browser for YouTube authentication...")
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, scopes)
            credentials = flow.run_local_server(port=0, open_browser=False)
            
        # Save the credentials for the next run so it's fully autonomous
        with open(token_file, "w") as f:
            f.write(credentials.to_json())
            
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    return youtube

def upload_video(youtube, file_path, title, description, tags):
    print(f"Uploading {file_path} to YouTube Shorts...")
    
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "22" # People & Blogs (or 26 How-to & Style)
        },
        "status": {
            "privacyStatus": "private", # We use 'private' for the initial test so you can verify it
            "selfDeclaredMadeForKids": False
        }
    }
    
    # Since it's a short, we ensure it's under 60 seconds (already handled by generation)
    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )
    
    response = None
    while response is None:
        status, response = insert_request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")
            
    print(f"Upload Complete! Video ID: {response['id']}")
    return response['id']

if __name__ == "__main__":
    youtube_service = get_authenticated_service()
    
    video_path = os.path.join(os.path.dirname(__file__), "assets", "tiktok_short.mp4")
    
    title = "Stop buying the Herman Miller Aeron 🛑 Do THIS instead. #shorts #ergonomics"
    description = (
        "Don't spend $1,700 on a Herman Miller chair until you check out these budget alternatives!\n\n"
        "Check out the full ranked list here: https://khichideepak001-png.github.io/reviews/herman-miller-alternatives.html \n\n"
        "These chairs provide the exact same back support for under $400. Save your spine and your wallet!"
    )
    tags = ["ergonomics", "desk setup", "work from home", "herman miller", "office chair", "tech"]
    
    if os.path.exists(video_path):
        upload_video(youtube_service, video_path, title, description, tags)
    else:
        print(f"Error: Could not find video file at {video_path}")
