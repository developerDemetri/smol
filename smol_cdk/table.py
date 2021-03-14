from aws_cdk.core import Construct
from aws_cdk.aws_dynamodb import Attribute, AttributeType, BillingMode, Table


class SmolTable(Construct):
    """
    DynamoDB Table for storing Links
    """

    def __init__(self, scope: Construct, id: str, table_name: str) -> None:
        super().__init__(scope, id)
        primary_key = Attribute(name="id", type=AttributeType.STRING)
        self.table = Table(
            self,
            "SmolTable",
            billing_mode=BillingMode.PAY_PER_REQUEST,
            partition_key=primary_key,
            point_in_time_recovery=True,
            table_name=table_name,
        )
