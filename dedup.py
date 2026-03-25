"""
Deduplication: persist seen job keys between runs.
Uses a JSON file that gets cached in GitHub Actions.
"""
import json
import logging
import os
from models import Job
import config

logger = logging.getLogger(__name__)


def load_seen_jobs() -> set[str]:
    """Load previously seen job keys from file."""
    filepath = config.SEEN_JOBS_FILE
    if not os.path.exists(filepath):
        return set()
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data) if isinstance(data, list) else set()
    except (json.JSONDecodeError, IOError) as e:
        logger.warning(f"Error loading seen jobs: {e}")
        return set()


def save_seen_jobs(seen: set[str]) -> None:
    """Save seen job keys to file, keeping only the latest N."""
    # Keep only the most recent entries to prevent unbounded growth
    seen_list = list(seen)
    if len(seen_list) > config.MAX_SEEN_JOBS:
        seen_list = seen_list[-config.MAX_SEEN_JOBS:]

    try:
        with open(config.SEEN_JOBS_FILE, "w", encoding="utf-8") as f:
            json.dump(seen_list, f)
        logger.info(f"Saved {len(seen_list)} seen job keys")
    except IOError as e:
        logger.error(f"Error saving seen jobs: {e}")


def filter_new_jobs(jobs: list[Job], seen: set[str]) -> list[Job]:
    """Return only jobs not previously seen."""
    new_jobs = []
    for job in jobs:
        key = job.dedup_key
        if key not in seen:
            new_jobs.append(job)
            seen.add(key)
    return new_jobs
