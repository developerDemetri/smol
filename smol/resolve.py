from logging import getLogger

from smol.exceptions import BadMethod, BadRequest, LinkNotFound
from smol.link import ID_REGEX, Link
from smol.alb_types import AlbEvent

LOGGER = getLogger(__name__)


class Resolver:
    """
    Handles Link resolution
    """

    def __init__(self, request: AlbEvent) -> None:
        req_method = request["httpMethod"].upper()
        if req_method != "GET":
            LOGGER.warning(f"Invalid method: {req_method}")
            raise BadMethod()

        link_path = str(request["path"]).strip()
        self.link_id = link_path.strip("/").upper()

    def resolve_link(self) -> Link:
        """
        Resolve Link from given event
        """
        if ID_REGEX.fullmatch(self.link_id) is None:
            LOGGER.warning(f"Invalid Link: {self.link_id}")
            raise BadRequest()

        try:
            target_link = Link.get(self.link_id)
        except Link.DoesNotExist as err:
            LOGGER.warning(f"Non Existent link ID: {self.link_id}")
            raise LinkNotFound() from err

        return target_link
