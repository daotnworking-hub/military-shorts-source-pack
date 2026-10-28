import os
import sys
import subprocess
import json
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"C:\Users\Dao\Downloads\military_shorts"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

def main():
    print("=== STEP 1: CONCATENATING AUDIO ===")
    concat_file = os.path.join(AUDIO_DIR, "concat.txt")
    with open(concat_file, "w", encoding="utf-8") as f:
        f.write(f"file '{os.path.join(AUDIO_DIR, 's1.mp3').replace(chr(92), '/')}'\n")
        f.write(f"file '{os.path.join(AUDIO_DIR, 's2.mp3').replace(chr(92), '/')}'\n")
        f.write(f"file '{os.path.join(AUDIO_DIR, 's3.mp3').replace(chr(92), '/')}'\n")
    
    speech_full = os.path.join(AUDIO_DIR, "speech_full.mp3")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_file, "-c", "copy", speech_full
    ], check=True)
    
    # Get duration
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", speech_full]
    info = json.loads(subprocess.check_output(cmd))
    duration = float(info["format"]["duration"])
    print(f"Total Speech Duration: {duration:.2f}s")
    
    # Mix with BGM
    print("=== STEP 2: MIXING WITH BACKGROUND MUSIC ===")
    bgm_file = os.path.join(ASSETS_DIR, "bgm_epic.mp3")
    final_audio = os.path.join(AUDIO_DIR, "final_audio.mp3")
    fade_start = max(0, duration - 1.5)
    subprocess.run([
        "ffmpeg", "-y",
        "-i", speech_full,
        "-i", bgm_file,
        "-filter_complex", f"[1:a]volume=0.20,afade=t=out:st={fade_start:.2f}:d=1.5[bgm];[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]",
        "-map", "[aout]",
        "-b:a", "192k",
        final_audio
    ], check=True)
    print("Audio mixing complete!")

if __name__ == "__main__":
    main()
