
import db

#nota body y httpmetod soloe stan habilitados si se usalambda proxy integration
def handler(event, context):
    # responde=bd.Creater()
    method = event['requestContext']['httpMethod']
    error={
                'statusCode': 500,
                'body': "Error al insertar registros"
            }
    response=None
    if(method == "GET"):
        try:
     #       esponse=db.Creater("""CREATE TABLE role2(
	#role_id serial PRIMARY KEY,
	#role_name VARCHAR (255) UNIQUE NOT NULL);""")
            response=db.queryData("SELECT * FROM role2")
            return {
                'statusCode': 200,
                'body': response
            }
        except:
            return error
        
    elif(method == "POST"):
        try:
            query="INSERT INTO role2(role_name) VALUES('{0}');".format(event['body']['role_name'])
            response=db.insertData(query)
            return {
                'statusCode': 200,
                'body': response
            }
        except:
            return error
    elif(method == "PUT"):
        return {
            'statusCode': 200,
            'body': "thisisa put method"
        }
    elif(method == "DELETE"):
        return {
            'statusCode': 200,
            'body': "thisisa delete method"
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
