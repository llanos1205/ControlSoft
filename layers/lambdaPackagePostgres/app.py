import logging
import db
import json
#nota body y httpmetod soloe stan habilitados si se usalambda proxy integration


CONN=None
logger = logging.getLogger()
logger.setLevel(logging.INFO)
def handler(event, context):
    # responde=bd.Creater()
    method = event['requestContext']['httpMethod']
    error={
                'statusCode': 500,
                'body': "error alguna parte"
            }
    response=None
    global CONN
    if(CONN is None):
        CONN=db.Connect()
        logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
    if(method == "GET"):
        try:
            response=db.queryData(CONN,"SELECT * FROM role2")
            return {
                'statusCode': 200,
                'body': response
            }
        except:
            return error
        
    elif(method == "POST"):
        try:
            body=json.loads(event['body'])
            query="INSERT INTO role2(role_name) VALUES('{0}');".format(body['role_name'])
            response=db.insertData(CONN,query)
            return {
                'statusCode': 200,
                'body': response
            } 
        except Exception as x: 
            return x
    elif(method == "PUT"):
        return {
            'statusCode': 200,
            'body': "thisisa put method"
        }
    elif(method == "DELETE"):
        return {
            'statusCode': 200,
            'body': "thisisa delet method"
        }
    elif(method == "PATCH"):
        return {
            'statusCode': 200,
            'body': "thisisa patch method"
        }
    else:
        return{
            'statusCode': 404,
            'body': "unhandled method"
        }
