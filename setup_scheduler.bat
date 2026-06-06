@echo off
chcp 65001 >nul
echo ========================================
echo   微信每日推送 - 注册 Windows 计划任务
echo ========================================
echo.
echo 将以每日 08:00 的频率注册任务。
echo 请以管理员身份运行此脚本。
echo.

schtasks /Create /SC DAILY /TN "WeChatDailyPush" /TR "pythonw D:\Idea\main.py" /ST 08:00 /F

if %ERRORLEVEL% EQU 0 (
    echo.
    echo 任务注册成功！可通过 taskschd.msc 查看和管理。
) else (
    echo.
    echo 任务注册失败，请尝试以管理员身份运行。
)

pause
