from aws_cdk import core
from chat_app_stack import ChatAppStack

app = core.App()
ChatAppStack(app, "ChatAppStack")

app.synth()