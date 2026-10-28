@echo off
chcp 65001 > nul
title TOOL XAO NAU VIDEO QUAN SU 9:16
color 0A
echo ======================================================================
echo           TOOL TỰ ĐỘNG XÀO NẤU VIDEO QUÂN SỰ 9:16 FULL HD
echo ======================================================================
echo.
echo [*] Đang kiểm tra video trong thư mục input_videos...
echo.
python "%~dp0auto_cook_video.py"
echo.
echo ======================================================================
echo Nhấn phím bất kỳ để mở thư mục chứa video vừa xuất...
pause > nul
explorer "%~dp0output"
