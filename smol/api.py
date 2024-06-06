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

from smol.models import LambdaRequest, LambdaResponse
from smol.exceptions import BadMethod, BadRequest, LinkNotFound, SmolError
from smol.resolve import Resolver
from smol.shorten import Shortener

EMPTY_BODY = dumps(dict())
STANDARD_HEADERS = {
    "access-control-allow-origin": "https://smol.io",
    "access-control-allow-methods": "POST, GET, OPTIONS",
    "content-type": "application/json",
    "strict-transport-security": "max-age=31536000; includeSubDomains; preload",
    "x-xss-protection": "1; mode=block",
}

ecs_handler = StreamHandler(stdout)
ecs_handler.setFormatter(StdlibFormatter())
basicConfig(level=INFO, handlers=[ecs_handler], force=True)
LOGGER = getLogger(__name__)


def process_request(req: LambdaRequest) -> LambdaResponse:
    """
    Route a well-formed request
    """
    if req.path == "/api/v1/link":
        if req.method == "OPTIONS":
            LOGGER.info("Handling OPTIONS check...")
            status = HTTPStatus.OK
            return LambdaResponse(
                statusCode=status.value,
                statusDescription=f"{status.value} {status.phrase}",
                headers=dict(),
                body=EMPTY_BODY,
            )
        elif req.method == "POST":
            LOGGER.info("Handling shortener request...")
            new_link = Shortener(req).shorten_link()
            status = HTTPStatus.CREATED
            return LambdaResponse(
                statusCode=status.value,
                statusDescription=f"{status.value} {status.phrase}",
                headers=dict(),
                body=dumps({"id": new_link.id, "target": new_link.target}),
            )
        else:
            LOGGER.warning(f"Invalid method: {req.method}")
            raise BadMethod()
    elif req.method == "GET":
        LOGGER.info("Handling resolver request...")
        resolved_link = Resolver(req).resolve_link()
        status = HTTPStatus.MOVED_PERMANENTLY
        return LambdaResponse(
            statusCode=status.value,
            statusDescription=f"{status.value} {status.phrase}",
            headers={"location": resolved_link.target},
            body=EMPTY_BODY,
        )
    else:
        raise LinkNotFound()


def http_handler(event: dict, _: Any) -> dict:
    """
    Lambda HTTP entrypoint
    """
    resp = LambdaResponse(
        statusCode=HTTPStatus.NOT_FOUND.value,
        statusDescription=f"{HTTPStatus.NOT_FOUND.value} {HTTPStatus.NOT_FOUND.phrase}",
        headers=dict(),
        body=EMPTY_BODY,
    )
    try:
        req: LambdaRequest
        try:
            LOGGER.info(event)
            req = LambdaRequest(
                headers=event.get("headers", {}),
                method=event["requestContext"]["http"]["method"].upper(),
                path=event["requestContext"]["http"]["path"].lower(),
                body=event.get("body", None),
            )
        except Exception as err:
            LOGGER.warning(f"Bad request object: {err}")
            raise BadRequest()

        resp = process_request(req)
    except SmolError as smol_err:
        LOGGER.warning(f"Caught smol error: {smol_err.error_message}")
        resp = smol_err.response()
    except Exception as err:
        LOGGER.exception(f"Unexpected error: {err}")
        resp = SmolError.response()
    finally:
        resp.headers.update(STANDARD_HEADERS)
        return resp.model_dump(mode="json")
