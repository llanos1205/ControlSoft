import bd

#nota body y httpmetod soloe stan habilitados si se usalambda proxy integration
def handler(event, context):
    # responde=bd.Creater()
    method = event['requestContext']['httpMethod']
    if(method == "GET"):
        return {
            'statusCode': 200,
            'body': "thisisa get method"
        }
    elif(method == "POST"):
        try:
            bd.Insertar(event['body'])
            return {
                'statusCode': 200,
                'body': "thisisa post method"
            }
        except:
            return{
                'statusCode': 500,
                'body': "Error al insertar registros"
            }
        
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
