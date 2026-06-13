"""Canonical outbound sending (ADR-004) → Telegram Bot API — SCAFFOLD (#10).

The mirror of /ingest: the core POSTs a canonical message to /send and this
service renders it on Telegram. To be implemented in chasqui-stack/chasqui#10.

Mirror of whatsapp/app/services/sender.py, but SIMPLER:
  - addressing is the chat id (contact.external_id); no wa_id requirement,
    so no NO_WA_ID error.
  - Telegram has no 24h customer-service window → no ReEngagementMessage /
    WINDOW_EXPIRED. Failures collapse to SEND_FAILED (e.g. 403 "bot was
    blocked by the user").
  - SendRequest/SendContact/SendMessage Pydantic models + _decode_data_uri
    (base64 data: URI → bytes) copied from the WhatsApp gateway.
  - type dispatch → sendMessage / sendPhoto / sendVoice (ogg) | sendAudio /
    sendDocument.
"""
