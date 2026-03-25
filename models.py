"""
Job model and filtering logic.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import config


@dataclass
class Job:
    id: str
    title: str
    company: str
    url: str
    source: str
    location: str = ""
    job_type: str = ""       # full_time, contract, freelance, etc.
    salary: str = ""
    posted_date: str = ""
    tags: list[str] = field(default_factory=list)

    @property
    def dedup_key(self) -> str:
        """Unique key for deduplication across sources."""
        # Normalize: lowercase title + company combo handles cross-source dupes
        norm_title = self.title.lower().strip()
        norm_company = self.company.lower().strip()
        return f"{self.source}:{self.id}" if self.id else f"{norm_title}||{norm_company}"


def matches_keywords(text: str, keywords: list[str]) -> bool:
    """Check if text contains any of the keywords (case-insensitive)."""
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in keywords)


def is_graphic_design_job(job: Job) -> bool:
    """Filter: must match include keywords and NOT match exclude keywords."""
    searchable = f"{job.title} {' '.join(job.tags)}".strip()

    # Must match at least one include keyword
    if not matches_keywords(searchable, config.INCLUDE_KEYWORDS):
        return False

    # Must NOT match any exclude keyword
    if matches_keywords(job.title, config.EXCLUDE_KEYWORDS):
        return False

    return True


def is_remote_job(job: Job) -> bool:
    """Check if job is remote. Some sources are remote-only so we skip check."""
    remote_only_sources = {
        "remotive", "remoteok", "weworkremotely", "workingnomads",
        "himalayas", "jobicy", "arbeitnow", "jsearch",
    }
    if job.source in remote_only_sources:
        return True

    searchable = f"{job.title} {job.location}".strip()
    return matches_keywords(searchable, config.REMOTE_KEYWORDS)


def filter_jobs(jobs: list[Job]) -> list[Job]:
    """Apply all filters to a list of jobs."""
    return [j for j in jobs if is_graphic_design_job(j) and is_remote_job(j)]
