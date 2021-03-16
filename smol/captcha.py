from logging import getLogger
from os import environ

import requests
from requests.exceptions import HTTPError

CAPTCHA_KEY = environ.get("CAPTCHA_KEY", str())
CAPTCHA_URI = "https://www.google.com/recaptcha/api/siteverify"
LOGGER = getLogger(__name__)


class Captcha:
    """
    Handles reCaptcha verification
    """

    @staticmethod
    def verify_captcha(token: str) -> bool:
        """
        Verify reCaptcha challenge token
        """
        LOGGER.info("Checking if reCaptcha challenge is valid...")
        try:
            LOGGER.info("Calling reCaptcha API...")
            resp = requests.post(
                CAPTCHA_URI,
                data={"secret": CAPTCHA_KEY, "response": token},
                # https://stackoverflow.com/a/52416003
                headers={"content-type": "application/x-www-form-urlencoded"},
            )
            resp.raise_for_status()
            LOGGER.info("Successfully called reCaptcha API.")
            resp_data = resp.json()
            verify_success = resp_data.get("success", False)
            verify_score = resp_data.get("score", 0.0)
            captcha_errs = resp_data.get("error-codes", list())
        except HTTPError as err:
            LOGGER.exception(f"Captcha Verification failed: {err}")
            # when in doubt, reject
            return False

        if verify_success:
            LOGGER.info(f"Captcha check succeeded with score: {verify_score}")
            return True

        LOGGER.warning(
            f"Captcha check failed with score: {verify_score} "
            f"and errors: {captcha_errs}"
        )
        return False
