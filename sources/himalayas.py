"""
Himalayas — https://himalayas.app/jobs/api
Free public JSON API, no auth required. Search by keyword.
"""
import logging
from models import Job
from sources.http_utils import get_json

logger = logging.getLogger(__name__)

SEARCH_URL = "https://himalayas.app/jobs/api/search"

# Multiple search terms to cover graphic design variations
SEARCH_QUERIES = [
    "graphic designer",
    "brand designer",
    "visual designer",
    "logo designer",
    "social media designer",
]


def fetch_himalayas() -> list[Job]:
    """Fetch graphic design jobs from Himalayas search API."""
    jobs: list[Job] = []
    seen_ids: set[str] = set()

    for query in SEARCH_QUERIES:
        data = get_json(SEARCH_URL, params={"query": query, "limit": 20})
        if not data or "jobs" not in data:
            continue

        for item in data["jobs"]:
            job_id = str(item.get("id", ""))
            if job_id in seen_ids:
                continue
            seen_ids.add(job_id)

            # Build URL
            slug = item.get("slug", "")
            company_slug = item.get("companySlug", "")
            url = f"https://himalayas.app/companies/{company_slug}/jobs/{slug}" if slug else ""

            locations = item.get("locationRestrictions", [])
            location_str = ", ".join(locations) if locations else "Worldwide"

            salary_min = item.get("minSalary")
            salary_max = item.get("maxSalary")
            salary = ""
            if salary_min and salary_max:
                salary = f"${salary_min:,} - ${salary_max:,}"
            elif salary_min:
                salary = f"${salary_min:,}+"

            categories = item.get("categories", [])

            jobs.append(Job(
                id=job_id,
                title=item.get("title", ""),
                company=item.get("companyName", ""),
                url=url,
                source="himalayas",
                location=location_str,
                job_type=item.get("employmentType", ""),
                salary=salary,
                posted_date=item.get("pubDate", ""),
                tags=categories,
            ))

    logger.info(f"Himalayas: fetched {len(jobs)} jobs")
    return jobs
