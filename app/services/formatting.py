"""Render canonical Markdown → Telegram MarkdownV2.

The core emits one canonical markup (standard Markdown, ARCHITECTURE §5);
each gateway renders it to its platform. Telegram's MarkdownV2 needs a long
list of characters escaped (``_*[]()~>#+-=|{}.!``) and uses single-`*` bold /
single-`_` italic — hand-rolling is bug-prone, so we lean on the
battle-tested `telegramify-markdown` converter.

`to_markdown_v2` never raises: if conversion fails, return None so the caller
can fall back to sending the original text as plain (no parse_mode).
"""

import logging

import telegramify_markdown

logger = logging.getLogger(__name__)


def to_markdown_v2(text: str | None) -> str | None:
    """Convert standard Markdown to Telegram MarkdownV2 (None on empty/failure)."""
    if not text:
        return None
    try:
        return telegramify_markdown.markdownify(text)
    except Exception:
        logger.warning("MarkdownV2 conversion failed — will send plain", exc_info=True)
        return None
