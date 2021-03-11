"""
    Type definitions used by smol
"""

from typing import Dict, TypedDict


class AlbContext(TypedDict):
    """
    ALB Request Context
    """

    elb: Dict[str, str]


class AlbEvent(TypedDict):
    """
    ALB Request Payload
    """

    requestContext: AlbContext
    httpMethod: str
    path: str
    queryStringParameters: Dict[str, str]
    headers: Dict[str, str]
    body: str
    isBase64Encoded: bool


class AlbResponse(TypedDict):
    """
    ALB Response Payload
    """

    statusCode: int
    statusDescription: str
    isBase64Encoded: bool
    headers: Dict[str, str]
    body: str
