import os
import subprocess

BASE_DIR = r"C:\Users\Dao\Downloads\military_shorts"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# 1. Concat voice
print("Concatenating voice segments...")
concat_txt = os.path.join(AUDIO_DIR, "kt_concat.txt")
with open(concat_txt, "w", encoding="utf-8") as f:
    for i in range(1, 13):
        f.write(f"file 'kt_seg_{i:02d}.mp3'\n")

voice_full = os.path.join(AUDIO_DIR, "kt_voice_full.mp3")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c", "copy", voice_full], check=True)

# 2. Mix with BGM
clean_audio = os.path.join(AUDIO_DIR, "bgm_clean_36s.mp3")
mixed_audio = os.path.join(AUDIO_DIR, "kt_final_mixed.mp3")
subprocess.run([
    "ffmpeg", "-y",
    "-i", voice_full,
    "-i", clean_audio,
    "-filter_complex", "[1:a]volume=0.22[bg];[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2[aout]",
    "-map", "[aout]", "-b:a", "192k",
    mixed_audio
], check=True)

# 3. Generate ASS subtitles
KOREA_SCRIPT = [
    {"sub_top": "TIẾNG GẦM XÉ TOẠC BẦU TRỜI!", "sub_bot": "BÁN ĐẢO TRIỀU TIÊN RUNG CHUYỂN!"},
    {"sub_top": "HÀNG TRĂM CỖ CHIẾN XA TỐI TÂN", "sub_bot": "ĐỒNG LOẠT KHAI HỎA RẦM TRỜI!"},
    {"sub_top": "TRẬN ĐỊA PHÁO PHẢN LỰC TẦM XA", "sub_bot": "SẴN SÀNG TRÚT BÃO LỬA VẠN QUẢ!"},
    {"sub_top": "TỪNG PHÁT ĐẠN HẠNG NẶNG", "sub_bot": "BÁO HIỆU ĐÒN HỦY DIỆT KINH HOÀNG!"},
    {"sub_top": "TÊN LỬA RỜI BỆ PHÓNG", "sub_bot": "KHÓA CHẶT MỌI MỤC TIÊU CHIẾN LƯỢC!"},
    {"sub_top": "PHÁO ĐÀI THÉP TRỰC CHIẾN", "sub_bot": "PHONG TỎA MỌI NGẢ ĐƯỜNG BIỂN!"},
    {"sub_top": "PHI ĐỘI TIÊM KÍCH QUẦN THẢO 24/24", "sub_bot": "KHÔNG MỘT GIÂY PHÚT LƠ LÀ!"},
    {"sub_top": "CĂNG THẲNG ĐÃ CHẠM ĐỈNH ĐIỂM", "sub_bot": "MỘT TIA LỬA NHỎ CŨNG BÙNG NỔ!"},
    {"sub_top": "ĐỐI ĐẦU VŨ KHÍ TỐI THƯỢNG", "sub_bot": "RỰC SÁNG TRÊN BẦU TRỜI ĐÊM!"},
    {"sub_top": "MỆNH LỆNH TÁC CHIẾN ĐÃ BAN HÀNH", "sub_bot": "SẴN SÀNG CHO ĐÒN PHỦ ĐẦU!"},
    {"sub_top": "HÒA BÌNH CÓ ĐƯỢC GIỮ VỮNG", "sub_bot": "HAY CƠN BÃO THÉP SẮP ẬP ĐẾN?"},
    {"sub_top": "ĐĂNG KÝ QUÂN SỰ VIỆT NAM", "sub_bot": "ĐỂ CẬP NHẬT DIỄN BIẾN MỚI NHẤT!"}
]

events = []
for i, item in enumerate(KOREA_SCRIPT):
    t_start = i * 3.0
    t_end = (i + 1) * 3.0
    s_h, s_m, s_s = int(t_start//3600), int((t_start%3600)//60), t_start%60
    e_h, e_m, e_s = int(t_end//3600), int((t_end%3600)//60), t_end%60
    ts_str = f"{s_h}:{s_m:02d}:{s_s:05.2f}"
    te_str = f"{e_h}:{e_m:02d}:{e_s:05.2f}"
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

# 4. Render final video with subtitles
merged_raw = os.path.join(ASSETS_DIR, "merged_raw.mp4")
hook_img = os.path.join(ASSETS_DIR, "hook_korea_tensions.png")
hud_img = os.path.join(ASSETS_DIR, "overlay_vn_military.png")
out_demo = os.path.join(OUTPUT_DIR, "video_korea_tensions_with_voice_36s.mp4")

filter_full = (
    "[0:v][1:v]overlay=0:0:enable='between(t,0,3.2)'[v1];"
    "[v1][2:v]overlay=0:0[v2];"
    "subtitles=filename='audio/korea_subtitles.ass'[vout]"
)

cmd = [
    "ffmpeg", "-y",
    "-i", merged_raw,
    "-i", hook_img,
    "-i", hud_img,
    "-i", mixed_audio,
    "-filter_complex", "[0:v][1:v]overlay=0:0:enable='between(t,0,3.2)'[v1];[v1][2:v]overlay=0:0[v2];[v2]subtitles=filename='audio/korea_subtitles.ass'[vout]",
    "-map", "[vout]", "-map", "3:a",
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
    "-c:a", "aac", "-b:a", "192k",
    "-t", "36.0", "-pix_fmt", "yuv420p",
    out_demo
]

subprocess.run(cmd, cwd=BASE_DIR, check=True)
print("[DONE] Rendered video_korea_tensions_with_voice_36s.mp4 successfully!")
