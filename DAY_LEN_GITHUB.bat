@echo off
chcp 65001 > nul
title ĐẨY SOURCE LÊN GITHUB
color 0B
echo ======================================================================
echo          TOOL ĐẨY MASTER SOURCE & CODE LÊN GITHUB CỦA BẠN
echo ======================================================================
echo.
echo [*] Repo cục bộ đã commit sẵn Master Source Video (78.7 MB) và toàn bộ tool.
echo.
set /p REPO_URL="Nhập link Repository GitHub của bạn (Ví dụ: https://github.com/daotnworking-hub/military-shorts.git): "

if "%REPO_URL%"=="" (
    echo [!] Bạn chưa nhập link repo. Hãy tạo 1 repo mới trên https://github.com/new rồi dán link vào nhé!
    pause
    exit /b
)

git remote remove origin 2>nul
git remote add origin %REPO_URL%
git branch -M main
echo.
echo [*] Đang đẩy toàn bộ source lên GitHub...
git push -u origin main
echo.
echo ======================================================================
echo Hoàn tất!
pause
