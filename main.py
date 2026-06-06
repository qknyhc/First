"""每日推送 — 命令行入口

生成新闻摘要 + 概念故事，通过邮件发送。

每日运行（由 Windows 计划任务触发）：
    pythonw D:/Idea/main.py

手动测试：
    python main.py --dry-run              # 仅生成内容并打印，不发送
    python main.py --news-only --dry-run  # 仅生成新闻
    python main.py --concepts-only --dry-run  # 仅生成概念
    python main.py --count 3 --dry-run    # 覆盖默认条数
"""

import argparse

from config.settings import Config
from src.content_generator import generate_news, generate_concepts
from src.scheduler import run_daily
from src.logger import setup_logger


def _make_config(config: Config, **overrides) -> Config:
    return Config(
        deepseek_api_key=config.deepseek_api_key,
        smtp_host=config.smtp_host,
        smtp_port=config.smtp_port,
        sender_email=config.sender_email,
        sender_password=config.sender_password,
        receiver_email=config.receiver_email,
        deepseek_model=config.deepseek_model,
        news_count=overrides.get("news_count", config.news_count),
        concept_count=overrides.get("concept_count", config.concept_count),
        max_retries=config.max_retries,
        push_time=config.push_time,
    )


def main():
    parser = argparse.ArgumentParser(
        description="每日推送 — 新闻摘要 + 概念故事，邮件发送",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "首次使用：\n"
            "  python setup.py              → 交互式设置\n"
            "  python main.py --dry-run      → 预览内容\n"
            "  python main.py                → 正式发送\n"
        ),
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="仅生成内容并打印到控制台，不发送邮件",
    )
    parser.add_argument(
        "--news-only", action="store_true",
        help="仅生成新闻，跳过概念",
    )
    parser.add_argument(
        "--concepts-only", action="store_true",
        help="仅生成概念，跳过新闻",
    )
    parser.add_argument(
        "--count", type=int, default=None,
        help="覆盖新闻和概念的默认条数 (1-3)",
    )
    args = parser.parse_args()

    config = Config.from_env()
    logger = setup_logger()

    if args.count is not None:
        config = _make_config(config, news_count=args.count, concept_count=args.count)

    if args.dry_run:
        logger.info("--- 测试模式 (dry-run)，不发送邮件 ---")
        if not args.concepts_only:
            print("\n" + "=" * 50)
            print("📰 新闻摘要 (预览)")
            print("=" * 50 + "\n")
            try:
                print(generate_news(config))
            except Exception as e:
                print(f"新闻生成失败: {e}")
        if not args.news_only:
            print("\n" + "=" * 50)
            print("💡 概念故事 (预览)")
            print("=" * 50 + "\n")
            try:
                print(generate_concepts(config))
            except Exception as e:
                print(f"概念生成失败: {e}")
        logger.info("--- 测试完成 ---")
    elif args.news_only:
        config = _make_config(config, concept_count=0)
        run_daily(config)
    elif args.concepts_only:
        config = _make_config(config, news_count=0)
        run_daily(config)
    else:
        run_daily(config)


if __name__ == "__main__":
    main()
