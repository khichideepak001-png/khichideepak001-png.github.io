import os
import asyncio
import edge_tts
from moviepy.editor import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips

async def generate_voiceover(text, output_path):
    print(f"Generating High-Energy Voiceover: '{text[:30]}...'")
    # Swapped to a male, highly energetic voice and bumped the speed by 15%
    communicate = edge_tts.Communicate(text, "en-US-AndrewMultilingualNeural", rate="+15%")
    await communicate.save(output_path)
    print(f"Voiceover saved to {output_path}")

def create_fast_paced_video(slide_data, audio_path, bg_music_path, output_path):
    print("Assembling the fast-paced, high-retention video...")
    
    # 1. Load Audio
    voice_clip = AudioFileClip(audio_path)
    total_duration = voice_clip.duration
    
    # 2. Punchier Background Music (25% volume instead of 10%)
    bg_clip = AudioFileClip(bg_music_path).fx(lambda clip: clip.volumex(0.25))
    if bg_clip.duration > total_duration:
        bg_clip = bg_clip.subclip(0, total_duration)
    
    final_audio = CompositeAudioClip([bg_clip, voice_clip])
    
    # 3. Create Slide Clips with Hard Cuts
    clips = []
    current_time = 0
    for data in slide_data:
        path = data['path']
        duration = data['duration']
        
        # Adjust last slide to fill remaining time exactly
        if data == slide_data[-1]:
            duration = max(1.0, total_duration - current_time)
            
        if os.path.exists(path):
            img_clip = (ImageClip(path)
                        .resize(width=1080)
                        .crop(x_center=540, y_center=960, width=1080, height=1920)
                        .set_duration(duration))
            clips.append(img_clip)
            current_time += duration
        else:
            print(f"Missing image asset, skipping frame: {path}")
            
    if not clips:
        print("Error: No valid slides found.")
        return
        
    # 4. Concatenate Slides (Hard cuts trigger dopamine and retain attention)
    video_track = concatenate_videoclips(clips, method="compose")
    video_track = video_track.set_duration(total_duration)
    
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
    bg_file = os.path.join(assets_dir, "bg_music.mp3")
    
    for i in range(1, 8):
        print(f"\n--- Generating High-Engagement Video {i}/7 ---")
        script = (
            f"Stop buying the Herman Miller Aeron! Yes, it's a great chair, "
            f"but it costs over fifteen hundred dollars. This is alternative number {i}, and it gives you "
            f"the exact same ergonomic back support for a fraction of the price. "
            f"Check the link in my bio for the full ranked list and save yourself a thousand bucks today!"
        )
        
        audio_file = os.path.join(assets_dir, f"voiceover_{i}.mp3")
        video_file = os.path.join(assets_dir, f"tiktok_short_{i}.mp4")
        
        # Balanced pacing: Focus heavily on the chair and website info
        slide_data = [
            {"path": os.path.join(assets_dir, "herman_miller.png"), "duration": 2.0},
            {"path": os.path.join(assets_dir, f"slide_chair_{i}.png"), "duration": 3.5},
            {"path": os.path.join(assets_dir, "website_broll.png"), "duration": 3.0},
            {"path": os.path.join(assets_dir, f"slide_chair_{i}.png"), "duration": 3.5},
            {"path": os.path.join(assets_dir, "slide1.png"), "duration": 2.0},
            {"path": os.path.join(assets_dir, f"slide_chair_{i}.png"), "duration": 5.0} # Fills the rest
        ]
        
        if not os.path.exists(slide_data[2]["path"]):
            print(f"Skipping video {i} because {slide_data[2]['path']} does not exist.")
            continue
            
        await generate_voiceover(script, audio_file)
        create_fast_paced_video(slide_data, audio_file, bg_file, video_file)
        print(f"Video {i} ready: {video_file}")
        
        # The script will now loop and generate all 7 videos

if __name__ == "__main__":
    asyncio.run(main())
