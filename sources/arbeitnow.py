"""
Arbeitnow — https://www.arbeitnow.com/api/job-board-api
Free public API with remote filter.
"""
import logging
from models import Job
from sources.http_utils import get_json

logger = logging.getLogger(__name__)

API_URL = "https://www.arbeitnow.com/api/job-board-api"


def fetch_arbeitnow() -> list[Job]:
    """Fetch remote jobs from Arbeitnow API."""
    jobs: list[Job] = []

    data = get_json(API_URL)
    if not data or "data" not in data:
        logger.warning("Arbeitnow: no data returned")
        return jobs

    for item in data["data"]:
        if not item.get("remote", False):
            continue

        tags = item.get("tags", [])
        if isinstance(tags, str):
            tags = [tags]

        jobs.append(Job(
            id=str(item.get("slug", "")),
            title=item.get("title", ""),
            company=item.get("company_name", ""),
            url=item.get("url", ""),
            source="arbeitnow",
            location=item.get("location", "Remote"),
            job_type=item.get("job_types", [""])[0] if item.get("job_types") else "",
            salary="",
            posted_date=item.get("created_at", ""),
            tags=tags,
        ))

    logger.info(f"Arbeitnow: fetched {len(jobs)} remote jobs (pre-filter)")
    return jobs
