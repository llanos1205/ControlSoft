from psycopg2.extras import RealDictCursor
import json
import psycopg2
import rds_config
import logging
import sys
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def Connect():
    conn = None
    try:
        conn = psycopg2.connect(
            host=rds_config.db_host,
            database=rds_config.db_name,
            user=rds_config.db_user,
            password=rds_config.db_password
        )
    except (Exception, psycopg2.Error) as error:
        logger.error("ERROR:Connection Failed with error :{0}", str(error))
        sys.exit()
    return conn


def queryData(conn, Query):
    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(Query)
        for queryType in ["INSERT", "UPDATE","DELETE","PATCH"]:
            if queryType in Query:
                conn.commit()
                break
    except (Exception, psycopg2.Error) as error:
        logger.error("ERROR:Quering Failed with error {0}", str(error))
    return cursor


def getJson(cursor):
    return json.dumps(cursor.fetchall(), indent=2)
