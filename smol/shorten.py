from json import loads
from logging import getLogger
from random import choice

import validators

from smol.alb_types import AlbEvent
from smol.captcha import Captcha
from smol.exceptions import BadMethod, BadRequest, SmolError
from smol.link import ID_CHARS, ID_LENGTH
from smol.link import Link
from smol.safe_site import SafeSite

MAX_GENERATION_ATTEMPTS = 100

LOGGER = getLogger(__name__)


class Shortener:
    """
    Handles shortening links
    """

    def __init__(self, request: AlbEvent) -> None:
        if request["httpMethod"].upper() != "POST":
            raise BadMethod()
        if request["headers"].get("content-type", None) != "application/json":
            raise BadRequest()

        body = loads(request.get("body", "{}"))
        self.target = str(body.get("target", str()))
        self.token = str(body.get("token", str()))

    @staticmethod
    def _generate_id() -> str:
        LOGGER.info("Generating new ID...")
        new_id = None
        attempts = 0

        while attempts < MAX_GENERATION_ATTEMPTS:
            attempts += 1
            LOGGER.info(f"Generating new ID attempt {attempts}...")
            id_chars = list()
            for _ in range(ID_LENGTH):
                id_chars.append(choice(ID_CHARS))
            new_id = "".join(id_chars)

            try:
                collision = Link.get(new_id)
                LOGGER.info(f"Collision check for {new_id} returned {collision.id}")
            except Link.DoesNotExist:
                return new_id

        LOGGER.critical(f"Exceeded {MAX_GENERATION_ATTEMPTS} attempts!")
        raise SmolError()

    def shorten_link(self) -> Link:
        """
        Creates new short link
        """
        if not Captcha.verify_captcha(self.token):
            LOGGER.warning(f"Invalid token: {self.token}")
            raise BadRequest()

        if not validators.url(self.target, public=True):
            LOGGER.warning(f"Invalid target: {self.target}")
            raise BadRequest()

        if not SafeSite.is_safe_site(self.target):
            LOGGER.warning(f"Unsafe target: {self.target}")
            raise BadRequest()

        target_id = self._generate_id()
        new_link = Link(id=target_id, target=self.target)
        new_link.save()
        return new_link
