# Chat App CDK Deployment

This README provides instructions on how to set up and deploy the Chat App using AWS CDK.

## Prerequisites

- AWS CLI installed and configured
- AWS CDK installed
- Python 3.7 or later
- Node.js and npm (for frontend build)

## Setup

1. **Install AWS CDK**:
   ```
   npm install -g aws-cdk
   ```

2. **Navigate to the `cdk` directory**:
   ```
   cd chat-app/cdk
   ```

3. **Create a virtual environment**:
   ```
   python3 -m venv .env
   source .env/bin/activate
   ```

4. **Install Python dependencies**:
   ```
   pip install -r requirements.txt
   ```

5. **Bootstrap the CDK environment**:
   ```
   cdk bootstrap
   ```

## Deploy

1. **Deploy the CDK stack**:
   ```
   cdk deploy
   ```

   This command will deploy the stack and output the S3 bucket URL for the frontend.

## Cleanup

To delete the stack and all associated resources, run:
```
cdk destroy
```

## Notes

- Ensure your AWS credentials are properly configured.
- The deployment process will create an S3 bucket, Lambda function, and API Gateway.
- The frontend files will be uploaded to the S3 bucket and hosted publicly.

For any issues or questions, refer to the AWS CDK documentation or seek support from the community.