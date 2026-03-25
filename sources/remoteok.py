"""
RemoteOK — https://remoteok.com/api
Free JSON feed. Returns all jobs, we filter locally.
"""
import logging
from models import Job
from sources.http_utils import get_json

logger = logging.getLogger(__name__)

API_URL = "https://remoteok.com/api"


def fetch_remoteok() -> list[Job]:
    """Fetch jobs from RemoteOK JSON feed."""
    jobs: list[Job] = []

    data = get_json(API_URL)
    if not data or not isinstance(data, list):
        logger.warning("RemoteOK: no data returned")
        return jobs

    # First element is metadata, skip it
    for item in data[1:]:
        if not isinstance(item, dict):
            continue

        tags = item.get("tags", [])
        if isinstance(tags, str):
            tags = [tags]

        salary_min = item.get("salary_min")
        salary_max = item.get("salary_max")
        salary = ""
        if salary_min and salary_max:
            salary = f"${salary_min:,} - ${salary_max:,}"

        jobs.append(Job(
            id=str(item.get("id", "")),
            title=item.get("position", ""),
            company=item.get("company", ""),
            url=item.get("url", item.get("apply_url", "")),
            source="remoteok",
            location=item.get("location", "Worldwide"),
            job_type="",
            salary=salary,
            posted_date=item.get("date", ""),
            tags=tags,
        ))

    logger.info(f"RemoteOK: fetched {len(jobs)} total jobs (pre-filter)")
    return jobs
