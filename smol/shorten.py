from json import loads, JSONDecodeError
from logging import getLogger
from random import choice

import validators

from smol.models import LambdaRequest
from smol.captcha import Captcha
from smol.exceptions import BadRequest, SmolError
from smol.link import ID_CHARS, ID_LENGTH
from smol.link import Link
from smol.safe_site import SafeSite

MAX_GENERATION_ATTEMPTS = 100

LOGGER = getLogger(__name__)


class Shortener:
    """
    Handles shortening links
    """

    def __init__(self, request: LambdaRequest) -> None:
        req_type = str(request.headers.get("content-type", str()))
        if "application/json" not in req_type:
            LOGGER.warning(f"Invalid content-type: {req_type}")
            raise BadRequest()

        try:
            body = loads(str(request.body))
        except JSONDecodeError as err:
            LOGGER.warning(f"Invalid JSON body: {err}")
            raise BadRequest() from err
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

        if not validators.url(self.target):
            LOGGER.warning(f"Invalid target: {self.target}")
            raise BadRequest()

        if not SafeSite.is_safe_site(self.target):
            LOGGER.warning(f"Unsafe target: {self.target}")
            raise BadRequest()

        target_id = self._generate_id()
        new_link = Link(id=target_id, target=self.target)
        new_link.save(condition=Link.id.does_not_exist())
        return new_link
