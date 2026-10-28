@echo off
chcp 65001 > nul
echo ======================================================================
echo    TOOL TAO VIDEO QUAN SU HOANH TRANG (36S - 3S CHUYEN CANH 1 LAN)
echo ======================================================================
echo.
python "%~dp0build_epic_36s.py"
echo.
pause
