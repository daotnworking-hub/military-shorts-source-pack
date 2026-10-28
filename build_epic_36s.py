import os
import subprocess
import json

BASE_DIR = r"C:\Users\Dao\Downloads\military_shorts"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
CUTS_DIR = os.path.join(ASSETS_DIR, "cuts_36s")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    print("=== STEP 1: CONCATENATING 12 ACTION CUTS (36 SECONDS) ===")
    concat_list = os.path.join(CUTS_DIR, "concat_list.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        for i in range(1, 13):
            f.write(f"file 'cut_{i:02d}.mp4'\n")
    
    merged_raw = os.path.join(ASSETS_DIR, "merged_raw.mp4")
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list,
        "-c", "copy",
        merged_raw
    ]
    subprocess.run(cmd_concat, cwd=CUTS_DIR, check=True)
    print("[+] Merged 12 cuts successfully.")

    print("\n=== STEP 2: PREPARING EPIC SOUNDTRACK & RISER ===")
    bgm_in = os.path.join(ASSETS_DIR, "bgm_epic.mp3")
    audio_out = os.path.join(ASSETS_DIR, "soundtrack_36s.mp3")
    
    # 36 seconds of high energy music: Boost bass (+3dB at 80Hz) and treble for movie trailer punch
    # Fade out last 1.5 seconds
    af_filter = (
        "bass=g=4:f=90,"
        "treble=g=2:f=3000,"
        "afade=t=out:st=34.5:d=1.5,"
        "volume=0.9"
    )
    cmd_audio = [
        "ffmpeg", "-y",
        "-ss", "0.0",
        "-i", bgm_in,
        "-t", "36.0",
        "-af", af_filter,
        "-b:a", "256k",
        audio_out
    ]
    subprocess.run(cmd_audio, check=True)
    print("[+] Master soundtrack prepared.")

    print("\n=== STEP 3: MASTER COMPOSITING (HUD + OPENING HOOK + AUDIO) ===")
    title_hook = os.path.join(ASSETS_DIR, "title_hook.png")
    overlay_hud = os.path.join(ASSETS_DIR, "overlay_hud.png")
    final_output = os.path.join(OUTPUT_DIR, "video_military_epic_36s.mp4")

    # Filter complex:
    # 1. Overlay opening title with fade out at 3.0s: enable='between(t,0,3.2)'
    # 2. Overlay HUD watermark throughout the video
    filter_complex = (
        "[0:v][1:v]overlay=0:0:enable='between(t,0,3.2)'[v1];"
        "[v1][2:v]overlay=0:0[vout]"
    )

    cmd_master = [
        "ffmpeg", "-y",
        "-i", merged_raw,
        "-i", title_hook,
        "-i", overlay_hud,
        "-i", audio_out,
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-map", "3:a",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", "36.0",
        "-pix_fmt", "yuv420p",
        final_output
    ]
    subprocess.run(cmd_master, check=True)
    print("\n" + "=" * 60)
    print(f"[HOAN TAT] Video xuat thanh cong tai:\n{final_output}")
    print("=" * 60)

if __name__ == "__main__":
    main()
