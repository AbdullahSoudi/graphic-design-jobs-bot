"""
Shared HTTP utilities for fetching data from sources.
"""
import requests
import config
import logging

logger = logging.getLogger(__name__)

_session: requests.Session | None = None


def get_session() -> requests.Session:
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update({
            "User-Agent": config.USER_AGENT,
            "Accept": "application/json",
        })
    return _session


def get_json(url: str, params: dict | None = None) -> dict | list | None:
    """GET request returning parsed JSON, or None on failure."""
    try:
        resp = get_session().get(url, params=params, timeout=config.REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return None


def get_text(url: str) -> str | None:
    """GET request returning raw text (for RSS/XML), or None on failure."""
    try:
        s = get_session()
        s.headers.update({"Accept": "application/rss+xml, application/xml, text/xml"})
        resp = s.get(url, timeout=config.REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return None
