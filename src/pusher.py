"""每日推送 — 邮箱发送模块

支持 QQ邮箱 / 163邮箱 等 SMTP 服务。
需要先在邮箱设置中开启 SMTP 并获取授权码（不是登录密码）。
"""

import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config.settings import Config
from src.logger import setup_logger

logger = setup_logger()

# 常用邮箱 SMTP 参考
# QQ邮箱:  smtp.qq.com,  port 465 (SSL)
# 163邮箱: smtp.163.com, port 465 (SSL)


def _markdown_to_html(text: str) -> str:
    """将 Markdown 消息转换为 HTML 邮件。只处理已经格式化的内容。"""
    lines = text.split("\n")
    html_lines = []
    in_quote = False
    in_story = False

    for line in lines:
        if line.startswith("## "):
            html_lines.append(f'<h2 style="color:#333;border-bottom:2px solid #eee;padding-bottom:8px">{line[3:]}</h2>')
        elif line.startswith("### "):
            html_lines.append(f'<h3 style="color:#2c3e50;margin-top:24px">{line[4:]}</h3>')
        elif line.startswith("**") and line.endswith("**"):
            html_lines.append(f'<p style="font-weight:bold;font-size:15px;margin:12px 0 4px">{line[2:-2]}</p>')
        elif line.startswith("> "):
            if not in_story:
                in_story = True
                html_lines.append('<blockquote style="background:#f8f9fa;border-left:4px solid #6c757d;padding:12px 16px;margin:8px 0;color:#555;font-style:italic">')
            html_lines.append(f"{line[2:]}<br>")
        elif line.startswith("***揭示："):
            in_story = False
            html_lines.append('</blockquote>')
            html_lines.append(f'<p style="font-weight:bold;color:#e74c3c;font-size:15px;margin:12px 0">{line[3:-3]}</p>')
        elif line == "---":
            if in_story:
                html_lines.append('</blockquote>')
                in_story = False
            html_lines.append('<hr style="border:none;border-top:1px solid #e0e0e0;margin:20px 0">')
        elif line.startswith("> ") and in_quote:
            html_lines.append(f"{line[2:]}<br>")
        elif line.strip():
            html_lines.append(f'<p style="margin:6px 0;line-height:1.7">{line}</p>')
        else:
            if in_story:
                html_lines.append('</blockquote>')
                in_story = False
            html_lines.append("<br>")

    if in_story:
        html_lines.append('</blockquote>')

    return "\n".join(html_lines)


def assemble_message(news_text: str, concepts_text: str) -> str:
    today = datetime.now().strftime("%Y年%m月%d日")
    return (
        f"## 每日推送 | {today}\n\n"
        f"---\n\n"
        f"### 📰 今日资讯\n\n{news_text}\n\n"
        f"---\n\n"
        f"### 💡 今日概念\n\n{concepts_text}\n\n"
        f"---\n\n"
        f"> 由 Claude 生成"
    )


def send(config: Config, message: str) -> bool:
    today = datetime.now().strftime("%Y年%m月%d日")
    subject = f"每日推送 | {today}"

    html_body = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:'Microsoft YaHei','PingFang SC',sans-serif;max-width:600px;margin:0 auto;padding:16px;color:#333">
{_markdown_to_html(message)}
<p style="color:#999;font-size:12px;margin-top:24px;border-top:1px solid #eee;padding-top:12px">
由 Claude 生成 · 每日自动推送
</p>
</body>
</html>"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = config.sender_email
    msg["To"] = config.receiver_email

    msg.attach(MIMEText(message, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    for attempt in range(1, config.max_retries + 1):
        try:
            with smtplib.SMTP_SSL(config.smtp_host, config.smtp_port, timeout=15) as server:
                server.login(config.sender_email, config.sender_password)
                server.sendmail(config.sender_email, config.receiver_email, msg.as_string())
            logger.info(f"邮件发送成功 -> {config.receiver_email}")
            return True
        except smtplib.SMTPAuthenticationError:
            logger.error("邮箱登录失败，请检查 SENDER_EMAIL 和 SENDER_PASSWORD（授权码）是否正确")
            return False
        except Exception as e:
            logger.warning(f"邮件发送失败 (attempt {attempt}): {e}")

    logger.error("邮件发送最终失败，已重试 %d 次", config.max_retries)
    _save_failed_message(message)
    return False


def _save_failed_message(message: str) -> None:
    from pathlib import Path
    log_dir = Path(__file__).resolve().parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = log_dir / f"failed_{date_str}.md"
    filepath.write_text(message, encoding="utf-8")
    logger.info(f"失败消息已保存到: {filepath}")
