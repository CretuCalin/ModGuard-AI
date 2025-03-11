import os
import aws_cdk as cdk
from chat_app_stack import ModGuardStack

app = cdk.App()

# Specify the AWS account and region
env = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))

ModGuardStack(app, "ModGuardStack", env=env)

app.synth()