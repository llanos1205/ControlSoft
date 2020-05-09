import logging
import db
import json
from responses import Response, getBody
import scripts
import boto3
# nota body y httpmetod soloe stan habilitados si se usalambda proxy integration

client=boto3.client('sns')
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
            id=None
            cond=""
            if('idinvitacion' in event['pathParameters']):
                id=event['pathParameters']['idinvitacion']
                cond="where idinvitacion={}".format(id)
            cursor = db.queryData(CONN, scripts.get_query.format(keys="idinvitacion,idinvitado,idresidente,fechainvitacion,fechadeexpiracion,estado,horamaxentrada,horamaxsalida,codigoinvitacion", table="invitacion",cond=cond))
            resp = db.getJson(cursor)
            return Response(200, resp)
        except Exception as error:
            logger.error("ERROR:Quering Failed with error {}".format(str(error)))
            return Response(500, "Internal Errol")

    elif method == "POST":
        try:
            body = getBody(event)
            keys, values = scripts.key_value_parser(body)
            query = scripts.put_query.format(table="invitacion", keys=keys, values=values)
            #proceso de crear un link/QR mejor usar SNS
            cursor = db.queryData(CONN, query)
            # client.publish(
            #     PhoneNumber='string',
            #     Message='lok',
            #     Subject='string',
            #     MessageStructure='string',
            #     MessageAttributes={
            #         'string': {
            #             'DataType': 'string',
            #             'StringValue': 'string',
            #             'BinaryValue': b'bytes'
            #         }
            #     }
            # )
            return Response(200, "Insert Success")
        except Exception as error:
            logger.error('ERROR:Insertion Failed with error {}'.format(str(error)))
            return Response(500, "Internal Error")
    elif method == "PUT":

        try:
            body = getBody(event)
            query = scripts.update_query.format(table="invitacion", changes="", cond="")
            cursor = db.queryData(CONN, query)
            return Response(200, "Changes effective")
        except Exception as error:
            logger.error("ERROR:Modification Failed with error {}".format(str(error)))
            return Response(500, "Internal Error")
    elif method == "DELETE":
        try:
            body = getBody(event)
            query = scripts.delete_query.format(table="invitacion", cond="idinvitacion={}".format(body['idinvitacion']))
            cursor = db.queryData(CONN, query)
            return Response(200, "Changes effective")
        except Exception as error:
            logger.error("ERROR:Deletion Failed with error {}".format(str(error)))
            return Response(500, "Internal Error")
    elif method == "PATCH":
        try:
            body = getBody(event)

            query = scripts.update_query.format(table="invitado", changes="",cond="idinvitacion={}".format(body['idinvitacion']))
            cursor = db.queryData(CONN, query)
            return Response(200, "Changes effective")
        except Exception as error:
            logger.error("ERROR:Deletion Failed with error {}".format(str(error)))
            return Response(500, "Internal Error")
    else:
        return Response(404,"No managed method")
