from logging import getLogger
from os import environ

import requests
from requests.exceptions import HTTPError

SAFE_BROWSING_KEY = environ.get("SAFE_BROWSING_KEY", str())
SAFE_BROWSING_URI = (
    f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={SAFE_BROWSING_KEY}"
)
THREATS = ("MALWARE", "SOCIAL_ENGINEERING", "POTENTIALLY_HARMFUL_APPLICATION")
LOGGER = getLogger(__name__)


class SafeSite:
    """
    Handles Safe Browsing site verification
    """

    @staticmethod
    def is_safe_site(url: str) -> bool:
        """
        Verify site is not dangerous per Google Safe Browsing API
        """
        LOGGER.info(f"Checking if {url} is safe...")
        try:
            LOGGER.info("Calling safe browsing API...")
            resp = requests.post(
                SAFE_BROWSING_URI,
                json={
                    "client": {"clientId": "smol.io"},
                    "threatInfo": {
                        "threatTypes": THREATS,
                        "platformTypes": ["ANY_PLATFORM"],
                        "threatEntryTypes": ["URL"],
                        "threatEntries": [
                            {"url": url},
                        ],
                    },
                },
            )
            resp.raise_for_status()
            LOGGER.info("Successfully called safe browsing API.")
            resp_data = resp.json()
            threat_matches = resp_data.get("matches", list())
        except HTTPError as err:
            LOGGER.exception(f"Site check failed: {err}")
            # when in doubt, reject
            return False

        LOGGER.warning(
            f"Safe Browsing check returned {len(threat_matches)} threat matches."
        )
        if threat_matches:
            return False

        return True
