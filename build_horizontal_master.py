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

videos = sorted([f for f in os.listdir(NGANG_DIR) if f.endswith(".mp4")])
print(f"Found {len(videos)} horizontal videos.")

cut_list = []
# Extract 210s (3.5 mins) from each video instantly with stream copy
for idx, v in enumerate(videos, 1):
    src = os.path.join(NGANG_DIR, v)
    out_cut = os.path.join(TEMP_DIR, f"hcut_{idx:02d}.mp4")
    cmd = [
        "ffmpeg", "-y",
        "-ss", "60.0",
        "-i", src,
        "-t", "210.0",
        "-c", "copy",
        out_cut
    ]
    print(f"[*] Instant copy 3.5 mins from: {v[:40]}...")
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    cut_list.append(out_cut)

# Concat
concat_txt = os.path.join(TEMP_DIR, "concat_hcuts.txt")
with open(concat_txt, "w", encoding="utf-8") as f:
    for c in cut_list:
        f.write(f"file '{c.replace(chr(92), '/')}'\n")

out_master = os.path.join(BASE_DIR, "MASTER_SOURCE_NGANG_QUAN_SU.mp4")
print("\n[*] Concatenating into MASTER_SOURCE_NGANG_QUAN_SU.mp4...")
subprocess.run([
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0",
    "-i", concat_txt,
    "-c", "copy",
    out_master
], check=True)

size_mb = os.path.getsize(out_master) / (1024 * 1024)
print(f"[DONE] Created: {out_master}")
print(f"Size: {size_mb:.2f} MB")
