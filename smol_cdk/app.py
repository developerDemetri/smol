from os import environ

from aws_cdk.core import App, Environment

from smol_cdk.stack import SmolCdkStack


app = App()
SmolCdkStack(
    app,
    "SmolCdkStack",
    env=Environment(
        account=environ["CDK_ACCOUNT"], region=environ.get("CDK_REGION", "us-west-2")
    ),
)
app.synth()
