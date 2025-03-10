# Chat App with AI Content Moderation

## Project Structure

chat-app
├── cdk
│   ├── app.py
│   ├── chat_app_stack.py
│   ├── requirements.txt
│   └── README.md
├── lambda
│   ├── moderation_function.py
│   └── requirements.txt
├── frontend
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── README.md

## Prerequisites

- AWS CLI configured with appropriate permissions
- AWS CDK installed
- Python 3.8 or later
- Node.js and npm

## Setup Instructions

### 1. Clone the Repository

Clone the repository to your local machine:

git clone <repository-url>
cd chat-app

### 2. Set Up the CDK Application

Navigate to the `cdk` directory and install the required dependencies:

cd cdk
pip install -r requirements.txt

### 3. Deploy the CDK Stack

Deploy the CDK stack to your AWS account:

cdk bootstrap
cdk deploy

### 4. Set Up the Lambda Function

Navigate to the `lambda` directory and install the required dependencies:

cd ../lambda
pip install -r requirements.txt -t .

### 5. Upload the Frontend to S3

Navigate to the `frontend` directory and upload the contents to the S3 bucket created by the CDK stack:

cd ../frontend
aws s3 sync . s3://<your-s3-bucket-name>

### 6. Access the Application

Access the application via the public URL provided by the S3 bucket.

## Usage

1. Open the chat interface in your browser.
2. Send a message using the chat form.
3. The message will be sent to the backend Lambda function for moderation.
4. The moderated message will be displayed in the chat interface.

## Cleanup

To delete the resources created by the CDK stack, run:

cd ../cdk
cdk destroy

## License

This project is licensed under the MIT License.