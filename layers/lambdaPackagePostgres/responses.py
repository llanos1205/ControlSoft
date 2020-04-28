import json
def Response(StatusCode,Body,hdrs:dict={ "Content-Type": "application/json"}):
    return{
        'statusCode':StatusCode,
        'body':json.dumps(Body),
        'headers':hdrs
    }