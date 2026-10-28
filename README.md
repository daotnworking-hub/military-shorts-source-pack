# Military Shorts Auto Pipeline & Master Source Pack (Quân Sự Việt Nam)

Hệ thống tự động hóa toàn bộ quy trình tải, biên tập, chỉnh màu và dựng video ngắn 9:16 (Shorts/TikTok/Reels) chủ đề Quân sự Việt Nam & Thế giới.

---

## 📦 Nội Dung Package

1. **Master Source Video (18 phút 49 giây)**:
   - File: `MASTER_SOURCE_QUAN_SU_20CLIPS.mp4` (~78.7 MB)
   - Chứa 20 clip hành động quân sự chất lượng cao trích xuất từ kênh `@CDMediaQuanSu`.
   - Chuẩn khung hình dọc 9:16 (608x1080), âm thanh nguyên bản.

2. **Bộ Công Cụ Tự Động Hóa 1-Click (Code Python + Batch Windows)**:
   - `TAI_VIDEO_YOUTUBE.bat` / `download_from_youtube.py`: Tự động tải video YouTube Full HD không cần web converter trung gian.
   - `XAO_NAU_VIDEO.bat` / `auto_cook_video.py`: Tự động cắt 12 cảnh (3s/lần), gắn HUD thời sự, chèn tiêu đề giật gân, chỉnh màu điện ảnh và xuất video Full HD.
   - `compile_20_clips.py`: Script nối nhiều video clip thành 1 Master Source duy nhất trong chưa đầy 1 giây.

3. **Tài Nguyên Đồ Họa & Font Chữ (Assets)**:
   - Font **Montserrat ExtraBold**: Hỗ trợ 100% tiếng Việt có dấu, khắc phục hoàn toàn lỗi vỡ font.
   - Khung HUD thời sự `overlay_vn_military.png`.
   - Tiêu đề mở đầu Báo Động Đỏ `hook_korea_tensions.png`.
   - Nhạc nền Trailer kịch tính `bgm_epic.mp3`.

---

## 🚀 Hướng Dẫn Sử Dụng

### Bước 1: Tải thêm video nguồn (Tùy chọn)
- Bấm đúp vào `TAI_VIDEO_YOUTUBE.bat`.
- Chọn phím `1` để dán link video, hoặc phím `2` để tự động tải các Short mới nhất.

### Bước 2: Tự động xào nấu video ngắn 9:16
- Thả các video bạn thích vào thư mục `input_videos/`.
- (Tùy chọn) Thả file thu âm giọng đọc `voice.mp3` vào `input_videos/`.
- Bấm đúp vào `XAO_NAU_VIDEO.bat`.
- Sau 10-15 giây, video 9:16 hoàn chỉnh sẽ tự động xuất hiện trong thư mục `output/`.
