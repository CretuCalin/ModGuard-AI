from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_iam as iam,
    aws_cognito as cognito,
    RemovalPolicy,
    Duration,
)
import aws_cdk
from constructs import Construct

class ModGuardStackBackend(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create S3 bucket for hosting frontend
        bucket = s3.Bucket(self, "ModGuardBucket",
                           versioned=True,
                           # This is useful for development and testing environments but should be used with caution in production.
                           removal_policy=RemovalPolicy.DESTROY,
                           website_index_document="index.html",
                           block_public_access=s3.BlockPublicAccess.BLOCK_ACLS,
                           public_read_access=True)

        # Create Lambda function for moderation
        moderation_function = _lambda.Function(self, "ModerationFunction",
                                               runtime=_lambda.Runtime.PYTHON_3_8,
                                               handler="moderation_function.lambda_handler",
                                               code=_lambda.Code.from_asset("../lambda"),
                                               timeout=Duration.minutes(3),
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
        api = apigateway.RestApi(self, "ModGuardApi",
                                 rest_api_name="ModGuard Service")
    
        # Create a Cognito User Pool
        user_pool = cognito.UserPool(
            self, "UserPool",
            user_pool_name="MogGuardUserPool",
            sign_in_aliases=cognito.SignInAliases(email=True),  # Allow email sign-in
            self_sign_up_enabled=True,  # Allow users to sign up on their own
            auto_verify=cognito.AutoVerifiedAttrs(email=True),  # Automatically verify emails
            standard_attributes={
                "email": cognito.StandardAttribute(
                    required=True,
                    mutable=False
                )
            },
            password_policy=cognito.PasswordPolicy(
                min_length=6,
                require_lowercase=False,
                require_uppercase=False,
                require_digits=False,
                require_symbols=False
            ),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
        )

        # Create a User Pool Client (used by apps to interact with Cognito)
        user_pool_client = cognito.UserPoolClient(
            self, "UserPoolClient",
            user_pool=user_pool,
            generate_secret=False,  # Don't require a client secret (if using public clients like web apps)
            auth_flows=cognito.AuthFlow(
                user_password=True,  # Enable username & password authentication
                user_srp=True,        # Enable SRP (Secure Remote Password) authentication flow
            )
        )

        # Create Cognito Authorizer
        cognito_authorizer = apigateway.CognitoUserPoolsAuthorizer(
            self, "ModGuardCognitoAuthorizer",
            cognito_user_pools=[user_pool]
        )
        
        moderation_resource = api.root.add_resource("moderation")

        moderation_integration = apigateway.LambdaIntegration(moderation_function,
                                                              proxy=True,
                                                                integration_responses=[
                                                                    apigateway.IntegrationResponse(
                                                                        status_code="200",
                                                                        response_parameters={
                                                                            "method.response.header.Access-Control-Allow-Origin": "'*'",
                                                                            "method.response.header.Access-Control-Allow-Headers": "'Content-Type,Autorization'",
                                                                            "method.response.header.Access-Control-Allow-Methods": "'POST'"
                                                                        }
                                                                    )])
        method_responses=[
                apigateway.MethodResponse(
                    status_code="200",
                    response_parameters={
                        "method.response.header.Access-Control-Allow-Origin": True,
                        "method.response.header.Access-Control-Allow-Headers": True,
                        "method.response.header.Access-Control-Allow-Methods": True
                    }
                )
            ]
        moderation_resource.add_method("POST", moderation_integration, 
                                       method_responses=method_responses, 
                                       authorization_type=apigateway.AuthorizationType.COGNITO,
                                       authorizer=cognito_authorizer)
        moderation_resource.add_method("OPTIONS", 
                apigateway.MockIntegration(
                integration_responses=[apigateway.IntegrationResponse(
                    status_code="200",
                    response_parameters={
                        "method.response.header.Access-Control-Allow-Headers": "'Content-Type,Authorization'",
                        "method.response.header.Access-Control-Allow-Origin": "'*'",
                        "method.response.header.Access-Control-Allow-Methods": "'OPTIONS,POST'"
                    }
                )],
                passthrough_behavior=apigateway.PassthroughBehavior.NEVER,
                request_templates={
                    "application/json": "{\"statusCode\": 200}"
                }
            ),
            method_responses=method_responses
        )

        # Output API Gateway URL for the Lambda function
        aws_cdk.CfnOutput(self, "BedrockApi", value=api.url)
        aws_cdk.CfnOutput(self, "userPoolId", value=user_pool.user_pool_id)
        aws_cdk.CfnOutput(self, "userPoolClientId", value=user_pool_client.user_pool_client_id)