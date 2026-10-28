import os
import sys
import subprocess
import json
import argparse
import asyncio
import edge_tts

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

DEFAULT_SCRIPTS = [
    {
        "text": "Thế mới biết nếu một cuộc chiến nổ ra ở bán đảo Triều Tiên, sức hủy diệt sẽ khủng khiếp đến mức nào!",
        "sub_line1": "THẾ MỚI BIẾT NẾU CHIẾN TRANH NỔ RA",
        "sub_line2": "SỨC HỦY DIỆT SẼ KHỦNG KHIẾP ĐẾN MỨC NÀO!"
    },
    {
        "text": "Hàng trăm khẩu pháo tự hành và bệ phóng rocket tầm xa bất ngờ được kéo sát đường biên giới, đe dọa trực tiếp thủ đô Seoul!",
        "sub_line1": "HÀNG TRĂM KHẨU PHÁO VÀ ROCKET TẦM XA",
        "sub_line2": "BẤT NGỜ ÁP SÁT ĐƯỜNG BIÊN GIỚI!"
    },
    {
        "text": "Cả hai bên đã đặt quân đội vào tình trạng báo động cao nhất. Liệu đây là đòn răn đe, hay dấu hiệu của một cơn bão chiến tranh?",
        "sub_line1": "QUÂN ĐỘI ĐẶT TRẠNG THÁI BÁO ĐỘNG ĐỎ",
        "sub_line2": "ĐÂY LÀ RĂN ĐE HAY CƠN BÃO CHIẾN TRANH?"
    }
]

async def gen_tts_segment(text, out_path, voice="vi-VN-NamMinhNeural"):
    comm = edge_tts.Communicate(text, voice)
    await comm.save(out_path)

def get_audio_duration(file_path):
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", file_path]
    out = subprocess.check_output(cmd)
    info = json.loads(out)
    return float(info["format"]["duration"])

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def build_pipeline(custom_bgm=None, output_name="military_short_latest.mp4"):
    print("=" * 60)
    print(">>> 1. TAO GIONG DOC VOICE AI (EDGE-TTS NAM MINH)")
    print("=" * 60)
    
    segment_files = []
    durations = []
    
    for idx, item in enumerate(DEFAULT_SCRIPTS):
        seg_file = os.path.join(AUDIO_DIR, f"seg_{idx}.mp3")
        print(f"[*] Dang tao doan {idx+1}/{len(DEFAULT_SCRIPTS)}: {item['text'][:45]}...")
        asyncio.run(gen_tts_segment(item["text"], seg_file))
        d = get_audio_duration(seg_file)
        durations.append(d)
        segment_files.append(seg_file)
    
    # Concat
    concat_txt = os.path.join(AUDIO_DIR, "concat_auto.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for fpath in segment_files:
            f.write(f"file '{fpath.replace(chr(92), '/')}'\n")
    
    voice_full = os.path.join(AUDIO_DIR, "voice_full.mp3")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c", "copy", voice_full], check=True)
    total_voice_dur = sum(durations)
    print(f"[+] Tong thoi luong giong doc: {total_voice_dur:.2f}s")
    
    print("\n" + "=" * 60)
    print(">>> 2. TAO PHU DE ANIMATION DANG ASS")
    print("=" * 60)
    
    ass_events = []
    current_time = 0.0
    for idx, item in enumerate(DEFAULT_SCRIPTS):
        seg_dur = durations[idx]
        half_dur = seg_dur / 2.0
        
        t0 = format_ass_time(current_time)
        t1 = format_ass_time(current_time + half_dur)
        t2 = format_ass_time(current_time + seg_dur)
        
        ass_events.append(f"Dialogue: 0,{t0},{t1},MilitaryTitle,,0,0,0,,{item['sub_line1']}")
        ass_events.append(f"Dialogue: 0,{t1},{t2},MilitaryTitle,,0,0,0,,{{\\c&H0000FF&}}{item['sub_line2']}")
        current_time += seg_dur

    ass_content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: MilitaryTitle,Arial Black,54,&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,6,3,2,60,60,570,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ass_events) + "\n"

    ass_path = os.path.join(AUDIO_DIR, "auto_subtitles.ass")
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_content)
    print("[+] Phu de ASS da san sang.")

    print("\n" + "=" * 60)
    print(">>> 3. MIX NHAC NEN KICH TINH")
    print("=" * 60)
    bgm_path = custom_bgm if (custom_bgm and os.path.exists(custom_bgm)) else os.path.join(ASSETS_DIR, "bgm_epic.mp3")
    final_audio = os.path.join(AUDIO_DIR, "auto_final_audio.mp3")
    fade_start = max(0, total_voice_dur - 1.5)
    
    subprocess.run([
        "ffmpeg", "-y",
        "-i", voice_full,
        "-i", bgm_path,
        "-filter_complex", f"[1:a]volume=0.20,afade=t=out:st={fade_start:.2f}:d=1.5[bgm];[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]",
        "-map", "[aout]",
        "-b:a", "192k",
        final_audio
    ], check=True)
    print("[+] Mix am thanh hoan tat.")

    print("\n" + "=" * 60)
    print(">>> 4. DUNG VA XUAT VIDEO 9:16 (CHIA 3 TANG)")
    print("=" * 60)
    top_img = os.path.join(ASSETS_DIR, "top_leaders.jpg")
    mid_img = os.path.join(ASSETS_DIR, "artillery_middle.jpg")
    bot_img = os.path.join(ASSETS_DIR, "footer_banner.jpg")
    out_video_path = os.path.join(OUTPUT_DIR, output_name)

    fps = 30
    total_frames = int(total_voice_dur * fps) + 10

    filter_complex = f"""
[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:560,loop=loop={total_frames}:size=1:start=0,setpts=PTS-STARTPTS[top];
[1:v]zoompan=z='min(zoom+0.0006,1.25)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s=1080x820:fps={fps}[mid];
[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:540,loop=loop={total_frames}:size=1:start=0,setpts=PTS-STARTPTS[bot];
[top][mid][bot]vstack=inputs=3[stacked];
[stacked]drawbox=y=558:color=red@0.8:width=1080:height=4:t=fill,drawbox=y=1378:color=red@0.8:width=1080:height=4:t=fill,subtitles=filename='audio/auto_subtitles.ass'[vout]
"""

    cmd = [
        "ffmpeg", "-y",
        "-i", top_img,
        "-i", mid_img,
        "-i", bot_img,
        "-i", final_audio,
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-map", "3:a",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "19",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", f"{total_voice_dur:.2f}",
        "-pix_fmt", "yuv420p",
        out_video_path
    ]

    subprocess.run(cmd, cwd=BASE_DIR, check=True)
    print("\n" + "=" * 60)
    print(f"XONG! Video da xuat thanh cong tai:\n{out_video_path}")
    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bgm", type=str, default=None, help="Duong dan den file nhac nen mp3")
    parser.add_argument("--output", type=str, default="military_short_latest.mp4", help="Ten file video xuat ra")
    args = parser.parse_args()
    build_pipeline(custom_bgm=args.bgm, output_name=args.output)
