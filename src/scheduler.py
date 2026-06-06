from config.settings import Config
from src.content_generator import generate_news, generate_concepts
from src.pusher import assemble_message, send
from src.logger import setup_logger

logger = setup_logger()


def run_daily(config: Config) -> None:
    logger.info("=== 每日推送开始 ===")

    news_text = ""
    concepts_text = ""

    try:
        if config.news_count > 0:
            news_text = generate_news(config)
        else:
            logger.info("跳过新闻生成（count=0）")
    except Exception:
        logger.exception("新闻生成失败，将继续生成概念")
        news_text = "（今日新闻生成失败，请检查日志）"

    try:
        if config.concept_count > 0:
            concepts_text = generate_concepts(config)
        else:
            logger.info("跳过概念生成（count=0）")
    except Exception:
        logger.exception("概念生成失败")
        concepts_text = "（今日概念生成失败，请检查日志）"

    if not news_text and not concepts_text:
        logger.error("新闻和概念均生成失败，终止推送")
        return

    message = assemble_message(news_text, concepts_text)
    success = send(config, message)
    if success:
        logger.info("=== 每日推送完成 ===")
    else:
        logger.error("=== 每日推送完成，但推送发送失败 ===")
