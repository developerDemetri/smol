from logging import getLogger
from os import environ
from re import compile
from string import ascii_uppercase, digits

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

DYNAMO_REGION = environ.get("AWS_REGION", "eu-west-1")
DYNAMO_TABLE = environ.get("TABLE_NAME", "smol")
ID_LENGTH = 6
ID_CHARS = f"{ascii_uppercase}{digits}"
ID_REGEX = compile(r"^[a-zA-z0-9]{6}$")

LOGGER = getLogger(__name__)


class Link(Model):
    """
    DynamoDB model for a Link
    """

    class Meta:
        """
        DynamoDB config
        """

        region = DYNAMO_REGION
        table_name = DYNAMO_TABLE

    id = UnicodeAttribute(hash_key=True)
    target = UnicodeAttribute(null=False)
