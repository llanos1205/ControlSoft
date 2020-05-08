import logging
import db
import json
from responses import Response
import scripts

# nota body y httpmetod soloe stan habilitados si se usalambda proxy integration


CONN = None
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    method = event['requestContext']['httpMethod']
    response = None
    global CONN

    if (CONN is None):
        CONN = db.Connect()
        logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

    if (method == "GET"):
        try:
            cursor = db.queryData(CONN, scripts.get_query.format(keys="name,type", table="test"))
            resp = db.getJson(cursor)
            return Response(200, resp)
        except Exception as error:
            logger.error("ERROR:Quering Failed with error {0}", str(error))
            return Response(500, "Internal Errol")

    elif (method == "POST"):
        try:
            body = json.loads(event['body'])
            query = scripts.put_query.format(table="",keys=str(body.keys()).join(","))
            cursor = db.queryData(CONN, query)
            return Response(200, "Insertion Success")
        except Exception as error:
            logger.error("ERROR:Insertion Failed with error {0}", str(error))
            return Response(500, "Internal Errol")
    elif (method == "PUT"):
        return {
            'statusCode': 200,
            'body': "thisisa put method"
        }
    elif (method == "DELETE"):
        return {
            'statusCode': 200,
            'body': "thisisa delet method"
        }
    elif (method == "PATCH"):
        return {
            'statusCode': 200,
            'body': "thisisa patch method"
        }
    else:
        return {
            'statusCode': 404,
            'body': "unhandled method"
        }
