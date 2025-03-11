import json
import boto3
from system_string import moderation_sys_string
from prompt import moderation_prompt

bedrock_client = boto3.client('bedrock-runtime', region_name="eu-west-1")
model_id = "eu.anthropic.claude-3-5-sonnet-20240620-v1:0"

def validate_moderation_response(response):
    if "cyberbullying" not in response:
        raise Exception("Response does not contain cyberbullying field")
    if "notAgeAppropriate" not in response:
        raise Exception("Response does not contain notAgeAppropriate field")
    if "personalInfo" not in response:  
        raise Exception("Response does not contain personalInfo field")
    if "strangerDanger" not in response:    
        raise Exception("Response does not contain strangerDanger field")
    if "languageFilter" not in response:
        raise Exception("Response does not contain languageFilter field")
    if "negativeCommunication" not in response:
        raise Exception("Response does not contain negativeCommunication field")

def lambda_handler(event, context):
    # Extract the message from the event
    body = event['body']
    print(body)

    if type(body) == str:
        body = json.loads(body)
    message = body['message']
    print(message)
    
    retry = 0 # Number of current retries
    max_retries = 3 # Maximum number of retries

    # Retry the moderation check if the service is unavailable
    while retry < max_retries:

        try:
            # Call the Bedrock service to check the message for moderation
            response = bedrock_client.invoke_model(
                modelId=model_id,
                body=json.dumps({
                            "messages": [
                    {
                        "role": "system",
                        "content": [{
                            "type": "text",
                            "text": moderation_sys_string
                        }],
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": moderation_prompt.format(message=message)
                            }
                        ]
                    }
                ],
                "max_tokens": 150,
                "temperature": 0.3,
                "anthropic_version": "bedrock-2023-05-31"
                }),
                accept="application/json",
                contentType="application/json"
            )

            # Read the response stream and decode it
            response_body = json.loads(response['body'].read())

            # Claude models return `completion` in the result
            completion = response_body['content'][0]['text']
            print(completion)

            response_json = json.loads(completion)

            validate_moderation_response(response_json)
            
            # Return the moderation result
            return {
                'statusCode': 200,
                'headers': {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
                'body': json.dumps(response_json)
            }
        except Exception as e:
            print(e)
            retry += 1
            continue
    
    raise Exception("Moderation service is unavailable. Please try again later.")

