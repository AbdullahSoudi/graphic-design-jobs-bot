"""
Telegram message formatting and sending.
"""
import logging
import time
import requests
from models import Job
import config

logger = logging.getLogger(__name__)

TELEGRAM_API = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}"


def format_job_message(job: Job) -> str:
    """Format a single job into a Telegram-friendly HTML message."""
    emoji = config.SOURCE_EMOJI.get(job.source, "📋")

    lines = [f"{emoji} <b>{escape_html(job.title)}</b>"]

    if job.company:
        lines.append(f"🏢 {escape_html(job.company)}")
    if job.location:
        lines.append(f"📍 {escape_html(job.location)}")
    if job.salary:
        lines.append(f"💰 {escape_html(job.salary)}")
    if job.job_type:
        lines.append(f"📅 {escape_html(job.job_type)}")

    lines.append("")
    if job.url:
        lines.append(f"🔗 <a href=\"{job.url}\">Apply / View Job</a>")

    lines.append(f"\n<i>Source: {escape_html(job.source.title())}</i>")

    return "\n".join(lines)


def escape_html(text: str) -> str:
    """Escape HTML special characters for Telegram HTML parse mode."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def send_message(text: str) -> bool:
    """Send a message to the Telegram channel."""
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHANNEL_ID:
        logger.warning("Telegram credentials not set, printing instead:")
        print(text)
        print("─" * 50)
        return True

    try:
        resp = requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": config.TELEGRAM_CHANNEL_ID,
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": False,
            },
            timeout=10,
        )
        if resp.status_code == 200:
            return True
        elif resp.status_code == 429:
            # Rate limited — extract retry_after
            retry_after = resp.json().get("parameters", {}).get("retry_after", 5)
            logger.warning(f"Telegram rate limited, waiting {retry_after}s")
            time.sleep(retry_after)
            return send_message(text)  # retry once
        else:
            logger.error(f"Telegram API error {resp.status_code}: {resp.text}")
            return False
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {e}")
        return False


def send_jobs(jobs: list[Job]) -> int:
    """Send all jobs to Telegram channel. Returns count of successfully sent."""
    sent = 0
    for job in jobs:
        msg = format_job_message(job)
        if send_message(msg):
            sent += 1
            # Respect Telegram rate limits: max 20 msgs/min to a channel
            time.sleep(3)
    return sent
