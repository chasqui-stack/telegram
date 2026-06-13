from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Server — 8001 so it runs alongside the WhatsApp gateway (8000) locally
    port: int = 8001

    # Telegram Bot API
    telegram_bot_token: str
    # Shared secret echoed back by Telegram in the
    # `X-Telegram-Bot-Api-Secret-Token` header on every webhook call — the
    # gateway's authenticity check (Telegram's analog of Meta's app_secret HMAC).
    telegram_webhook_secret: str
    # Dev only (e.g. ngrok): when set, the gateway calls setWebhook on startup.
    # In production the webhook is registered once, out of band.
    telegram_webhook_url: str | None = None

    # Chasqui core
    core_url: str = "http://localhost:8090"
    internal_api_key: str = ""

    # Sentry (optional)
    sentry_dsn: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
