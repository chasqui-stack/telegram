"""Chasqui Telegram gateway — stateless channel adapter.

Mirror of the WhatsApp gateway (chasqui-stack/whatsapp): receive Telegram
webhook updates, normalize to the canonical contract (ARCHITECTURE §5), POST
the core's /ingest, render the canonical response back to Telegram. Plus the
canonical outbound contract POST /send (ADR-004) for the human-handoff inbox.

This is the SCAFFOLD (epic chasqui-stack/chasqui#6). The app boots and /health
works; inbound webhook processing (#9) and outbound /send (#10) are stubbed —
see the TODOs. The library + webhook-integration decision is ADR-006 (#7).
"""

import logging
from contextlib import asynccontextmanager
from typing import Annotated

import sentry_sdk
from fastapi import FastAPI, Header, HTTPException, Request

from app.core.config import settings

if settings.sentry_dsn:
    sentry_sdk.init(dsn=settings.sentry_dsn, traces_sample_rate=0.1)

from app.services.core_client import CoreClient  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

core_client: CoreClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global core_client
    core_client = CoreClient(base_url=settings.core_url, api_key=settings.internal_api_key)
    logger.info("Chasqui Telegram gateway started — core=%s", settings.core_url)
    # TODO(#9): if settings.telegram_webhook_url is set, register it with
    # setWebhook(secret_token=settings.telegram_webhook_secret) here.
    yield
    if core_client:
        await core_client.close()


app = FastAPI(
    title="Chasqui Telegram Gateway",
    description="Stateless Telegram channel adapter",
    version="0.1.0",
    lifespan=lifespan,
)


def get_core() -> CoreClient:
    if core_client is None:
        raise RuntimeError("CoreClient not initialized")
    return core_client


def _verify_webhook_secret(token: str | None) -> None:
    """Telegram echoes the secret set via setWebhook on every call."""
    if token != settings.telegram_webhook_secret:
        raise HTTPException(
            status_code=401,
            detail={"code": "UNAUTHORIZED", "message": "Invalid webhook secret"},
        )


@app.post("/webhook")
async def webhook(
    request: Request,
    x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None,
):
    """Telegram update entry point — verify, ack fast, process async.

    TODO(#9): parse the Update, build the canonical payload (channel="telegram",
    contact.external_id = chat id), inline media as base64 data: URIs, and
    dispatch the core round-trip as a background task (the whatsapp/ ack-fast
    pattern). For now we only authenticate and ack.
    """
    _verify_webhook_secret(x_telegram_bot_api_secret_token)
    await request.body()  # drain
    logger.info("Webhook received (processing not yet implemented — #9)")
    return {"ok": True}


@app.post("/send")
async def send_message(
    x_internal_api_key: Annotated[str | None, Header()] = None,
):
    """Canonical outbound contract (ADR-004) — mirror of the core's /ingest.

    TODO(#10): accept the canonical SendRequest and render it on Telegram via
    sendMessage/sendPhoto/sendVoice/sendDocument, addressed by chat id. No 24h
    window (unlike WhatsApp), so no WINDOW_EXPIRED.
    """
    if settings.internal_api_key and x_internal_api_key != settings.internal_api_key:
        raise HTTPException(
            status_code=401,
            detail={"code": "UNAUTHORIZED", "message": "Invalid internal API key"},
        )
    raise HTTPException(
        status_code=501,
        detail={"code": "NOT_IMPLEMENTED", "message": "POST /send lands in #10"},
    )


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "chasqui-telegram"}
