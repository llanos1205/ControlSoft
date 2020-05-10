import logging
import db
import json
from responses import Response, getBody
import scripts
import boto3

# nota body y httpmetod soloe stan habilitados si se usalambda proxy integration

CONN = None
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    method = event['requestContext']['httpMethod']
    response = None
    query = None
    global CONN

    if CONN is None:
        CONN = db.Connect()
        logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

    id = None
    cond = ""
    if (event['pathParameters']):
        if ('id' in event['pathParameters']):
            id = event['pathParameters']['id']

    if method == "GET":
        try:
            if (id):
                cond = str("where idpersona={}".format(id))
            query = scripts.get_query.format(keys="idpersona,nombre1,correo", table="persona", cond=cond)

            cursor = db.queryData(CONN, str(query))
            resp = db.getJson(cursor)
            return Response(200, resp)
        except Exception as error:

            logger.error("ERROR:Quering Failed with error {}".format(str(error)))
            return Response(501, str(error))

    elif method == "POST":
        try:
            body = getBody(event)
            keys, values = scripts.key_value_parser(body)
            query = scripts.put_query.format(table="persona", keys=keys, values=values)
            # proceso de crear un link/QR mejor usar SNS
            cursor = db.queryData(CONN, str(query))
            return Response(200, "Insert Success")
        except Exception as error:

            logger.error('ERROR:Insertion Failed with error {}'.format(str(error)))
            return Response(502, "Internal Error")
    elif method == "PUT":

        try:
            body = getBody(event)
            query = scripts.update_query.format(table="persona", changes="", cond="")
            cursor = db.queryData(CONN, query)
            return Response(200, "Changes effective")
        except Exception as error:
            logger.error("ERROR:Modification Failed with error {}".format(str(error)))
            return Response(503, "Internal Error")
    elif method == "DELETE":
        try:
            body = getBody(event)
            if (id):
                cond = str("where idpersona={}".format(id))
            query = scripts.delete_query.format(table="persona", cond=cond)
            cursor = db.queryData(CONN, str(query))
            return Response(200, "Changes effective")
        except Exception as error:
            logger.error("ERROR:Deletion Failed with error {}".format(str(error)))
            return Response(504, "Internal Error")
    elif method == "PATCH":
        try:
            body = getBody(event)
            if (id):
                cond = str("idpersona={}".format(id))
            changes = str(scripts.key_value_comparer_parser(body))
            query = scripts.update_query.format(table="persona", changes=changes, cond=cond)
            cursor = db.queryData(CONN, str(query))
            return Response(200, "Changes effective")
        except Exception as error:
            logger.error("ERROR:Deletion Failed with error {}".format(str(error)))
            return Response(505, str(error))
    else:
        return Response(404, "No managed method")
