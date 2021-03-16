from os.path import abspath
from os import environ

from aws_cdk.core import Construct, Duration, Environment, Stack
from aws_cdk.aws_ec2 import SubnetSelection, SubnetType, Vpc
from aws_cdk.aws_lambda import Code, Function, Handler, Runtime
from aws_cdk.aws_logs import RetentionDays

from smol_cdk.table import SmolTable
from smol_cdk.target import SmolTarget

API_HOST = environ.get("FUNCTION_NAME", "api.smol.io")
FUNCTION_NAME = environ.get("FUNCTION_NAME", "SmolAPI")
MEMORY_ALLOCATION = int(environ.get("MEMORY_ALLOCATION", "256"))
RESERVED_CONCURRENCY = int(environ.get("RESERVED_CONCURRENCY", "100"))
TABLE_NAME = environ.get("TABLE_NAME", "smol")
TIMEOUT_SEC = float(environ.get("TIMEOUT_SEC", "3.0"))
VPC_NAME = environ.get("VPC_NAME", "core")


class SmolCdkStack(Stack):
    """
    Top level CFN Stack for smol
    """

    def __init__(self, scope: Construct, construct_id: str, env: Environment) -> None:
        super().__init__(scope, construct_id, env=env)
        smol_table = SmolTable(self, "SmolTable", table_name=TABLE_NAME)
        smol_vpc = Vpc.from_lookup(self, "CoreVPC", vpc_name=VPC_NAME)
        smol_subnets = SubnetSelection(
            one_per_az=True,
            subnet_type=SubnetType.PRIVATE,
        )
        smol_lambda = Function(
            self,
            "SmolAPI",
            code=Code.from_asset_image(directory=abspath("./")),
            function_name=FUNCTION_NAME,
            handler=Handler.FROM_IMAGE,
            log_retention=RetentionDays.ONE_WEEK,
            memory_size=MEMORY_ALLOCATION,
            reserved_concurrent_executions=RESERVED_CONCURRENCY,
            runtime=Runtime.FROM_IMAGE,
            timeout=Duration.seconds(TIMEOUT_SEC),
            vpc=smol_vpc,
            vpc_subnets=smol_subnets,
        )
        smol_table.table.grant(smol_lambda, "dynamodb:DescribeTable")
        smol_table.table.grant(smol_lambda, "dynamodb:GetItem")
        smol_table.table.grant(smol_lambda, "dynamodb:PutItem")
        SmolTarget(self, "SmolTarget", smol_lambda, API_HOST)
