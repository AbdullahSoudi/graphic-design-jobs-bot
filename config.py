"""
Configuration for Graphic Design Jobs Telegram Bot
"""
import os

# ── Telegram ──────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")  # e.g. "@your_channel"

# ── Keywords ──────────────────────────────────────────────
# Include: job title must match at least one of these (case-insensitive)
INCLUDE_KEYWORDS = [
    "graphic design",
    "graphic designer",
    "visual designer",
    "brand designer",
    "brand identity",
    "logo design",
    "logo designer",
    "social media design",
    "social media designer",
    "print designer",
    "print design",
    "packaging design",
    "packaging designer",
    "illustrator",
    "illustration",
    "creative designer",
    "motion graphic",
    "motion designer",
    "art director",
    "visual identity",
    "branding designer",
    "graphic artist",
    # Arabic keywords
    "مصمم جرافيك",
    "تصميم جرافيك",
    "مصمم هوية بصرية",
    "هوية بصرية",
    "تصميم لوجو",
    "تصميم سوشيال ميديا",
    "مصمم سوشيال",
]

# Exclude: skip if title matches any of these
EXCLUDE_KEYWORDS = [
    "ui designer",
    "ux designer",
    "ui/ux",
    "ux/ui",
    "product designer",
    "web designer",
    "web developer",
    "frontend designer",
    "front-end designer",
    "interaction designer",
    "service designer",
    "game designer",
    "instructional designer",
    "interior designer",
    "fashion designer",
    "sound designer",
    "hardware designer",
]

# ── Remote filter keywords ────────────────────────────────
REMOTE_KEYWORDS = [
    "remote",
    "anywhere",
    "worldwide",
    "work from home",
    "distributed",
    "عن بعد",
    "عن بُعد",
]

# ── Source emoji map ──────────────────────────────────────
SOURCE_EMOJI = {
    "remotive": "🟢",
    "himalayas": "🏔️",
    "jobicy": "💼",
    "remoteok": "🚀",
    "arbeitnow": "🇪🇺",
    "weworkremotely": "🌍",
    "workingnomads": "🧳",
    "wuzzuf": "🇪🇬",
    "dribbble": "🏀",
    "jsearch": "🔍",
}

# ── Dedup ─────────────────────────────────────────────────
SEEN_JOBS_FILE = os.getenv("SEEN_JOBS_FILE", "seen_jobs.json")
MAX_SEEN_JOBS = 5000  # keep last N to avoid file growing forever

# ── Request settings ──────────────────────────────────────
REQUEST_TIMEOUT = 15  # seconds
USER_AGENT = "GraphicDesignJobsBot/1.0"
