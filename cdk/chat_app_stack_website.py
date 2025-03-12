from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_s3_deployment as s3_deployment,
    RemovalPolicy,
)
import aws_cdk
from constructs import Construct

class ModGuardStackWebsite(Stack):

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

        # Create a CloudFront distribution
        distribution = cloudfront.Distribution(self, "CloudFrontDistribution",
                                               default_behavior={
                                                   "origin": origins.S3StaticWebsiteOrigin(bucket),
                                                   "viewer_protocol_policy": cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                                                   "allowed_methods": cloudfront.AllowedMethods.ALLOW_ALL,
                                                   "cache_policy": cloudfront.CachePolicy.CACHING_DISABLED,
                                                   "response_headers_policy": cloudfront.ResponseHeadersPolicy.CORS_ALLOW_ALL_ORIGINS
                                               },
                                               default_root_object="index.html")
        
        # Upload frontend files to the S3 bucket
        s3_deployment.BucketDeployment(self, "DeployFrontend",
                                       sources=[s3_deployment.Source.asset("../frontend")],
                                       destination_bucket=bucket,
                                       distribution=distribution,
                                       distribution_paths=["/*"])
        

        # Output CloudFront URL
        aws_cdk.CfnOutput(self, "CloudFrontURL", value=distribution.distribution_domain_name)