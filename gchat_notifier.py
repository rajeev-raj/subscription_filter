import json
import boto3
import requests

def lambda_handler(event, context):
    # Get the log message from the event
    log_message = event['awslogs']['data']
    # Decode the log message
    log_message = json.loads(json.loads(log_message)['logEvents'][0]['message'])
    
    # Extract relevant information from the log message
    log_group_name = event['awslogs']['logGroup']
    log_stream_name = event['awslogs']['logStream']
    log_message_text = log_message['message']
    log_timestamp = log_message['timestamp']
    
    # Compose the message to be sent to Google Chat
    message = f"CloudWatch log message:\nLog group name: {log_group_name}\nLog stream name: {log_stream_name}\nLog message: {log_message_text}\nLog timestamp: {log_timestamp}"
    
    # Set up the Google Chat webhook URL
    webhook_url = '<YOUR_GOOGLE_CHAT_WEBHOOK_URL>'
    
    # Set up the Google Chat message payload
    payload = {
        'text': message
    }
    
    # Send the message to Google Chat
    response = requests.post(webhook_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    
    # Check if the message was successfully sent
    if response.status_code != 200:
        raise ValueError(f"Request to Google Chat webhook returned an error {response.status_code}, {response.text}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Message sent to Google Chat successfully!')
    }
