import os
import subprocess
import json

BASE_DIR = r"C:\Users\Dao\Downloads\military_shorts"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

top_img = os.path.join(ASSETS_DIR, "top_leaders.jpg")
mid_img = os.path.join(ASSETS_DIR, "artillery_middle.jpg")
bot_img = os.path.join(ASSETS_DIR, "footer_banner.jpg")
audio_file = os.path.join(AUDIO_DIR, "final_audio.mp3")
ass_file = os.path.join(AUDIO_DIR, "subtitles.ass").replace("\\", "/")
output_video = os.path.join(OUTPUT_DIR, "video_military_short.mp4")

# Get exact duration of audio
cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", audio_file]
info = json.loads(subprocess.check_output(cmd))
duration = float(info["format"]["duration"])
fps = 30
total_frames = int(duration * fps) + 15
print(f"Target Duration: {duration:.2f}s ({total_frames} frames)")

# Subtitle file using relative path to avoid Windows drive colon escaping
filter_complex = f"""
[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:560,loop=loop={total_frames}:size=1:start=0,setpts=PTS-STARTPTS[top];
[1:v]zoompan=z='min(zoom+0.0006,1.25)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s=1080x820:fps={fps}[mid];
[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:540,loop=loop={total_frames}:size=1:start=0,setpts=PTS-STARTPTS[bot];
[top][mid][bot]vstack=inputs=3[stacked];
[stacked]drawbox=y=558:color=red@0.8:width=1080:height=4:t=fill,drawbox=y=1378:color=red@0.8:width=1080:height=4:t=fill,subtitles=filename='audio/subtitles.ass'[vout]
"""

ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-i", top_img,
    "-i", mid_img,
    "-i", bot_img,
    "-i", audio_file,
    "-filter_complex", filter_complex,
    "-map", "[vout]",
    "-map", "3:a",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-crf", "19",
    "-c:a", "aac",
    "-b:a", "192k",
    "-t", f"{duration:.2f}",
    "-pix_fmt", "yuv420p",
    output_video
]

print("Rendering video with FFmpeg...")
subprocess.run(ffmpeg_cmd, cwd=BASE_DIR, check=True)
print(f"Video generated successfully at: {output_video}")
