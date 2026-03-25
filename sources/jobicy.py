"""
Jobicy — https://jobicy.com/api/v2/remote-jobs
Free public API with industry/tag filters.
"""
import logging
from models import Job
from sources.http_utils import get_json

logger = logging.getLogger(__name__)

API_URL = "https://jobicy.com/api/v2/remote-jobs"


def fetch_jobicy() -> list[Job]:
    """Fetch design jobs from Jobicy API."""
    jobs: list[Job] = []

    data = get_json(API_URL, params={
        "count": 50,
        "industry": "design",
        "tag": "graphic design",
    })

    if not data or "jobs" not in data:
        # Try without tag filter
        data = get_json(API_URL, params={"count": 50, "industry": "design"})
        if not data or "jobs" not in data:
            logger.warning("Jobicy: no data returned")
            return jobs

    for item in data["jobs"]:
        salary_min = item.get("annualSalaryMin", "")
        salary_max = item.get("annualSalaryMax", "")
        salary = ""
        if salary_min and salary_max:
            salary = f"${salary_min} - ${salary_max}"

        jobs.append(Job(
            id=str(item.get("id", "")),
            title=item.get("jobTitle", ""),
            company=item.get("companyName", ""),
            url=item.get("url", ""),
            source="jobicy",
            location=item.get("jobGeo", "Worldwide"),
            job_type=item.get("jobType", ""),
            salary=salary,
            posted_date=item.get("pubDate", ""),
            tags=item.get("jobIndustry", []) if isinstance(item.get("jobIndustry"), list) else [],
        ))

    logger.info(f"Jobicy: fetched {len(jobs)} design jobs")
    return jobs
