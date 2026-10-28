import os
import sys
import subprocess

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE_DIR = r"C:\Users\Dao\Downloads\military_shorts"
NGANG_DIR = os.path.join(BASE_DIR, "source_ngang")
TEMP_DIR = os.path.join(BASE_DIR, "assets", "temp_ngang")
os.makedirs(TEMP_DIR, exist_ok=True)

# 5 horizontal videos downloaded
videos = sorted([f for f in os.listdir(NGANG_DIR) if f.endswith(".mp4")])
print(f"Found {len(videos)} horizontal videos.")

# Extract 4-minute best action highlights from each video (total 20 minutes)
cut_list = []
for idx, v in enumerate(videos, 1):
    src = os.path.join(NGANG_DIR, v)
    out_cut = os.path.join(TEMP_DIR, f"highlight_{idx:02d}.mp4")
    
    # Take 240 seconds (4 minutes) starting from minute 1:30 (where core action/battle footage begins)
    cmd = [
        "ffmpeg", "-y",
        "-ss", "90.0",
        "-i", src,
        "-t", "240.0",
        "-c:v", "libx264", "-preset", "faster", "-crf", "24",
        "-c:a", "aac", "-b:a", "128k",
        out_cut
    ]
    print(f"[*] Extracting 4-min highlight from {v[:40]}...")
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    cut_list.append(out_cut)

# Concat 5 highlights into 1 Master Horizontal Video (~20 mins, ~75MB)
concat_txt = os.path.join(TEMP_DIR, "concat_ngang.txt")
with open(concat_txt, "w", encoding="utf-8") as f:
    for c in cut_list:
        f.write(f"file '{c.replace(chr(92), '/')}'\n")

out_master_ngang = os.path.join(BASE_DIR, "MASTER_SOURCE_NGANG_20MINS.mp4")
print("\n[*] Concatenating into MASTER_SOURCE_NGANG_20MINS.mp4...")
subprocess.run([
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0",
    "-i", concat_txt,
    "-c", "copy",
    out_master_ngang
], check=True)

size_mb = os.path.getsize(out_master_ngang) / (1024 * 1024)
print(f"\n[DONE] Master Horizontal Source Video created: {out_master_ngang}")
print(f"Duration: ~20 minutes | Size: {size_mb:.2f} MB (under 100MB limit for GitHub!)")
