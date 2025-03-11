import json
import boto3

def lambda_handler(event, context):
    # Extract the message from the event
    # body = event['body']
    # print(body)

    # if type(body) == str:
    #     body = json.loads(body)
    # message = body['message']
    # print(message)
    
    # # Initialize the Bedrock client
    # bedrock_client = boto3.client('bedrock')
    
    # # Call the Bedrock service to check the message for moderation
    # response = bedrock_client.check_message(
    #     Text=message
    # )
    
    # # Extract the moderation result
    # moderation_result = response['ModerationResult']
    
    # Return the moderation result
    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        'body': json.dumps({
            'cyberbullying': True,
            'ageAppropriate': False,
            'personalInfo': True,
            'strangerDanger': False,
            'languageFilter': True,
            'positiveCommunication': False,
        })
    }