import logging
import db
import json
from responses import Response, getBody
import scripts

# nota body y httpmetod soloe stan habilitados si se usalambda proxy integration


CONN = None
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    method = event['requestContext']['httpMethod']
    response = None
    global CONN

    if CONN is None:
        CONN = db.Connect()
        logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

    if method == "GET":
        try:
            cursor = db.queryData(CONN, scripts.get_query.format(keys="name,type", table="invitado"))
            resp = db.getJson(cursor)
            return Response(200, resp)
        except Exception as error:
            logger.error("ERROR:Quering Failed with error {0}", str(error))
            return Response(500, "Internal Errol")

    elif method == "POST":
        try:
            body = getBody(event)
            keys, values = scripts.key_value_parser(body)
            query = scripts.put_query.format(table="invitado", keys=keys, values=values)
            cursor = db.queryData(CONN, query)
            return Response(200, "Insert Success")
        except Exception as error:
            logger.error("ERROR:Insertion Failed with error {0}", str(error))
            return Response(500, "Internal Error")
    elif method == "PUT":

        try:
            body = getBody(event)
            query = scripts.update_query.format(table="invitado", changes="", cond="")
            cursor = db.queryData(CONN, query)
            return Response(200, "Changes effective")
        except Exception as error:
            logger.error("ERROR:Modification Failed with error {0}", str(error))
            return Response(500, "Internal Error")
    elif method == "DELETE":
        try:
            body = getBody(event)
            query = scripts.delete_query.format(table="invitado", cond="")
            cursor = db.queryData(CONN, query)
            return Response(200, "Changes effective")
        except Exception as error:
            logger.error("ERROR:Deletion Failed with error {0}", str(error))
            return Response(500, "Internal Error")
    elif method == "PATCH":
        try:
            body = getBody(event)
            query = scripts.update_query.format(table="invitado", changes="", cond="")
            cursor = db.queryData(CONN, query)
            return Response(200, "Changes effective")
        except Exception as error:
            logger.error("ERROR:Deletion Failed with error {0}", str(error))
            return Response(500, "Internal Error")
    else:
        return Response(404,"No managed method")
