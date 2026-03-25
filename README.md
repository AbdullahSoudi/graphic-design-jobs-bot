# 🎨 Graphic Design Jobs — Telegram Bot

> بوت تليجرام بيجمع وظائف **Graphic Design Remote** من 7+ مصادر عالمية ويبعتها على قناة تليجرام كل 5 دقايق.

## المصادر 📡

| Source | Type | Category |
|--------|------|----------|
| Remotive | Free API | Design |
| Himalayas | Free API | Search by keyword |
| Jobicy | Free API | Design |
| RemoteOK | JSON Feed | All (filtered locally) |
| Arbeitnow | Free API | Remote only |
| We Work Remotely | RSS | Design |
| Working Nomads | RSS | Design |

## الفلتر 🎯

**بيقبل:**
- Graphic Designer, Visual Designer, Brand Designer
- Logo Designer, Social Media Designer, Print Designer
- Brand Identity, Packaging Designer, Illustration
- Motion Graphic, Art Director, Creative Designer
- مصمم جرافيك, هوية بصرية, تصميم سوشيال ميديا

**بيستبعد:**
- UI/UX Designer, Product Designer, Web Designer
- Frontend Designer, Game Designer, Interior Designer

## التشغيل 🚀

### 1. عمل Telegram Bot

1. كلم [@BotFather](https://t.me/BotFather) على تليجرام
2. ابعتله `/newbot` واتبع الخطوات
3. هيديك **Bot Token** — احفظه
4. اعمل Channel جديدة على تليجرام
5. ضيف البوت كـ **Admin** في القناة
6. الـ Channel ID هيبقى `@your_channel_name`

### 2. عمل GitHub Repository

```bash
# Clone أو اعمل repo جديد
git init graphic-design-jobs-bot
cd graphic-design-jobs-bot

# انسخ كل الملفات فيه
```

### 3. إضافة الـ Secrets

روح على **Settings → Secrets and variables → Actions** في الـ repo وضيف:

| Secret | Value |
|--------|-------|
| `TELEGRAM_BOT_TOKEN` | التوكن من BotFather |
| `TELEGRAM_CHANNEL_ID` | `@your_channel_name` |

### 4. Push والبوت هيشتغل

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

البوت هيشتغل أوتوماتيك كل 5 دقايق! تقدر كمان تشغله يدوي من **Actions → Run workflow**.

## التشغيل المحلي 🖥️

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export TELEGRAM_BOT_TOKEN="your_token_here"
export TELEGRAM_CHANNEL_ID="@your_channel"

# Run
python main.py
```

لو مفيش Telegram credentials، البوت هيطبع الوظائف في الـ terminal.

## هيكل المشروع 📂

```
├── main.py                 # Entry point
├── config.py               # Keywords, settings
├── models.py               # Job model + filter logic
├── dedup.py                # Duplicate detection
├── telegram_sender.py      # Telegram formatting + sending
├── sources/
│   ├── __init__.py         # All fetchers registry
│   ├── http_utils.py       # Shared HTTP client
│   ├── remotive.py         # Remotive API
│   ├── himalayas.py        # Himalayas API
│   ├── jobicy.py           # Jobicy API
│   ├── remoteok.py         # RemoteOK JSON
│   ├── arbeitnow.py        # Arbeitnow API
│   ├── wwr.py              # We Work Remotely RSS
│   └── workingnomads.py    # Working Nomads RSS
├── requirements.txt
└── .github/
    └── workflows/
        └── job_bot.yml     # GitHub Actions cron
```

## إضافة مصدر جديد ➕

1. اعمل ملف جديد في `sources/` (مثلاً `sources/dribbble.py`)
2. اعمل function اسمها `fetch_dribbble()` بترجع `list[Job]`
3. ضيفها في `sources/__init__.py` في `ALL_FETCHERS`

```python
# sources/my_source.py
from models import Job

def fetch_my_source() -> list[Job]:
    # Fetch and parse jobs
    return [Job(id=..., title=..., company=..., url=..., source="my_source")]
```

## الرخصة 📄

MIT — استخدمه زي ما تحب!
