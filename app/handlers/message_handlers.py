"""Telegram message handlers — SCAFFOLD (#9).

Mirror of whatsapp/app/handlers/message_handlers.py: pure `payload_from_*`
builders (no I/O, unit-testable) that normalize a Telegram update to the
canonical contract (ARCHITECTURE §5), plus a `process_update` coroutine that
does the core round-trip and a `_reply_canonical` that renders the response.

To be implemented in chasqui-stack/chasqui#9. Key mapping notes:
  - channel = "telegram"
  - contact.external_id = message.chat.id (stable per conversation; Telegram
    has no BSUID). Keep user id / username in contact.metadata. wa_id is None.
  - inbound media: getFile(file_id) → download → base64 data: URI in media_url
    (mirror whatsapp/app/services/media.py — size-capped, never-raise).
  - callback_query → canonical "button" message.
"""
