"""Inbound media → self-contained data URI — SCAFFOLD (#9).

Telegram file URLs require the bot token and are channel-private, so the
channel-agnostic core can never fetch them. The gateway downloads the bytes
(getFile(file_id) → file_path → https://api.telegram.org/file/bot<TOKEN>/<path>)
and ships them inline in the canonical `media_url` as `data:<mime>;base64,…`.

Mirror of whatsapp/app/services/media.py — keep the MAX_MEDIA_BYTES cap and the
never-raise posture (return None on failure → the turn proceeds text-only).
To be implemented in chasqui-stack/chasqui#9.
"""
