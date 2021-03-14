from os.path import abspath
from os import environ

from aws_cdk.core import Construct, Stack
from aws_cdk.aws_lambda import Code, Function, Handler, Runtime
from aws_cdk.aws_logs import RetentionDays

from smol_cdk.table import SmolTable

FUNCTION_NAME = environ.get("FUNCTION_NAME", "SmolAPI")
TABLE_NAME = environ.get("TABLE_NAME", "smol")


class SmolCdkStack(Stack):
    """
    Top level CFN Stack for smol
    """

    def __init__(self, scope: Construct, construct_id: str) -> None:
        super().__init__(scope, construct_id)
        smol_table = SmolTable(self, "SmolTable", table_name=TABLE_NAME)
        smol_lambda = Function(
            self,
            "SmolAPI",
            code=Code.from_asset_image(directory=abspath("./")),
            function_name=FUNCTION_NAME,
            handler=Handler.FROM_IMAGE,
            log_retention=RetentionDays.ONE_WEEK,
            memory_size=256,
            runtime=Runtime.FROM_IMAGE,
        )
        smol_table.table.grant(smol_lambda, "dynamodb:GetItem")
        smol_table.table.grant(smol_lambda, "dynamodb:PutItem")
