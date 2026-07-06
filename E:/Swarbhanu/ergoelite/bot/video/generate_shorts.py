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
    os.makedirs(assets_dir, exist_ok=True)
    
    bg_file = os.path.join(assets_dir, "bg_music.mp3")
    
    # We captured 7 chairs
    for i in range(1, 8):
        print(f"\n--- Generating Video {i}/7 ---")
        script = (
            f"Stop buying the Herman Miller Aeron. Yes it's the best chair in the world, "
            f"but it costs seventeen hundred dollars. This is alternative number {i} that gives you "
            f"the exact same back support for a fraction of the price. Check the link in my bio "
            f"for the full ranked list and save a thousand bucks today."
        )
        
        audio_file = os.path.join(assets_dir, f"voiceover_{i}.mp3")
        video_file = os.path.join(assets_dir, f"tiktok_short_{i}.mp4")
        
        slide_data = [
            # Intro hook (0-5 seconds)
            {"path": os.path.join(assets_dir, "slide_hero.png"), "duration": 5.0},
            # Specific Chair (5-11 seconds)
            {"path": os.path.join(assets_dir, f"slide_chair_{i}.png"), "duration": 6.0},
            # CTA/End (Remaining time, loop back to hero)
            {"path": os.path.join(assets_dir, "slide_hero.png"), "duration": 5.0}
        ]
        
        # Verify the chair slide exists before rendering
        if not os.path.exists(slide_data[1]["path"]):
            print(f"Skipping video {i} because {slide_data[1]['path']} does not exist.")
            continue
            
        await generate_voiceover(script, audio_file)
        create_slideshow_video(slide_data, audio_file, bg_file, video_file)
        print(f"Video {i} ready: {video_file}")

if __name__ == "__main__":
    asyncio.run(main())
