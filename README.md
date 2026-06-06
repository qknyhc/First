# Daily Digest

A Python script that generates a daily email with curated news summaries and bite-sized concept stories, powered by [DeepSeek](https://platform.deepseek.com/) AI and sent via any SMTP email (163.com, QQ, Gmail, etc.).

## What you get

Each email has two sections:

**📰 News (1–3 items)** — tech, economy, politics. Each item comes with a concise "why it matters" takeaway.

**💡 Concepts (1–3 items)** — an everyday story or metaphor, followed by a reveal: *"This is the concept of [X]"*. Covers economics, psychology, political science, and sociology. Designed to make complex ideas stick.

## Quick start

### 1. Clone and install

```bash
git clone https://github.com/qknyhc/First.git
cd First
pip install -r requirements.txt
```

### 2. Get a DeepSeek API key

- Register at [platform.deepseek.com](https://platform.deepseek.com/) (phone number required)
- Go to **API Keys** → create a key
- New users get free credits; paid usage is ~$0.15 per million tokens

### 3. Configure email SMTP

You need a **free SMTP authorization code** (not your login password):

| Provider | SMTP Host | Port | Where to get the code |
|----------|-----------|------|-----------------------|
| 163.com | smtp.163.com | 465 | Settings → POP3/SMTP/IMAP → Add auth code |
| QQ Mail | smtp.qq.com | 465 | Settings → Account → POP3/SMTP → Enable |
| Gmail | smtp.gmail.com | 587 | Security → App passwords |

### 4. Set up your `.env` file

```bash
cp .env.example .env
```

Then edit `.env`:

```ini
DEEPSEEK_API_KEY=sk-your-key-here

SMTP_HOST=smtp.163.com
SMTP_PORT=465
SENDER_EMAIL=you@163.com
SENDER_PASSWORD=your-auth-code
RECEIVER_EMAIL=you@163.com
```

### 5. Run

```bash
# Preview content (no email sent)
python main.py --dry-run

# Send the real thing
python main.py
```

## CLI options

| Flag | What it does |
|------|-------------|
| `--dry-run` | Print content to console, skip email |
| `--news-only` | Only generate news |
| `--concepts-only` | Only generate concepts |
| `--count N` | Override item count (default: 2) |

## Scheduling (Windows)

```bat
setup_scheduler.bat
```

This registers a daily Task Scheduler job at 08:00. Or set it up manually in `taskschd.msc`.

For Linux/macOS, use cron:

```bash
0 8 * * * cd /path/to/project && python main.py
```

## Project structure

```
├── config/settings.py          # Config from .env
├── src/
│   ├── content_generator.py    # DeepSeek API calls
│   ├── pusher.py               # Email assembly & SMTP send
│   ├── scheduler.py            # Daily run orchestration
│   └── logger.py               # Rotating file logs
├── templates/
│   ├── news_prompt.py          # Prompt for news curation
│   └── concept_prompt.py       # Prompt for story-first concept teaching
├── main.py                     # CLI entry point
├── setup.py                    # Interactive setup wizard
└── .env.example                # Config template
```

## FAQ

**Q: Can I use a different AI provider?**  
Yes. Edit `src/content_generator.py` to swap DeepSeek for OpenAI, Anthropic, or any OpenAI-compatible API.

**Q: Can I use Gmail?**  
Yes. Set `SMTP_HOST=smtp.gmail.com`, `SMTP_PORT=587`, and use a [Google App Password](https://support.google.com/accounts/answer/185833).

**Q: How much does it cost?**  
- DeepSeek: free credits for new users, then ~$0.15/million tokens (a few cents per day)
- SMTP: free via 163.com, QQ Mail, or Gmail

## License

MIT
