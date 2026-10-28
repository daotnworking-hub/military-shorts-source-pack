import os
import sys
import subprocess
import json
import glob
import math

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "input_videos")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TEMP_DIR = os.path.join(ASSETS_DIR, "temp_cook")

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

VALID_EXTS = (".mp4", ".mov", ".mkv", ".webm", ".avi", ".ts", ".m4v")

def get_video_duration(path):
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", path]
    out = subprocess.check_output(cmd)
    info = json.loads(out)
    return float(info["format"]["duration"])

def main():
    print("=" * 65)
    print("      TOOL TU DONG XAO NAU VIDEO QUAN SU 9:16 SIEU DEP")
    print("=" * 65)

    # 1. Quet source video
    videos = [os.path.join(INPUT_DIR, f) for f in os.listdir(INPUT_DIR) if f.lower().endswith(VALID_EXTS)]
    
    if not videos:
        print("\n[!] CHUA CO VIDEO NAO TRONG THU MUC input_videos!")
        print(f"--> Ban hay copy cac video Full HD ban vua tai vao thu muc sau:\n    {INPUT_DIR}\n")
        print("Sau do chay lai file nay la xong nhe!")
        return

    print(f"\n[+] Da tim thay {len(videos)} video source cua ban:")
    for v in videos:
        dur = get_video_duration(v)
        print(f"    - {os.path.basename(v)} ({dur:.1f}s)")

    # 2. Xay dung 12 doan cat (Moi doan 3s -> Tong 36s)
    TARGET_CUTS = 12
    CUT_DUR = 3.0
    print(f"\n[*] Dang tu dong cat {TARGET_CUTS} canh dep nhat (moi canh 3s)...")
    
    cut_files = []
    for idx in range(TARGET_CUTS):
        src_video = videos[idx % len(videos)]
        dur = get_video_duration(src_video)
        
        # Tinh toan thoi gian bat dau thong minh (chia deu theo do dai clip, tranh dau clip)
        slice_idx = idx // len(videos)
        step = max(3.5, (dur - 4.0) / max(1, (TARGET_CUTS // len(videos) + 1)))
        ss = min(dur - 3.5, 2.0 + slice_idx * step)
        if ss < 0:
            ss = 0.0

        out_cut = os.path.join(TEMP_DIR, f"cook_cut_{idx:02d}.mp4")
        
        vf = (
            "scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,"
            "fps=30,"
            "eq=contrast=1.18:brightness=0.01:saturation=1.22"
        )
        
        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{ss:.2f}",
            "-i", src_video,
            "-t", f"{CUT_DUR:.2f}",
            "-vf", vf,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "18",
            "-an",
            out_cut
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        cut_files.append(out_cut)
        print(f"    [OK] Canh {idx+1:02d}/{TARGET_CUTS} tu '{os.path.basename(src_video)}' tai giay thu {ss:.1f}s")

    # 3. Ghep 12 canh
    print("\n[*] Dang rap noi cac canh lai voi nhau...")
    concat_txt = os.path.join(TEMP_DIR, "cook_concat.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for fpath in cut_files:
            f.write(f"file '{fpath.replace(chr(92), '/')}'\n")

    merged_temp = os.path.join(TEMP_DIR, "cook_merged.mp4")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c", "copy", merged_temp], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # 4. Xu ly Am thanh (Kiem tra xem ban co bo file voice vao khong)
    user_voices = glob.glob(os.path.join(INPUT_DIR, "*voice*.*")) + glob.glob(os.path.join(INPUT_DIR, "*giong*.*"))
    bgm_in = os.path.join(ASSETS_DIR, "bgm_epic.mp3")
    final_audio = os.path.join(TEMP_DIR, "cook_final_audio.mp3")

    if user_voices:
        voice_path = user_voices[0]
        print(f"\n[+] Phat hien giong doc cua ban: '{os.path.basename(voice_path)}'")
        print("[*] Dang hoa am giong doc voi nhac nen thoi su...")
        subprocess.run([
            "ffmpeg", "-y",
            "-i", voice_path,
            "-i", bgm_in,
            "-filter_complex", "[1:a]volume=0.20,afade=t=out:st=34.5:d=1.5[bg];[0:a][bg]amix=inputs=2:duration=first[aout]",
            "-map", "[aout]", "-b:a", "192k", "-t", "36.0",
            final_audio
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    else:
        print("\n[*] Su dung nhac nen Trailer kịch tính (Ban co the long tieng sau)...")
        subprocess.run([
            "ffmpeg", "-y", "-ss", "0.0", "-i", bgm_in, "-t", "36.0",
            "-af", "bass=g=4:f=90,treble=g=2:f=3000,afade=t=out:st=34.5:d=1.5,volume=0.9",
            "-b:a", "192k",
            final_audio
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # 5. Xuat Video Hoan Chinh kem Khung Thoi Su
    print("\n[*] Dang phu Khung Ban Tin Thoi Su va xuat video Full HD...")
    hook_img = os.path.join(ASSETS_DIR, "hook_korea_tensions.png")
    hud_img = os.path.join(ASSETS_DIR, "overlay_vn_military.png")
    final_output = os.path.join(OUTPUT_DIR, "video_xao_nau_hoan_chinh.mp4")

    filter_complex = (
        "[0:v][1:v]overlay=0:0:enable='between(t,0,3.2)'[v1];"
        "[v1][2:v]overlay=0:0[vout]"
    )

    cmd_master = [
        "ffmpeg", "-y",
        "-i", merged_temp,
        "-i", hook_img,
        "-i", hud_img,
        "-i", final_audio,
        "-filter_complex", filter_complex,
        "-map", "[vout]", "-map", "3:a",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-t", "36.0", "-pix_fmt", "yuv420p",
        final_output
    ]
    subprocess.run(cmd_master, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    print("\n" + "=" * 65)
    print(f"XONG! Video da duoc xao nau hoan hao tai:\n{final_output}")
    print("=" * 65)

if __name__ == "__main__":
    main()
