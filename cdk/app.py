import aws_cdk as cdk
from chat_app_stack import ModGuardStack

app = cdk.App()
ModGuardStack(app, "ModGuardStack")

app.synth()