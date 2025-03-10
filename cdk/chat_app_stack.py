from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_iam as iam,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_s3_deployment as s3_deployment,
    RemovalPolicy,
)
from constructs import Construct

class ModGuardStack(Stack):

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

        moderation_integration = apigateway.LambdaIntegration(moderation_function)
        api.root.add_method("POST", moderation_integration)

        # Create a CloudFront distribution
        distribution = cloudfront.Distribution(self, "CloudFrontDistribution",
                                               default_behavior={
                                                   "origin": origins.S3Origin(bucket),
                                                   "viewer_protocol_policy": cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
                                               },
                                               default_root_object="index.html")
        
            # Upload frontend files to the S3 bucket
        s3_deployment.BucketDeployment(self, "DeployFrontend",
                                                sources=[s3_deployment.Source.asset("../frontend")],
                                                destination_bucket=bucket,
                                                distribution=distribution,
                                                distribution_paths=["/*"])
