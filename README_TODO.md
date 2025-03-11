# ModGuard-AI for Agentic Content Moderation

## Table of Contents
- [Overview](#overview)
- [LLM task definition](#llm-tasks-definition)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Deployment](#deployment)
- [Usage](#usage)
- [Security Considerations](#security-considerations)
- [Cost Optimization](#cost-optimization)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

This project demonstrates a serverless application designed as a chat moderation tool for a children's platform, utilizing a Large Language Model (LLM) via AWS Bedrock. The application consists of a backend service and a frontend user interface. The backend processes chat messages, leverages AWS Bedrock to analyze the content through an LLM, and flags messages based on specific moderation categories. The frontend provides an intuitive interface for monitoring and managing flagged messages.

---

## LLM tasks definition

The Large Language Model (LLM) is responsible for analyzing chat messages and flagging them into specific moderation categories. When a user wants to send a message in the chat, the LLM processes the message and attempts to identify if it falls into categories such as Cyberbullying Prevention, Age-Inappropriate Content, Personal Information Protection, Stranger Danger and Grooming Detection, Language Filtering and Profanity Control, and Encouraging Negative Communication.

---

## Architecture

TODO
The application follows a fully serverless architecture leveraging various AWS services to ensure scalability, availability, and cost-efficiency.

- **AWS Lambda:** Powers the backend logic, processes API requests, and interacts with AWS Bedrock for LLM functionality.
- **Amazon API Gateway:** Exposes a secure REST API endpoint for the frontend to communicate with the backend.
- **AWS Bedrock:** Provides access to pre-trained Large Language Models (LLMs) to perform specific NLP tasks.
- **Amazon S3:** Used to host static assets for the frontend.
- **Amazon CloudFront:** Distributes the frontend UI globally with low latency.

---

## Technologies Used

TODO
- **AWS Bedrock** for Large Language Model interactions.
- **AWS Lambda** for serverless computing.
- **Amazon API Gateway** to handle HTTP requests.
- **Amazon S3** for frontend hosting.
- **Amazon CloudFront** for global content delivery.
- **HTML/CSS/JavaScript** for the frontend interface.

---

## Features

TODO
- **LLM Integration:** Backend service communicates with an LLM on AWS Bedrock to perform [define your task, e.g., sentiment analysis, text generation].
- **Serverless Architecture:** Fully scalable and cost-effective backend using AWS Lambda.
- **Simple UI:** Intuitive frontend interface for users to interact with the model.
- **Security:** Incorporates best practices such as authentication and API protection.

---

## Prerequisites

Before setting up this application, ensure you have the following:

- Linux based system
- AWS account with access to AWS Bedrock and required services.
- Conda installed
- Node.js installed
  
---

## Installation and Deployment

1. Clone the repository:

    ```bash
    git clone https://github.com/CretuCalin/ModGuard-AI
    cd ModGuard-AI
    ```

2. Create and activate the conda environment:

    ```bash
    conda env create -f environment.yaml
    conda activate modguard
    ```

3. Configure AWS CLI with your credentials:

    ```bash
    aws configure
    ```

4. Bootstrap the AWS CDK stack:

    ```bash
    cd cdk
    cdk bootstrap
    ```

4. Deploy the AWS CDK stack:

    ```bash
    cdk deploy
    ```

---

## Deployment

### Backend

1. **Deploy Lambda Functions & API Gateway:**
   - Use AWS SAM or Serverless Framework to deploy the Lambda function.
   - Example using Serverless Framework:

    ```bash
    sls deploy
    ```

2. **Configure API Gateway:**
   - Ensure the API Gateway is connected to the Lambda functions and integrated with AWS Bedrock.

### Frontend

1. **Deploy Frontend:**
   - Upload the frontend assets to an Amazon S3 bucket.

    ```bash
    aws s3 sync ./frontend s3://<your-s3-bucket-name> --acl public-read
    ```

2. **Set Up CloudFront Distribution:**
   - Create a CloudFront distribution to serve the static assets globally.

---

## Usage

1. Access the frontend by navigating to the CloudFront distribution URL.
2. Enter your input in the provided field and submit the request.
3. The backend will process the request via the API Gateway and AWS Bedrock, and the response will be displayed on the frontend.

---

## Security Considerations

- **Authentication & Authorization:** Ensure that your API Gateway is secured using AWS Cognito or API keys.
- **IAM Roles:** Use the principle of least privilege for all IAM roles associated with AWS services.
- **API Rate Limiting:** Implement API rate limiting to prevent misuse or DDoS attacks.

---

## Cost Optimization

- **Lambda Function Timeout:** Set appropriate timeouts for your Lambda functions to avoid unnecessary costs.
- **API Gateway Caching:** Enable caching to reduce the number of requests made to the Lambda function.
- **S3 & CloudFront:** Use Amazon S3 Intelligent-Tiering for the frontend storage and ensure CloudFront distribution is optimized.

---

## Troubleshooting

- **Lambda Timeout Errors:** Ensure that the Lambda timeout setting is adequate for the model's response time.
- **API Gateway Configuration:** Double-check API Gateway integration with Lambda and Bedrock to ensure proper routing of requests.
- **CORS Issues:** If you encounter CORS errors, make sure CORS is enabled in the API Gateway settings.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
