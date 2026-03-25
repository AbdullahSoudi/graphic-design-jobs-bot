#!/usr/bin/env python3
"""
Graphic Design Jobs Telegram Bot
─────────────────────────────────
Fetches remote graphic design jobs from 7+ sources,
filters for relevant roles, deduplicates, and posts
new listings to a Telegram channel.
"""
import logging
import sys
import time
from datetime import datetime, timezone

from models import filter_jobs
from dedup import load_seen_jobs, save_seen_jobs, filter_new_jobs
from telegram_sender import send_jobs
from sources import ALL_FETCHERS

# ── Logging setup ─────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-7s │ %(name)s │ %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("main")


def main():
    start = time.time()
    logger.info("=" * 55)
    logger.info("🎨 Graphic Design Jobs Bot — starting run")
    logger.info(f"   Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    logger.info("=" * 55)

    # ── Step 1: Fetch from all sources ────────────────────
    all_jobs = []
    for source_name, fetcher in ALL_FETCHERS:
        try:
            logger.info(f"Fetching from {source_name}...")
            jobs = fetcher()
            all_jobs.extend(jobs)
            logger.info(f"  → {len(jobs)} raw jobs from {source_name}")
        except Exception as e:
            logger.error(f"  ✗ {source_name} failed: {e}")

    logger.info(f"\n📦 Total raw jobs fetched: {len(all_jobs)}")

    # ── Step 2: Filter for graphic design + remote ────────
    filtered = filter_jobs(all_jobs)
    logger.info(f"🎯 After keyword filter: {len(filtered)} graphic design jobs")

    if not filtered:
        logger.info("No matching jobs found this run. Exiting.")
        return

    # ── Step 3: Deduplicate ───────────────────────────────
    seen = load_seen_jobs()
    is_first_run = len(seen) == 0
    logger.info(f"📚 Previously seen: {len(seen)} jobs")

    if is_first_run:
        # ── SEED MODE: first run — save all current jobs as "seen"
        #    without posting them. Only truly NEW jobs from next run
        #    onwards will be sent to Telegram.
        logger.info("=" * 55)
        logger.info("🌱 FIRST RUN — Seed mode activated!")
        logger.info(f"   Marking {len(filtered)} existing jobs as seen...")
        logger.info("   NO messages will be sent this run.")
        logger.info("   Next run will only post NEW jobs.")
        logger.info("=" * 55)
        for job in filtered:
            seen.add(job.dedup_key)
        save_seen_jobs(seen)
        logger.info(f"✅ Seeded {len(seen)} jobs. Next run will post only new ones!")
        return

    new_jobs = filter_new_jobs(filtered, seen)
    logger.info(f"🆕 New jobs to post: {len(new_jobs)}")

    if not new_jobs:
        logger.info("No new jobs to post. Saving state and exiting.")
        save_seen_jobs(seen)
        return

    # ── Step 4: Send to Telegram ──────────────────────────
    logger.info(f"\n📤 Sending {len(new_jobs)} jobs to Telegram...")
    sent_count = send_jobs(new_jobs)
    logger.info(f"✅ Successfully sent: {sent_count}/{len(new_jobs)}")

    # ── Step 5: Save state ────────────────────────────────
    save_seen_jobs(seen)

    elapsed = time.time() - start
    logger.info(f"\n⏱️  Run completed in {elapsed:.1f}s")
    logger.info("=" * 55)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Unhandled error: {e}", exc_info=True)
        sys.exit(1)
