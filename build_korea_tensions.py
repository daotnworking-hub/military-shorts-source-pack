import os
import subprocess
import json
import asyncio
import edge_tts

BASE_DIR = r"C:\Users\Dao\Downloads\military_shorts"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 12 SCENES SCRIPT FOR "CĂNG THẲNG TRIỀU TIÊN - HÀN QUỐC"
KOREA_SCRIPT = [
    {
        "id": 1,
        "text": "Tiếng gầm xé toạc bầu trời! Bán đảo Triều Tiên lại một lần nữa rung chuyển!",
        "sub_top": "TIẾNG GẦM XÉ TOẠC BẦU TRỜI!",
        "sub_bot": "BÁN ĐẢO TRIỀU TIÊN RUNG CHUYỂN!"
    },
    {
        "id": 2,
        "text": "Hàng trăm cỗ chiến xa tối tân nhất đồng loạt khai hỏa rầm trời!",
        "sub_top": "HÀNG TRĂM CỖ CHIẾN XA TỐI TÂN",
        "sub_bot": "ĐỒNG LOẠT KHAI HỎA RẦM TRỜI!"
    },
    {
        "id": 3,
        "text": "Các trận địa pháo phản lực tầm xa sẵn sàng trút bão lửa vạn quả!",
        "sub_top": "TRẬN ĐỊA PHÁO PHẢN LỰC TẦM XA",
        "sub_bot": "SẴN SÀNG TRÚT BÃO LỬA VẠN QUẢ!"
    },
    {
        "id": 4,
        "text": "Từng phát đạn hạng nặng dội thẳng vào lòng đất, báo hiệu đòn hủy diệt!",
        "sub_top": "TỪNG PHÁT ĐẠN HẠNG NẶNG",
        "sub_bot": "BÁO HIỆU ĐÒN HỦY DIỆT KINH HOÀNG!"
    },
    {
        "id": 5,
        "text": "Tên lửa rời bệ phóng, khóa chặt mọi mục tiêu chiến lược vào tầm ngắm!",
        "sub_top": "TÊN LỬA RỜI BỆ PHÓNG",
        "sub_bot": "KHÓA CHẶT MỌI MỤC TIÊU CHIẾN LƯỢC!"
    },
    {
        "id": 6,
        "text": "Dưới mặt biển, những pháo đài thép trực chiến phong tỏa mọi ngả đường!",
        "sub_top": "PHÁO ĐÀI THÉP TRỰC CHIẾN",
        "sub_bot": "PHONG TỎA MỌI NGẢ ĐƯỜNG BIỂN!"
    },
    {
        "id": 7,
        "text": "Các phi đội chiến đấu cơ quần thảo 24 trên 24, không một giây lơ là!",
        "sub_top": "PHI ĐỘI TIÊM KÍCH QUẦN THẢO 24/24",
        "sub_bot": "KHÔNG MỘT GIÂY PHÚT LƠ LÀ!"
    },
    {
        "id": 8,
        "text": "Căng thẳng biên giới đã chạm đỉnh điểm, một tia lửa nhỏ cũng bùng chiến hỏa!",
        "sub_top": "CĂNG THẲNG ĐÃ CHẠM ĐỈNH ĐIỂM",
        "sub_bot": "MỘT TIA LỬA NHỎ CŨNG BÙNG NỔ!"
    },
    {
        "id": 9,
        "text": "Đối đầu cân não, nơi mỗi bên đều nắm giữ sức mạnh hủy diệt tối thượng!",
        "sub_top": "ĐỐI ĐẦU VŨ KHÍ TỐI THƯỢNG",
        "sub_bot": "RỰC SÁNG TRÊN BẦU TRỜI ĐÊM!"
    },
    {
        "id": 10,
        "text": "Mệnh lệnh tác chiến đã nằm trên bàn chỉ huy, sẵn sàng cho tình huống xấu nhất!",
        "sub_top": "MỆNH LỆNH TÁC CHIẾN ĐÃ BAN HÀNH",
        "sub_bot": "SẴN SÀNG CHO ĐÒN PHỦ ĐẦU!"
    },
    {
        "id": 11,
        "text": "Liệu hòa bình có được giữ vững, hay một cơn bão thép sắp ập đến?",
        "sub_top": "HÒA BÌNH CÓ ĐƯỢC GIỮ VỮNG",
        "sub_bot": "HAY CƠN BÃO THÉP SẮP ẬP ĐẾN?"
    },
    {
        "id": 12,
        "text": "Đăng ký kênh Quân Sự Việt Nam ngay để cập nhật diễn biến mới nhất!",
        "sub_top": "ĐĂNG KÝ QUÂN SỰ VIỆT NAM",
        "sub_bot": "ĐỂ CẬP NHẬT DIỄN BIẾN MỚI NHẤT!"
    }
]

async def gen_voice():
    print("[*] Generating 12 synchronized voice segments...")
    seg_files = []
    for item in KOREA_SCRIPT:
        f = os.path.join(AUDIO_DIR, f"korea_seg_{item['id']:02d}.mp3")
        comm = edge_tts.Communicate(item["text"], "vi-VN-NamMinhNeural", rate="+6%")
        await comm.save(f)
        seg_files.append(f)
    
    # Concat into single voice track
    concat_txt = os.path.join(AUDIO_DIR, "korea_concat.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for p in seg_files:
            f.write(f"file '{p.replace(chr(92), '/')}'\n")
    
    voice_full = os.path.join(AUDIO_DIR, "korea_voice_full.mp3")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c", "copy", voice_full], check=True)
    return voice_full

def gen_ass_subtitles():
    events = []
    for i, item in enumerate(KOREA_SCRIPT):
        t_start = i * 3.0
        t_end = (i + 1) * 3.0
        
        # Format ASS timestamp h:mm:ss.cc
        s_h, s_m, s_s = int(t_start//3600), int((t_start%3600)//60), t_start%60
        e_h, e_m, e_s = int(t_end//3600), int((t_end%3600)//60), t_end%60
        
        ts_str = f"{s_h}:{s_m:02d}:{s_s:05.2f}"
        te_str = f"{e_h}:{e_m:02d}:{e_s:05.2f}"
        
        # Two lines formatted with high-impact yellow and white
        events.append(f"Dialogue: 0,{ts_str},{te_str},MilitarySub,,0,0,0,,{item['sub_top']}\\N{{\\c&H00D7FF&}}{item['sub_bot']}")

    ass_text = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: MilitarySub,Arial Black,46,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,5,3,2,60,60,340,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(events) + "\n"

    ass_path = os.path.join(AUDIO_DIR, "korea_subtitles.ass")
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_text)
    return ass_path

def main():
    print("=" * 60)
    print(">>> DUNG VIDEO FULL HD: CANG THANG TRIEU TIEN - HAN QUOC <<<")
    print("=" * 60)

    merged_raw = os.path.join(ASSETS_DIR, "merged_raw.mp4")
    hook_img = os.path.join(ASSETS_DIR, "hook_korea_tensions.png")
    hud_img = os.path.join(ASSETS_DIR, "overlay_vn_military.png")
    bgm_in = os.path.join(ASSETS_DIR, "bgm_epic.mp3")

    # 1. GENERATE CLEAN VIDEO (PURE EPIC SOUNDTRACK - READY FOR USER VOICE)
    print("\n--- 1. RENDER BAN CLEAN (NHAC NEN TRAILER, SAN SANG CHO BAN THU VOICE) ---")
    clean_audio = os.path.join(AUDIO_DIR, "bgm_clean_36s.mp3")
    subprocess.run([
        "ffmpeg", "-y", "-ss", "0.0", "-i", bgm_in, "-t", "36.0",
        "-af", "bass=g=4:f=90,treble=g=2:f=3000,afade=t=out:st=34.5:d=1.5,volume=0.9",
        "-b:a", "256k", clean_audio
    ], check=True)

    out_clean = os.path.join(OUTPUT_DIR, "video_korea_tensions_clean_36s.mp4")
    filter_clean = (
        "[0:v][1:v]overlay=0:0:enable='between(t,0,3.2)'[v1];"
        "[v1][2:v]overlay=0:0[vout]"
    )
    subprocess.run([
        "ffmpeg", "-y",
        "-i", merged_raw,
        "-i", hook_img,
        "-i", hud_img,
        "-i", clean_audio,
        "-filter_complex", filter_clean,
        "-map", "[vout]", "-map", "3:a",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-t", "36.0", "-pix_fmt", "yuv420p",
        out_clean
    ], check=True)
    print(f"[OK] Da xuat ban Clean: {out_clean}")

    # 2. GENERATE FULL DEMO VIDEO (WITH SYNCED VOICE & SUBTITLES)
    print("\n--- 2. RENDER BAN FULL (CO GIONG DOC NAM MINH VA SUBTITLES CHUAN DONG BO) ---")
    voice_file = asyncio.run(gen_voice())
    ass_file = gen_ass_subtitles().replace("\\", "/")
    
    # Mix voice (1.0) with background music (0.22)
    mixed_audio = os.path.join(AUDIO_DIR, "korea_final_mixed.mp3")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", voice_file,
        "-i", clean_audio,
        "-filter_complex", "[1:a]volume=0.22[bg];[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2[aout]",
        "-map", "[aout]", "-b:a", "192k",
        mixed_audio
    ], check=True)

    out_demo = os.path.join(OUTPUT_DIR, "video_korea_tensions_with_voice_36s.mp4")
    filter_full = (
        f"[0:v][1:v]overlay=0:0:enable='between(t,0,3.2)'[v1];"
        f"[v1][2:v]overlay=0:0[v2];"
        f"[v2]subtitles=filename='audio/korea_subtitles.ass'[vout]"
    )
    subprocess.run([
        "ffmpeg", "-y",
        "-i", merged_raw,
        "-i", hook_img,
        "-i", hud_img,
        "-i", mixed_audio,
        "-filter_complex", filter_full,
        "-map", "[vout]", "-map", "3:a",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-t", "36.0", "-pix_fmt", "yuv420p",
        out_demo
    ], cwd=BASE_DIR, check=True)
    print(f"[OK] Da xuat ban Demo kem Voice: {out_demo}")

if __name__ == "__main__":
    main()
