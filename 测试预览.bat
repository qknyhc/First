@echo off
chcp 65001 >nul
cd /d D:\Idea
echo 正在生成内容预览...
echo.
python main.py --dry-run
pause
