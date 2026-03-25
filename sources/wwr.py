"""
We Work Remotely — RSS feed for Design category.
https://weworkremotely.com/categories/remote-design-jobs.rss
"""
import logging
import xml.etree.ElementTree as ET
from models import Job
from sources.http_utils import get_text

logger = logging.getLogger(__name__)

RSS_URL = "https://weworkremotely.com/categories/remote-design-jobs.rss"


def fetch_wwr() -> list[Job]:
    """Fetch design jobs from We Work Remotely RSS feed."""
    jobs: list[Job] = []

    xml_text = get_text(RSS_URL)
    if not xml_text:
        logger.warning("WWR: no data returned")
        return jobs

    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        logger.warning(f"WWR: XML parse error: {e}")
        return jobs

    for item in root.findall(".//item"):
        title_el = item.find("title")
        link_el = item.find("link")
        pubdate_el = item.find("pubDate")
        # WWR title format: "Company: Job Title"
        raw_title = title_el.text if title_el is not None and title_el.text else ""
        link = link_el.text if link_el is not None and link_el.text else ""
        pubdate = pubdate_el.text if pubdate_el is not None and pubdate_el.text else ""

        company = ""
        title = raw_title
        if ":" in raw_title:
            parts = raw_title.split(":", 1)
            company = parts[0].strip()
            title = parts[1].strip()

        # Use link as unique ID
        job_id = link.split("/")[-1] if link else raw_title

        jobs.append(Job(
            id=job_id,
            title=title,
            company=company,
            url=link,
            source="weworkremotely",
            location="Remote",
            posted_date=pubdate,
        ))

    logger.info(f"WWR: fetched {len(jobs)} design jobs")
    return jobs
