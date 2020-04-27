# The verification is valid only for 24 hours, Lets say the user missed that window to confirm her/his registration,
#  then he can request the verification code again from cognito.
import json
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import uuid
import Cognito_Config
USER_POOL_ID = Cognito_Config.Pool_Id
CLIENT_ID = Cognito_Config.Pool_AppClient_Id
CLIENT_SECRET = Cognito_Config.Pool_AppClient_Secret

def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'), 
        msg = str(msg).encode('utf-8'),
        digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2
def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    try:
        username = event['username']
        response = client.resend_confirmation_code(
        ClientId=CLIENT_ID,
        SecretHash=get_secret_hash(username),
        Username=username,
    )
    except client.exceptions.UserNotFoundException:
        return {"error": True, "success": False, "message":   "Username doesnt exists"}
        
    except client.exceptions.InvalidParameterException:
        return {"error": True, "success": False, "message": "User is already confirmed"}
    
    except Exception as e:
        return {"error": True, "success": False, "message": f"Unknown error {e.__str__()} "}
      
    return  {"error": False, "success": True}