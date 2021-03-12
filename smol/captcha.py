from logging import getLogger
from os import environ
from typing import Optional

import requests
from requests.exceptions import HTTPError

CAPTCHA_KEY = environ["CAPTCHA_KEY"]
CAPTCHA_URI = "https://www.google.com/recaptcha/api/siteverify"
LOGGER = getLogger(__name__)


class Captcha:
    """
    Handles reCaptcha verification
    """

    @staticmethod
    def verify_captcha(token: Optional[str] = None) -> bool:
        """
        Verify reCaptcha challenge token
        """
        if not token:
            LOGGER.warning("No Captcha token provided!")
            return False

        try:
            resp = requests.post(
                CAPTCHA_URI, data={"secret": CAPTCHA_KEY, "response": token}
            )
            resp.raise_for_status()
            resp_data = resp.json()
            verify_success = resp_data.get("success", False)
            verify_score = resp_data.get("score", 0.0)
        except HTTPError as err:
            LOGGER.exception(f"Captcha Verification failed: {err}")
            # when in doubt, reject
            return False

        if verify_success:
            LOGGER.info(f"Captcha check succeeded with score: {verify_score}")
            return True

        LOGGER.warning(f"Captcha check failed with score: {verify_score}")
        return False
