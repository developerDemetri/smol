"""
    smol specific exceptions
"""

from http import HTTPStatus
from json import dumps

from smol.types import AlbResponse


class SmolError(Exception):
    """
    Base smol error
    """

    error_status = HTTPStatus.INTERNAL_SERVER_ERROR
    error_message = "Something broke :/"

    @classmethod
    def response(cls) -> AlbResponse:
        """
        Generates ALB Response for smol error
        """
        return AlbResponse(
            statusCode=cls.error_status.value,
            statusDescription=cls.error_status.phrase,
            isBase64Encoded=False,
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
