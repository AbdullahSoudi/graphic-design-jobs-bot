"""
Remotive — https://remotive.com/api/remote-jobs
Free public API with category filter.
"""
import logging
from models import Job
from sources.http_utils import get_json

logger = logging.getLogger(__name__)

API_URL = "https://remotive.com/api/remote-jobs"


def fetch_remotive() -> list[Job]:
    """Fetch design jobs from Remotive API."""
    jobs: list[Job] = []

    # Fetch "design" category
    data = get_json(API_URL, params={"category": "design", "limit": 50})
    if not data or "jobs" not in data:
        logger.warning("Remotive: no data returned")
        return jobs

    for item in data["jobs"]:
        jobs.append(Job(
            id=str(item.get("id", "")),
            title=item.get("title", ""),
            company=item.get("company_name", ""),
            url=item.get("url", ""),
            source="remotive",
            location=item.get("candidate_required_location", "Worldwide"),
            job_type=item.get("job_type", ""),
            salary=item.get("salary", ""),
            posted_date=item.get("publication_date", ""),
            tags=item.get("tags", []),
        ))

    logger.info(f"Remotive: fetched {len(jobs)} design jobs")
    return jobs
