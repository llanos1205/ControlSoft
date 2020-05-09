import json


def Response(statusCode, body, hdrs: dict = {"Content-Type": "application/json"}):
    return {
        'statusCode': statusCode,
        'body': json.dumps(body),
        'headers': hdrs
    }


def getBody(event):
    if type(event['body']) is str:
        return json.loads(event['body'])
    else:
        return event['body']
