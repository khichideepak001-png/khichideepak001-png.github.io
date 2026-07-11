import os
import subprocess

def fix_video_for_instagram():
    input_file = "assets/tiktok_short_1.mp4"
    output_file = "assets/tiktok_insta.mp4"
    
    print(f"Fixing pixel format for {input_file}...")
    
    # We use moviepy's internal ffmpeg if it's available, or just call ffmpeg
    from moviepy.config import get_setting
    ffmpeg_exe = get_setting("FFMPEG_BINARY")
    
    cmd = [
        ffmpeg_exe, 
        "-y", 
        "-i", input_file, 
        "-c:v", "libx264", 
        "-pix_fmt", "yuv420p", 
        "-c:a", "aac", 
        "-movflags", "+faststart", 
        output_file
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("Successfully fixed video format for Instagram!")
    except Exception as e:
        print(f"Error running ffmpeg: {e}")

if __name__ == "__main__":
    fix_video_for_instagram()
