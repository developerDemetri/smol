"""
Type definitions used by smol
"""

from typing import Optional
from pydantic import BaseModel


class LambdaRequest(BaseModel):
    headers: dict[str, str]
    method: str
    path: str
    body: Optional[str]


class LambdaResponse(BaseModel):
    """
    HTTP Response Payload
    """

    statusCode: int
    statusDescription: str
    headers: dict[str, str]
    body: str
