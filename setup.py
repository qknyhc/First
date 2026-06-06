"""首次设置向导 — 对着提示输入就行，不需要懂代码"""

from pathlib import Path

ENV_PATH = Path(__file__).parent / ".env"


def main():
    print("=" * 50)
    print("  每日推送 — 首次设置")
    print("=" * 50)
    print()
    print("  这个程序每天自动发一封邮件给你，")
    print("  里面有当天新闻 + 有趣的小知识。")
    print()
    print("  设置过程只需要 5 分钟，跟着提示输入即可。")
    print()

    # === DeepSeek API Key ===
    print("=" * 50)
    print("  第1步：获取 DeepSeek 密钥（用于生成内容）")
    print("=" * 50)
    print()
    print("  请在浏览器里操作：")
    print()
    print("  ① 打开网址：platform.deepseek.com")
    print("  ② 点右上角「注册」，用手机号注册（中国手机号就行）")
    print("  ③ 注册完登录进去")
    print("  ④ 点左侧菜单的「API Keys」")
    print("  ⑤ 点「创建 API key」按钮")
    print("  ⑥ 复制那串以 sk- 开头的英文数字")
    print()
    print("  ─────────────────────")
    api_key = input("  然后粘贴到这里 → ").strip()
    print("  ─────────────────────")

    if not api_key.startswith("sk-"):
        print()
        print("  ⚠ 注意：密钥一般以 sk- 开头，你粘贴的内容看起来不太对。")
        print("  请回到 DeepSeek 网页，重新复制完整的密钥。")
        a = input("  按回车键退出，重新运行 setup.bat...")
        return

    # === Email ===
    print()
    print("=" * 50)
    print("  第2步：设置网易邮箱（用于发送邮件）")
    print("=" * 50)
    print()

    # 默认网易邮箱
    smtp_host = "smtp.163.com"
    smtp_port = "465"

    sender_email = input("  你的网易邮箱地址（比如 abc@163.com）: ").strip()
    print()

    if "@" not in sender_email:
        print("  ⚠ 邮箱地址格式不对，请重新运行 setup.bat")
        return

    if "163.com" not in sender_email and "126.com" not in sender_email:
        print("  看起来不像是网易邮箱？")
        print("  如果你用的是 QQ邮箱，输入 qq")
        print("  如果是其他邮箱，直接输入 SMTP 地址")
        alt = input("  → ").strip()
        if alt == "qq":
            smtp_host = "smtp.qq.com"
        elif alt:
            smtp_host = alt

    print()
    print("  ⚡ 现在需要获取「授权码」：")
    print()
    if "qq.com" in sender_email:
        print("  ① 浏览器打开 mail.qq.com，登录")
        print("  ② 点顶部「设置」→ 选「账户」")
        print("  ③ 往下翻，找到「POP3/IMAP/SMTP服务」")
        print("  ④ 点「开启」IMAP/SMTP服务")
        print("  ⑤ 按提示发送短信验证")
        print("  ⑥ 短信发送后，页面会出现一串英文字母")
        print("     那就是授权码，复制它")
    else:
        print("  ① 浏览器打开 mail.163.com，登录你的邮箱")
        print("  ② 点顶部「设置」→ 选「POP3/SMTP/IMAP」")
        print("  ③ 在「SMTP 服务」那一行，点「新增授权码」")
        print("  ④ 按提示用手机发短信")
        print("  ⑤ 短信发送后，页面会出现一串英文字母")
        print("     那就是授权码，复制它")
    print()
    print("  ─────────────────────")
    sender_password = input("  粘贴授权码到这里 → ").strip()
    print("  ─────────────────────")

    receiver = input("  邮件发到哪个地址？（默认就是上面那个）: ").strip()
    receiver_email = receiver or sender_email

    # === Write .env ===
    print()
    print("=" * 50)
    print("  第3步：保存")
    print("=" * 50)

    content = f"""# DeepSeek API
DEEPSEEK_API_KEY={api_key}

# 邮箱 SMTP
SMTP_HOST={smtp_host}
SMTP_PORT={smtp_port}
SENDER_EMAIL={sender_email}
SENDER_PASSWORD={sender_password}
RECEIVER_EMAIL={receiver_email}

# 可选
DEEPSEEK_MODEL=deepseek-chat
NEWS_COUNT=2
CONCEPT_COUNT=2
MAX_RETRIES=3
PUSH_TIME=08:00
"""

    ENV_PATH.write_text(content, encoding="utf-8")
    print("  ✓ 搞定！配置已保存。")

    print()
    print("=" * 50)
    print()
    print("  接下来请双击运行：")
    print()
    print("  → 「测试预览.bat」  先看看内容长什么样")
    print()
    print("  如果内容没问题，再双击：")
    print()
    print("  → 「发送邮件.bat」  正式发送到邮箱")
    print()
    print("=" * 50)


if __name__ == "__main__":
    main()
