from sources.remotive import fetch_remotive
from sources.himalayas import fetch_himalayas
from sources.jobicy import fetch_jobicy
from sources.remoteok import fetch_remoteok
from sources.arbeitnow import fetch_arbeitnow
from sources.wwr import fetch_wwr
from sources.workingnomads import fetch_workingnomads
from sources.jsearch import fetch_jsearch

ALL_FETCHERS = [
    ("remotive", fetch_remotive),
    ("himalayas", fetch_himalayas),
    ("jobicy", fetch_jobicy),
    ("remoteok", fetch_remoteok),
    ("arbeitnow", fetch_arbeitnow),
    ("weworkremotely", fetch_wwr),
    ("workingnomads", fetch_workingnomads),
    ("jsearch", fetch_jsearch),
]
