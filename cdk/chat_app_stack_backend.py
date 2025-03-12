from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_iam as iam,
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
        
        moderation_resource = api.root.add_resource("moderation")

        moderation_integration = apigateway.LambdaIntegration(moderation_function,
                                                              proxy=True,
                                                                integration_responses=[
                                                                    apigateway.IntegrationResponse(
                                                                        status_code="200",
                                                                        response_parameters={
                                                                            "method.response.header.Access-Control-Allow-Origin": "'*'",
                                                                            "method.response.header.Access-Control-Allow-Headers": "'Content-Type'",
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
        moderation_resource.add_method("POST", moderation_integration, method_responses=method_responses)
        moderation_resource.add_method("OPTIONS", 
                apigateway.MockIntegration(
                integration_responses=[apigateway.IntegrationResponse(
                    status_code="200",
                    response_parameters={
                        "method.response.header.Access-Control-Allow-Headers": "'Content-Type'",
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

        # # Create a CloudFront distribution
        # distribution = cloudfront.Distribution(self, "CloudFrontDistribution",
        #                                        default_behavior={
        #                                            "origin": origins.S3StaticWebsiteOrigin(bucket),
        #                                            "viewer_protocol_policy": cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        #                                            "allowed_methods": cloudfront.AllowedMethods.ALLOW_ALL,
        #                                            "cache_policy": cloudfront.CachePolicy.CACHING_DISABLED,
        #                                            "response_headers_policy": cloudfront.ResponseHeadersPolicy.CORS_ALLOW_ALL_ORIGINS
        #                                        },
        #                                        default_root_object="index.html")
        
        # # Upload frontend files to the S3 bucket
        # s3_deployment.BucketDeployment(self, "DeployFrontend",
        #                                sources=[s3_deployment.Source.asset("../frontend")],
        #                                destination_bucket=bucket,
        #                                distribution=distribution,
        #                                distribution_paths=["/*"])
        

        # Output API Gateway URL for the Lambda function
        aws_cdk.CfnOutput(self, "BedrockApi", value=api.url)