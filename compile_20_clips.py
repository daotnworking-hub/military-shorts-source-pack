import os
import subprocess

clips_dir = r"C:\Users\Dao\Downloads\military_shorts\source_20_clips"
files = [f for f in os.listdir(clips_dir) if f.startswith("clip_") and f.endswith(".mp4")]
files.sort()

concat_list = os.path.join(clips_dir, "concat_all_20.txt")
with open(concat_list, "w", encoding="utf-8") as f:
    for fpath in files:
        f.write(f"file '{fpath}'\n")

out_master = os.path.join(r"C:\Users\Dao\Downloads\military_shorts", "MASTER_SOURCE_QUAN_SU_20CLIPS.mp4")
print(f"Concatenating {len(files)} clips into 1 Master Source Video (Instant Copy Mode)...")

cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0",
    "-i", concat_list,
    "-c", "copy",
    out_master
]
subprocess.run(cmd, cwd=clips_dir, check=True)
size_mb = os.path.getsize(out_master) / (1024 * 1024)
print(f"Master Source Video created at: {out_master}")
print(f"Size: {size_mb:.2f} MB")
