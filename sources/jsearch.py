"""
JSearch (via RapidAPI) — aggregates LinkedIn, Indeed, Glassdoor & more.
https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch

Free tier: 200 requests/month.
"""
import os
import logging
import requests
from models import Job

logger = logging.getLogger(__name__)

API_URL = "https://jsearch.p.rapidapi.com/search"
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")

# Search queries to cover graphic design variations
SEARCH_QUERIES = [
    "graphic designer remote",
    "brand identity designer remote",
    "social media designer remote",
    "logo designer remote",
    "مصمم جرافيك عن بعد",
]


def fetch_jsearch() -> list[Job]:
    """Fetch graphic design jobs from JSearch API (LinkedIn, Indeed, etc.)."""
    if not RAPIDAPI_KEY:
        logger.warning("JSearch: RAPIDAPI_KEY not set, skipping")
        return []

    jobs: list[Job] = []
    seen_ids: set[str] = set()

    headers = {
        "x-rapidapi-host": "jsearch.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY,
    }

    for query in SEARCH_QUERIES:
        try:
            resp = requests.get(
                API_URL,
                headers=headers,
                params={
                    "query": query,
                    "page": "1",
                    "num_pages": "1",
                    "date_posted": "today",        # Only recent jobs
                    "remote_jobs_only": "true",     # Remote only
                },
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()

            if not data.get("data"):
                continue

            for item in data["data"]:
                job_id = item.get("job_id", "")
                if job_id in seen_ids:
                    continue
                seen_ids.add(job_id)

                # Get the best apply link
                apply_link = item.get("job_apply_link", "")
                
                # Detect source (LinkedIn, Indeed, etc.)
                publisher = item.get("job_publisher", "")

                # Salary info
                salary = ""
                sal_min = item.get("job_min_salary")
                sal_max = item.get("job_max_salary")
                sal_currency = item.get("job_salary_currency", "USD")
                if sal_min and sal_max:
                    salary = f"{sal_currency} {sal_min:,.0f} - {sal_max:,.0f}"
                elif sal_min:
                    salary = f"{sal_currency} {sal_min:,.0f}+"

                # Location
                city = item.get("job_city", "")
                country = item.get("job_country", "")
                is_remote = item.get("job_is_remote", False)
                location = "Remote"
                if city and country:
                    location = f"Remote — {city}, {country}"
                elif country:
                    location = f"Remote — {country}"

                jobs.append(Job(
                    id=job_id,
                    title=item.get("job_title", ""),
                    company=item.get("employer_name", ""),
                    url=apply_link,
                    source="jsearch",
                    location=location,
                    job_type=item.get("job_employment_type", ""),
                    salary=salary,
                    posted_date=item.get("job_posted_at_datetime_utc", ""),
                    tags=[publisher] if publisher else [],
                ))

        except Exception as e:
            logger.warning(f"JSearch query '{query}' failed: {e}")
            continue

    logger.info(f"JSearch: fetched {len(jobs)} jobs (LinkedIn, Indeed, etc.)")
    return jobs
