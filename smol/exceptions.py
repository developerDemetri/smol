"""
smol specific exceptions
"""

from http import HTTPStatus
from json import dumps
from os import environ

from smol.models import LambdaResponse

LOST_PAGE = environ.get("LOST_PAGE", "https://smol.io/?im=lost")


class SmolError(Exception):
    """
    Base smol error
    """

    error_status = HTTPStatus.INTERNAL_SERVER_ERROR
    error_message = "Something broke :/"

    @classmethod
    def response(cls) -> LambdaResponse:
        """
        Generates HTTP Response for smol error
        """
        return LambdaResponse(
            statusCode=cls.error_status.value,
            statusDescription=f"{cls.error_status.value} {cls.error_status.phrase}",
            headers=dict(),
            body=dumps({"message": cls.error_message}),
        )


class BadMethod(SmolError):
    """
    Invalid API method called
    """

    error_status = HTTPStatus.METHOD_NOT_ALLOWED
    error_message = "Invalid HTTP Method"


class BadRequest(SmolError):
    """
    Invalid API request
    """

    error_status = HTTPStatus.BAD_REQUEST
    error_message = "Invalid Request"


class LinkNotFound(SmolError):
    """
    Requested Link does not exist
    """

    error_status = HTTPStatus.NOT_FOUND
    error_message = "Link Not Found"

    @classmethod
    def response(cls) -> LambdaResponse:
        """
        Redirect missing Links to lost page
        """
        status = HTTPStatus.MOVED_PERMANENTLY
        return LambdaResponse(
            statusCode=status.value,
            statusDescription=f"{status.value} {status.phrase}",
            headers={"location": LOST_PAGE},
            body=dumps({"message": cls.error_message}),
        )
