from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    deepseek_api_key: str
    smtp_host: str
    smtp_port: int
    sender_email: str
    sender_password: str
    receiver_email: str
    deepseek_model: str = "deepseek-chat"
    news_count: int = 2
    concept_count: int = 2
    max_retries: int = 3
    push_time: str = "08:00"

    def __post_init__(self):
        if not self.deepseek_api_key:
            raise ValueError("DEEPSEEK_API_KEY 未设置，请在 .env 中配置")
        if not self.smtp_host:
            raise ValueError("SMTP_HOST 未设置，请在 .env 中配置")
        if not self.sender_email:
            raise ValueError("SENDER_EMAIL 未设置，请在 .env 中配置")
        if not self.sender_password:
            raise ValueError("SENDER_PASSWORD 未设置，请在 .env 中配置（邮箱授权码）")
        if not self.receiver_email:
            raise ValueError("RECEIVER_EMAIL 未设置，请在 .env 中配置")

    @classmethod
    def from_env(cls) -> "Config":
        load_dotenv()
        return cls(
            deepseek_api_key=os.getenv("DEEPSEEK_API_KEY", os.getenv("ANTHROPIC_API_KEY", "")),
            smtp_host=os.getenv("SMTP_HOST", "smtp.qq.com"),
            smtp_port=int(os.getenv("SMTP_PORT", "465")),
            sender_email=os.getenv("SENDER_EMAIL", ""),
            sender_password=os.getenv("SENDER_PASSWORD", ""),
            receiver_email=os.getenv("RECEIVER_EMAIL", ""),
            deepseek_model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
            news_count=int(os.getenv("NEWS_COUNT", "2")),
            concept_count=int(os.getenv("CONCEPT_COUNT", "2")),
            max_retries=int(os.getenv("MAX_RETRIES", "3")),
            push_time=os.getenv("PUSH_TIME", "08:00"),
        )
