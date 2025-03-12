import aws_cdk as cdk
from chat_app_stack_backend import ModGuardStackBackend
from chat_app_stack_website import ModGuardStackWebsite

app = cdk.App()

backend_stack = ModGuardStackBackend(app, "ModGuardStackBackend")
website_stack = ModGuardStackWebsite(app, "ModGuardStackWebsite")


app.synth()