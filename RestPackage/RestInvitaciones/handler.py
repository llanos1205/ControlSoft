import logging
import db
from responses import responseAgw, getBody
import scripts

CONN = None
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    method = event['requestContext']['httpMethod']
    response = None
    query = None
    global CONN

    if CONN is None:
        CONN = db.connect()
        logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

    identifier = None
    cond = ""
    if event['pathParameters']:
        if 'id' in event['pathParameters']:
            identifier = event['pathParameters']['id']

    if method == "GET":
        try:
            if identifier:
                cond = str("where idpersona={}".format(identifier))
            query = scripts.getQuery.format(keys="idpersona,nombre1,correo", table="persona", cond=cond)

            cursor = db.queryData(CONN, str(query))
            resp = db.getJson(cursor)
            return responseAgw(200, resp)
        except Exception as error:

            logger.error("ERROR:Quering Failed with error {}".format(str(error)))
            return responseAgw(501, str(error))

    elif method == "POST":
        try:
            body = getBody(event)
            keys, values = scripts.keyValueParser(body)
            query = scripts.putQuery.format(table="persona", keys=keys, values=values)
            # proceso de crear un link/QR mejor usar SNS
            cursor = db.queryData(CONN, str(query))
            return responseAgw(200, "Insert Success")
        except Exception as error:

            logger.error('ERROR:Insertion Failed with error {}'.format(str(error)))
            return responseAgw(502, "Internal Error")
    elif method == "PUT":

        try:
            body = getBody(event)
            query = scripts.updateQuery.format(table="persona", changes="", cond="")
            cursor = db.queryData(CONN, query)
            return responseAgw(200, "Changes effective")
        except Exception as error:
            logger.error("ERROR:Modification Failed with error {}".format(str(error)))
            return responseAgw(503, "Internal Error")
    elif method == "DELETE":
        try:
            body = getBody(event)
            if identifier:
                cond = str("where idpersona={}".format(identifier))
            query = scripts.deleteQuery.format(table="persona", cond=cond)
            cursor = db.queryData(CONN, str(query))
            return responseAgw(200, "Changes effective")
        except Exception as error:
            logger.error("ERROR:Deletion Failed with error {}".format(str(error)))
            return responseAgw(504, "Internal Error")
    elif method == "PATCH":
        try:
            body = getBody(event)
            if identifier:
                cond = str("idpersona={}".format(identifier))
            changes = str(scripts.keyValueComparerParser(body))
            query = scripts.updateQuery.format(table="persona", changes=changes, cond=cond)
            cursor = db.queryData(CONN, str(query))
            return responseAgw(200, "Changes effective")
        except Exception as error:
            logger.error("ERROR:Deletion Failed with error {}".format(str(error)))
            return responseAgw(505, str(error))
    else:
        return responseAgw(404, "No managed method")
