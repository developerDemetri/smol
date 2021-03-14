from aws_cdk.core import App

from smol_cdk.stack import SmolCdkStack


app = App()
SmolCdkStack(app, "SmolCdkStack")
app.synth()
