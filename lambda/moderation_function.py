import json
import boto3
from system_string import moderation_sys_string
from prompt import moderation_prompt
from llm_tools import tool_list

bedrock_client = boto3.client('bedrock-runtime', region_name="eu-west-1")

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

    model_id = body['model_id']
    
    retry = 0 # Number of current retries
    max_retries = 5 # Maximum number of retries

    format_prompt = moderation_prompt.format(message=message)

    # Prepare Claude-specific request payload (Anthropic format)
    messages = [{
        "role": "user",
        "content": [
            {"text": moderation_sys_string},
            {"text": f"<instructions>\n{format_prompt}\n</instructions>\n"},
        ],
    }]

    # Retry the moderation check if the service is unavailable
    while retry < max_retries:

        try:
            # Call the Bedrock service to check the message for moderation
            response = bedrock_client.converse(
                modelId=model_id,
                messages=messages,
                inferenceConfig={
                    "maxTokens": 1000,
                    "temperature": 0.3,
                },
                toolConfig={
                    "tools": tool_list,
                    "toolChoice": {"tool": {"name": "chat_moderation"}},
                }
            )

                        # Read the response stream and get the tool output
            response_message = response["output"]["message"]
            response_content_blocks = response_message["content"]
            content_block = next(
                (block for block in response_content_blocks if "toolUse" in block), None
            )
            tool_use_block = content_block["toolUse"]
            tool_result_dict = tool_use_block["input"]

            validate_moderation_response(tool_result_dict)
            
            # Return the moderation result
            return {
                'statusCode': 200,
                'headers': {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
                'body': json.dumps(tool_result_dict)
            }
        except Exception as e:
            print(e)
            retry += 1
            continue
    
    raise Exception("Moderation service is unavailable. Please try again later.")

