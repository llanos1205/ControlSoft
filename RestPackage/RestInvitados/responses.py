import json


def responseAgw(statusCode, body, hdrs: dict = {"Content-Type": "application/json"}):
    return {
        'statusCode': statusCode,
        'body': json.dumps(body),
        'headers': hdrs
    }


def getBody(event):
    if 'body' in event.keys():
        if type(event['body']) is str:
            return json.loads(event['body'])
        else:
            return event['body']
    else:
        return None
