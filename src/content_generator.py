"""内容生成模块 — 调用 DeepSeek API 生成新闻摘要和概念故事

DeepSeek API 兼容 OpenAI SDK，直接用 openai 库。
注册地址：https://platform.deepseek.com （国内手机号即可）
新用户赠送免费额度，后续按量计费（约 1 元/百万 tokens）。
"""

from openai import OpenAI, AuthenticationError, RateLimitError, APIConnectionError, InternalServerError, BadRequestError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from config.settings import Config
from src.logger import setup_logger
from templates.news_prompt import NEWS_SYSTEM_PROMPT, NEWS_USER_PROMPT
from templates.concept_prompt import CONCEPT_SYSTEM_PROMPT, CONCEPT_USER_PROMPT

logger = setup_logger()

RETRYABLE_ERRORS = (RateLimitError, APIConnectionError, InternalServerError)


def _build_client(config: Config) -> OpenAI:
    return OpenAI(
        api_key=config.deepseek_api_key,
        base_url="https://api.deepseek.com",
        timeout=120.0,
    )


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, max=60),
    retry=retry_if_exception_type(RETRYABLE_ERRORS),
    reraise=True,
)
def _call_deepseek(config: Config, system_prompt: str, user_prompt: str) -> str:
    client = _build_client(config)
    response = client.chat.completions.create(
        model=config.deepseek_model,
        max_tokens=2000,
        temperature=0.8,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    usage = response.usage
    logger.info(
        "DeepSeek API 调用成功 | "
        f"prompt_tokens={usage.prompt_tokens}, "
        f"completion_tokens={usage.completion_tokens}, "
        f"total_tokens={usage.total_tokens}"
    )
    return response.choices[0].message.content


def generate_news(config: Config) -> str:
    logger.info(f"开始生成新闻摘要，数量: {config.news_count}")
    user_prompt = NEWS_USER_PROMPT.format(count=config.news_count)
    try:
        result = _call_deepseek(config, NEWS_SYSTEM_PROMPT, user_prompt)
        logger.info("新闻摘要生成完成")
        return result.strip()
    except AuthenticationError:
        logger.error("DeepSeek API Key 无效，请检查 .env 中的 DEEPSEEK_API_KEY")
        raise
    except BadRequestError as e:
        logger.error(f"请求参数错误: {e}")
        raise
    except Exception as e:
        logger.error(f"新闻生成失败: {e}")
        raise


def generate_concepts(config: Config, past_concepts: str = "") -> str:
    logger.info(f"开始生成概念故事，数量: {config.concept_count}")
    user_prompt = CONCEPT_USER_PROMPT.format(count=config.concept_count, past_concepts=past_concepts)
    try:
        result = _call_deepseek(config, CONCEPT_SYSTEM_PROMPT, user_prompt)
        logger.info("概念故事生成完成")
        return result.strip()
    except AuthenticationError:
        logger.error("DeepSeek API Key 无效，请检查 .env 中的 DEEPSEEK_API_KEY")
        raise
    except BadRequestError as e:
        logger.error(f"请求参数错误: {e}")
        raise
    except Exception as e:
        logger.error(f"概念生成失败: {e}")
        raise
