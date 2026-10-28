import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"C:\Users\Dao\Downloads\military_shorts"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
FONT_FILE = os.path.join(ASSETS_DIR, "fonts", "Montserrat-ExtraBold.ttf")

W, H = 1080, 1920

# 1. FIX HUD OVERLAY
print("1. Re-generating HUD with Montserrat-ExtraBold...")
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

font_hud = ImageFont.truetype(FONT_FILE, 24)
font_badge = ImageFont.truetype(FONT_FILE, 44)
font_badge_sub = ImageFont.truetype(FONT_FILE, 22)

# Top Left HUD
draw.rounded_rectangle([(40, 60), (490, 120)], radius=30, fill=(0, 0, 0, 190), outline=(220, 20, 20, 220), width=2)
draw.ellipse([(65, 80), (85, 100)], fill=(255, 30, 30, 255))
draw.text((105, 78), "BẢN TIN QUÂN SỰ ĐẶC BIỆT", fill=(255, 255, 255, 240), font=font_hud)

# Top Right HUD
draw.rounded_rectangle([(W - 200, 60), (W - 40, 120)], radius=30, fill=(0, 0, 0, 190), outline=(120, 120, 120, 200), width=2)
draw.text((W - 175, 78), "FULL HD", fill=(255, 215, 0, 240), font=font_hud)

# Bottom Branding Gradient
for y in range(H - 220, H):
    alpha = int(220 * (y - (H - 220)) / 220)
    draw.line([(0, y), (W, y)], fill=(8, 8, 12, alpha))

draw.line([(60, H - 180), (W - 60, H - 180)], fill=(220, 20, 20, 220), width=3)

# 'QUÂN SỰ VIỆT NAM' Metallic Branding
text_badge = "QUÂN SỰ VIỆT NAM"
bbox = draw.textbbox((0, 0), text_badge, font=font_badge)
tw = bbox[2] - bbox[0]
draw.text(((W - tw) // 2, H - 155), text_badge, fill=(245, 245, 245, 255), font=font_badge)

text_sub = "THEO DÕI ĐỂ CẬP NHẬT MỚI NHẤT"
bbox_sub = draw.textbbox((0, 0), text_sub, font=font_badge_sub)
tw_sub = bbox_sub[2] - bbox_sub[0]
draw.text(((W - tw_sub) // 2, H - 95), text_sub, fill=(255, 215, 0, 220), font=font_badge_sub)

overlay.save(os.path.join(ASSETS_DIR, "overlay_vn_military.png"))

# 2. FIX OPENING TITLE HOOK
print("2. Re-generating Title Hook with Montserrat-ExtraBold...")
hook = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw_h = ImageDraw.Draw(hook)

font_tag = ImageFont.truetype(FONT_FILE, 32)
font_t1 = ImageFont.truetype(FONT_FILE, 52)
font_t2 = ImageFont.truetype(FONT_FILE, 40)

tag_text = "⚡ BÁO ĐỘNG ĐỎ"
tag_w, tag_h = 320, 56
tag_x = (W - tag_w) // 2
tag_y = 450
draw_h.rounded_rectangle([(tag_x, tag_y), (tag_x + tag_w, tag_y + tag_h)], radius=15, fill=(220, 20, 20, 240))
draw_h.text((tag_x + 25, tag_y + 8), tag_text, fill=(255, 255, 255, 255), font=font_tag)

l1 = "TRIỀU TIÊN - HÀN QUỐC"
bbox_l1 = draw_h.textbbox((0, 0), l1, font=font_t1)
tw_l1 = bbox_l1[2] - bbox_l1[0]
x_l1 = (W - tw_l1) // 2
y_l1 = 530
for ox, oy in [(-3,-3), (3,-3), (-3,3), (3,3), (0, 4), (0, -4)]:
    draw_h.text((x_l1 + ox, y_l1 + oy), l1, fill=(0, 0, 0, 255), font=font_t1)
draw_h.text((x_l1, y_l1), l1, fill=(255, 215, 0, 255), font=font_t1)

l2 = "BÁN ĐẢO BÊN BỜ VỰC XUNG ĐỘT!"
bbox_l2 = draw_h.textbbox((0, 0), l2, font=font_t2)
tw_l2 = bbox_l2[2] - bbox_l2[0]
x_l2 = (W - tw_l2) // 2
y_l2 = 615
for ox, oy in [(-3,-3), (3,-3), (-3,3), (3,3), (0, 3)]:
    draw_h.text((x_l2 + ox, y_l2 + oy), l2, fill=(0, 0, 0, 255), font=font_t2)
draw_h.text((x_l2, y_l2), l2, fill=(255, 255, 255, 255), font=font_t2)

hook.save(os.path.join(ASSETS_DIR, "hook_korea_tensions.png"))

# 3. RE-GENERATE ASS SUBTITLES WITH MONTSERRAT EXTRABOLD
print("3. Re-generating ASS Subtitles with Montserrat ExtraBold...")
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
Style: MilitarySub,Montserrat ExtraBold,48,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,5,2,2,40,40,320,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(events) + "\n"

ass_path = os.path.join(AUDIO_DIR, "korea_subtitles_fixed.ass")
with open(ass_path, "w", encoding="utf-8") as f:
    f.write(ass_text)

# 4. RENDER CLEAN VERSION WITH FIXED GRAPHICS
print("4. Re-rendering Clean Video with 100% fixed font...")
merged_raw = os.path.join(ASSETS_DIR, "merged_raw.mp4")
hook_img = os.path.join(ASSETS_DIR, "hook_korea_tensions.png")
hud_img = os.path.join(ASSETS_DIR, "overlay_vn_military.png")
clean_audio = os.path.join(AUDIO_DIR, "bgm_clean_36s.mp3")
out_clean = os.path.join(OUTPUT_DIR, "video_korea_tensions_clean_36s.mp4")

cmd_clean = [
    "ffmpeg", "-y",
    "-i", merged_raw,
    "-i", hook_img,
    "-i", hud_img,
    "-i", clean_audio,
    "-filter_complex", "[0:v][1:v]overlay=0:0:enable='between(t,0,3.2)'[v1];[v1][2:v]overlay=0:0[vout]",
    "-map", "[vout]", "-map", "3:a",
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
    "-c:a", "aac", "-b:a", "192k",
    "-t", "36.0", "-pix_fmt", "yuv420p",
    out_clean
]
subprocess.run(cmd_clean, check=True)

# 5. RENDER DEMO VERSION WITH FIXED SUBTITLES
print("5. Re-rendering Demo Video with 100% fixed subtitles...")
mixed_audio = os.path.join(AUDIO_DIR, "kt_final_mixed.mp3")
out_demo = os.path.join(OUTPUT_DIR, "video_korea_tensions_with_voice_36s.mp4")

cmd_demo = [
    "ffmpeg", "-y",
    "-i", merged_raw,
    "-i", hook_img,
    "-i", hud_img,
    "-i", mixed_audio,
    "-filter_complex", "[0:v][1:v]overlay=0:0:enable='between(t,0,3.2)'[v1];[v1][2:v]overlay=0:0[v2];[v2]subtitles=filename='audio/korea_subtitles_fixed.ass':fontsdir='assets/fonts'[vout]",
    "-map", "[vout]", "-map", "3:a",
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
    "-c:a", "aac", "-b:a", "192k",
    "-t", "36.0", "-pix_fmt", "yuv420p",
    out_demo
]
subprocess.run(cmd_demo, cwd=BASE_DIR, check=True)
print("ALL DONE! Zero font errors!")
