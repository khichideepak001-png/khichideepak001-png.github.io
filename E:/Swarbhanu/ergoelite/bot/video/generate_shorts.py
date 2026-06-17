import os
import asyncio
import edge_tts
from moviepy.editor import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips

async def generate_voiceover(text, output_path):
    print(f"Generating Voiceover: '{text[:30]}...'")
    communicate = edge_tts.Communicate(text, "en-US-ChristopherNeural")
    await communicate.save(output_path)
    print(f"Voiceover saved to {output_path}")

def create_slideshow_video(slide_data, audio_path, bg_music_path, output_path):
    print("Assembling the cinematic slideshow video...")
    
    # 1. Load Audio
    voice_clip = AudioFileClip(audio_path)
    total_duration = voice_clip.duration
    
    bg_clip = AudioFileClip(bg_music_path).fx(lambda clip: clip.volumex(0.1))
    if bg_clip.duration > total_duration:
        bg_clip = bg_clip.subclip(0, total_duration)
    
    final_audio = CompositeAudioClip([bg_clip, voice_clip])
    
    # 3. Create Slide Clips with custom durations and crossfades
    clips = []
    for data in slide_data:
        path = data['path']
        duration = data['duration']
        
        if os.path.exists(path):
            # Resize and crop to perfect 1080x1920 center to avoid distortion
            # We use crossfades instead of zooming to make it feel premium without breaking x264
            img_clip = (ImageClip(path)
                        .resize(width=1080)
                        .crop(x_center=540, y_center=960, width=1080, height=1920)
                        .set_duration(duration))
            clips.append(img_clip)
        else:
            print(f"Missing image: {path}")
            
    if not clips:
        print("Error: No valid slides found.")
        return
        
    # Apply crossfade to all clips except the first
    final_clips = [clips[0]]
    for clip in clips[1:]:
        final_clips.append(clip.crossfadein(0.5))
        
    # 4. Concatenate Slides
    video_track = concatenate_videoclips(final_clips, padding=-0.5, method="compose")
    
    # 5. Combine Video and Audio
    final_clip = video_track.set_audio(final_audio)
    
    # 6. Render
    final_clip.write_videofile(
        output_path, 
        fps=24, 
        codec="libx264", 
        audio_codec="aac",
        preset="ultrafast",
        threads=4
    )
    print(f"Video generation complete: {output_path}")

async def main():
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    artifacts_dir = r"C:\Users\deepa\.gemini\antigravity\brain\30c140c9-abcb-4d9f-a04c-96e38a11d532"
    os.makedirs(assets_dir, exist_ok=True)
    
    script = (
        "If you work from home and your wrist hurts after 5 hours at your desk, "
        "your standard mouse is twisting your median nerve. "
        "You need to use a vertical ergonomic mouse. It keeps your arm in a natural handshake position. "
        "Link in bio to get yours under 30 dollars."
    )
    
    audio_file = os.path.join(assets_dir, "voiceover.mp3")
    bg_file = os.path.join(assets_dir, "bg_music.mp3")
    video_file = os.path.join(assets_dir, "tiktok_short.mp4")
    
    # Custom timed slides matching the voiceover
    # Total script is ~11 seconds
    slide_data = [
        # Intro: Pain point (4 seconds)
        {"path": os.path.join(artifacts_dir, "wrist_pain_1781267641197.png"), "duration": 4.5},
        # Fix: Vertical Mouse (4 seconds)
        {"path": os.path.join(artifacts_dir, "vertical_mouse_1781267651356.png"), "duration": 4.5},
        # Call to Action: Website Product Card (Remaining time)
        {"path": os.path.join(assets_dir, "slide2.png"), "duration": 3.0}
    ]
    
    await generate_voiceover(script, audio_file)
    create_slideshow_video(slide_data, audio_file, bg_file, video_file)

if __name__ == "__main__":
    asyncio.run(main())
