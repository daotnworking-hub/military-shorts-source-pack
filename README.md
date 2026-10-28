# Military Source Pack & Automation Pipeline (Quân Sự Việt Nam)

Hệ thống tự động hóa toàn bộ quy trình tải, biên tập, chỉnh màu và dựng video ngắn 9:16 (Shorts/TikTok/Reels) từ nguồn tư liệu phong phú của kênh **@CDMediaQuanSu**.

---

## 📦 Nội Dung Package

### 1. Master Source Video Ngang (16:9 - 17 phút 31 giây)
- File: `MASTER_SOURCE_NGANG_QUAN_SU.mp4` (~67.7 MB)
- Trích xuất và ghép nối liền mạch các thước phim đắt giá nhất từ 5 đại phóng sự quân sự:
  - 01. Bộ đội Việt Nam xẻ dọc Trường Sơn đưa xe tăng vào tác chiến.
  - 02. Việt Nam chi 2 tỷ USD mua tàu ngầm Kilo bảo vệ biển đảo.
  - 03. Samurra 1991 - Trận không chiến rực lửa làm lu mờ F-15.
  - 04. Sư đoàn 308 - Quân Tiên Phong và kế hoạch tác chiến 1975.
  - 05. Vì sao trực thăng quân đội Mỹ mang tên các bộ tộc da đỏ?
- Định dạng: Chuẩn 16:9 (1280x720), âm thanh nguyên bản.

### 2. Master Source Video Dọc (9:16 - 18 phút 49 giây)
- File: `MASTER_SOURCE_QUAN_SU_20CLIPS.mp4` (~78.7 MB)
- Tổng hợp 20 video Short quân sự tốc độ cao, sẵn sàng đưa vào CapCut / Premiere.

### 3. Nguồn Video Dài Cục Bộ (Hơn 1 giờ 15 phút)
- Thư mục cục bộ: `source_ngang/` lưu giữ toàn bộ 5 video dài nguyên bản (10-17 phút/video) để dựng phim chuyên sâu.

### 4. Bộ Công Cụ Tự Động Hóa 1-Click
- `TAI_VIDEO_YOUTUBE.bat`: Tự động tải video YouTube Full HD trực tiếp (không cần web trung gian).
- `XAO_NAU_VIDEO.bat`: Tự động cắt cảnh 3s/lần, gắn khung thời sự, tiêu đề mở đầu giật gân và xuất video Shorts 9:16.
- `compile_horizontal_master.py`: Tool nối các đoạn highlight ngang thành Master Source.

---

## 🚀 Hướng Dẫn Sử Dụng

1. **Lấy tư liệu**: Kéo trực tiếp file `MASTER_SOURCE_NGANG_QUAN_SU.mp4` hoặc `MASTER_SOURCE_QUAN_SU_20CLIPS.mp4` vào CapCut / Premiere để cắt b-roll.
2. **Dựng tự động**: Thả clip vào `input_videos/` và bấm đúp chuột vào `XAO_NAU_VIDEO.bat`.
