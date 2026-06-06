@echo off
chcp 65001 >nul
cd /d D:\Idea
echo 正在生成并发送邮件...
python main.py
pause
