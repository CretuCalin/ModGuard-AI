chat-app/cdk/chat_app_stack.py

from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_iam as iam,
)
from constructs import Construct

class ChatAppStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create S3 bucket for hosting frontend
        bucket = s3.Bucket(self, "ChatAppBucket",
                           website_index_document="index.html",
                           public_read_access=True)

        # Create Lambda function for moderation
        moderation_function = _lambda.Function(self, "ModerationFunction",
                                               runtime=_lambda.Runtime.PYTHON_3_8,
                                               handler="moderation_function.lambda_handler",
                                               code=_lambda.Code.from_asset("../lambda"),
                                               environment={
                                                   "BUCKET_NAME": bucket.bucket_name
                                               })

        # Grant necessary permissions to Lambda function
        bucket.grant_read_write(moderation_function)
        moderation_function.add_to_role_policy(iam.PolicyStatement(
            actions=["bedrock:InvokeModel"],
            resources=["*"]
        ))

        # Create API Gateway to route requests to Lambda function
        api = apigateway.RestApi(self, "ChatAppApi",
                                 rest_api_name="ChatApp Service")

        moderation_integration = apigateway.LambdaIntegration(moderation_function)
        api.root.add_method("POST", moderation_integration)