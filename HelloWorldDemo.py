import json

def lambda_handler(event, context):
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello World!",
            "request_id": context.aws_request_id 
        })
    }