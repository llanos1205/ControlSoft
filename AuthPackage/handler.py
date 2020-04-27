import boto3
import Cognito_Config
import responses
import json
import hmac
import hashlib
import base64
import time
client = boto3.client('cognito-idp')
def lambda_handler(event, context):
    # TODO implement
    response=client.admin_initiate_auth(
    UserPoolId=Cognito_Config.Pool_Id,
    ClientId=Cognito_Config.Pool_AppClient_Id,
    AuthFlow='ADMIN_USER_PASSWORD_AUTH',
    AuthParameters={
        'USERNAME': event['USERNAME'],
        'PASSWORD': event['PASSWORD']
       
        }
    )
    if('ChallengeName' in response):
        response2=client.admin_respond_to_auth_challenge(
        UserPoolId=Cognito_Config.Pool_Id,
        ClientId=Cognito_Config.Pool_AppClient_Id,
        ChallengeName='NEW_PASSWORD_REQUIRED',
        ChallengeResponses={
            'NEW_PASSWORD': event['PASSWORD'],
            'USERNAME':event['USERNAME']
        },
        Session=response['Session']
        )
        response=response2
    response=responses.Response(200,response['AuthenticationResult'],None)
    return response

''' Key=bytearray(Cognito_Config.Poll_AppClient_Secret,'utf8')
    msg=(event['USERNAME']+Cognito_Config.Pool_AppClient_Id).encode("utf-8")
    Signature = hmac.new(Key,msg ,digestmod=hashlib.sha256)
    Hash = base64.b64encode(Signature.digest())
    
        '''