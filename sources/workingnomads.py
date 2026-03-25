"""
Working Nomads — RSS feed for Design category.
https://www.workingnomads.com/remote-design-jobs (RSS)
"""
import logging
import xml.etree.ElementTree as ET
from models import Job
from sources.http_utils import get_text

logger = logging.getLogger(__name__)

RSS_URL = "https://www.workingnomads.com/jobsrss/design"


def fetch_workingnomads() -> list[Job]:
    """Fetch design jobs from Working Nomads RSS feed."""
    jobs: list[Job] = []

    xml_text = get_text(RSS_URL)
    if not xml_text:
        # Try alternative URL
        xml_text = get_text("https://www.workingnomads.com/jobs/rss/design")
        if not xml_text:
            logger.warning("Working Nomads: no data returned")
            return jobs

    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        logger.warning(f"Working Nomads: XML parse error: {e}")
        return jobs

    for item in root.findall(".//item"):
        title_el = item.find("title")
        link_el = item.find("link")
        pubdate_el = item.find("pubDate")

        title = title_el.text.strip() if title_el is not None and title_el.text else ""
        link = link_el.text.strip() if link_el is not None and link_el.text else ""
        pubdate = pubdate_el.text.strip() if pubdate_el is not None and pubdate_el.text else ""

        # Try to extract company from description
        desc_el = item.find("description")
        company = ""
        if desc_el is not None and desc_el.text:
            # Some feeds include company name in description
            desc = desc_el.text.strip()
            if " at " in title:
                parts = title.rsplit(" at ", 1)
                title = parts[0].strip()
                company = parts[1].strip()

        job_id = link.split("/")[-1] if link else title

        jobs.append(Job(
            id=job_id,
            title=title,
            company=company,
            url=link,
            source="workingnomads",
            location="Remote",
            posted_date=pubdate,
        ))

    logger.info(f"Working Nomads: fetched {len(jobs)} design jobs")
    return jobs
