import json
def Response(StatusCode,Body,hdrs):
    return{
        'statusCode':StatusCode,
        'headers':hdrs,
        'body':json.dumps(Body)
    }