# Chat App with AI Content Moderation

## Prerequisites
- AWS CLI configured
- Node.js installed
- Conda installed

## Setup

1. **Create Conda Environment**:
    - Create a new Conda environment:
        ```sh
        conda create -n modguard python=3.8
        ```
    - Activate the environment:
        ```sh
        conda activate modguard
        ```

2. **Install AWS CDK**:
    - Install AWS CDK using npm:
        ```sh
        sudo npm install -g aws-cdk
        ```

3. **CDK Deployment**:
    - Navigate to the `cdk` directory:
        ```sh
        cd cdk
        ```
    - Install required Python packages:
        ```sh
        pip install -r requirements.txt
        ```
    - Bootstrap the CDK environment:
        ```sh
        cdk bootstrap
        ```
    - Deploy the stack:
        ```sh
        cdk deploy
        ```

4. **Lambda Function**:
    - Navigate to the `lambda` directory:
        ```sh
        cd lambda
        ```
    - Install required packages:
        ```sh
        pip install -r requirements.txt -t .
        ```
    - Zip the contents and upload to the Lambda function created by CDK.

5. **Frontend**:
    - Navigate to the `frontend` directory:
        ```sh
        cd frontend
        ```
    - Upload the contents to the S3 bucket created by CDK.

## Usage
- Access the chat interface via the public URL provided by the S3 bucket.
- Messages sent in the chat will be moderated by the AI model before being displayed.