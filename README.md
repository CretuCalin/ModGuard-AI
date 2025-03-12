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

The Large Language Model (LLM) is responsible for analyzing chat messages and flagging them into specific moderation categories. When a user wants to send a message in the chat, the LLM processes the message and attempts to identify if it falls into the categories:
- Cyberbullying Prevention
- Age-Inappropriate Content
- Personal Information Protection
- Stranger Danger and Grooming Detection
- Language Filtering and Profanity Control
- Encouraging Negative Communication.

---

## Architecture

![AWS architecture](assets/aws_architecture.png)

This application is a serverless chat interface that performs message moderation using Large Language Models (LLMs). It leverages AWS services for scalability, security, and real-time processing.

1. **Frontend**:
   - **Frontend/Website**: The frontend is a simple web application that allows users to interact with the chat interface.
   - **S3 Bucket**: The S3 bucket stores static website assets (HTML, CSS, JS).
   - **CloudFront**: CloudFront caches and delivers the frontend assets to users worldwide, ensuring low latency and high performance.

2. **Authorization**:
   - **Cognito**: AWS Cognito manages user authentication and authorization, ensuring that only authorized users can access the chat application.

3. **Backend**:
   - **API Gateway**: The frontend communicates with the backend through API Gateway, which exposes RESTful endpoints for interaction with the system.
   - **Lambda Function**: API Gateway invokes Lambda functions to handle requests. The Lambda function processes chat messages and forwards them for moderation.
   - **Bedrock**: Amazon Bedrock, integrated with LLMs, performs message moderation by analyzing and processing the content.
   - **LLM**: The LLM (Large Language Model) returns a moderated response, ensuring compliance with predefined content policies.

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

## Installation

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

---

## Deployment

1. Deploy the backend stack:

    ```bash
    cd cdk
    cdk deploy ModGuardStackBackend
    ```

2. Copy the `ModGuardStackBackend.BedrockApi` variable from the ModGuardStackBackend stack output:
        
    ```sh
    # cdk deploy ModGuardStackBackend
    ModGuardStackBackend.BedrockApi = https://<some_id>.execute-api.eu-west-1.amazonaws.com/prod/
    ```

3. Paste the value in the `frontend/app.js` file:
        ```js
        // /frontend/app.js
        const ApiUrl = "https://<some_id>.execute-api.eu-west-1.amazonaws.com/prod/";
        ```

4. Deploy the website stack:
        ```sh
        cdk deploy ModGuardStackWebsite
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
