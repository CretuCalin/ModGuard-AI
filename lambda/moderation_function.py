import json
import boto3

def lambda_handler(event, context):
    # Extract the message from the event
    message = event['body']['message']
    
    # Initialize the Bedrock client
    bedrock_client = boto3.client('bedrock')
    
    # Call the Bedrock service to check the message for moderation
    response = bedrock_client.check_message(
        Text=message
    )
    
    # Extract the moderation result
    moderation_result = response['ModerationResult']
    
    # Return the moderation result
    return {
        'statusCode': 200,
        'body': json.dumps({
            'moderation_result': moderation_result
        })
    }