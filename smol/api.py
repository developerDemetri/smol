"""
    Main application entrypoint
"""

from http import HTTPStatus
from json import dumps
from logging import INFO
from logging import basicConfig, getLogger, StreamHandler
from typing import Any
from sys import stdout

from ecs_logging import StdlibFormatter

from smol.exceptions import SmolError
from smol.resolve import Resolver
from smol.shorten import Shortener
from smol.types import AlbEvent, AlbResponse

EMPTY_BODY = dumps(dict())
STANDARD_HEADERS = {
    "Access-Control-Allow-Origin": "https://smol.io",
    "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    "Content-Type": "application/json",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
    "X-XSS-Protection": "1; mode=block",
}

ecs_handler = StreamHandler(stdout)
ecs_handler.setFormatter(StdlibFormatter())
basicConfig(level=INFO, handlers=[ecs_handler], force=True)
LOGGER = getLogger(__name__)


def alb_handler(event: AlbEvent, _: Any) -> AlbResponse:
    """
    Lambda entrypoint from ALB
    """
    try:
        if event["path"].lower() == "/api/v1/link":
            if event["httpMethod"].upper() == "OPTIONS":
                resp = AlbResponse(
                    statusCode=HTTPStatus.OK.value,
                    statusDescription=HTTPStatus.OK.phrase,
                    isBase64Encoded=False,
                    headers=dict(),
                    body=EMPTY_BODY,
                )
            else:
                new_link = Shortener(event).shorten_link()
                resp = AlbResponse(
                    statusCode=HTTPStatus.CREATED.value,
                    statusDescription=HTTPStatus.CREATED.phrase,
                    isBase64Encoded=False,
                    headers=dict(),
                    body=dumps({"id": new_link.id, "target": new_link.target}),
                )
        else:
            resolved_link = Resolver(event).resolve_link()
            resp = AlbResponse(
                statusCode=HTTPStatus.MOVED_PERMANENTLY.value,
                statusDescription=HTTPStatus.MOVED_PERMANENTLY.phrase,
                isBase64Encoded=False,
                headers={"Location": resolved_link.target},
                body=EMPTY_BODY,
            )
    except SmolError as smol_err:
        LOGGER.warning(f"Caught smol error: {smol_err.error_message}")
        resp = smol_err.response()
    except Exception as err:  # pylint: disable=W0703
        LOGGER.exception(f"Unexpected error: {err}")
        resp = SmolError.response()
    finally:
        resp["headers"].update(STANDARD_HEADERS)
        return resp  # pylint: disable=W0150
