from psycopg2.extras import RealDictCursor
import json
import psycopg2
import rds_config
import logging
import sys
logger=logging.getLogger()
logger.setLevel(logging.INFO)
def Connect():
    conn=None
    try :
        conn = psycopg2.connect( 
            host=rds_config.db_host,
            database=rds_config.db_name,
            user=rds_config.db_user,
            password=rds_config.db_password
        )
    except (Exception, psycopg2.Error) as error:
        logger.error("ERROR:Connection Failed with error :{0}",str(error))
        sys.exit()
    return conn
    

def Creater(conn,Query):
    cursor=None
    response="noting happened"
    try:
        cursor = conn.cursor()
        cursor.execute(Query)
        conn.commit()
        response="Success"
    except (Exception, psycopg2.Error) as error:
        logger.error("ERROR: Creations failed with error: {0}",str(error))
        response="something wrong happened"
        #write error to CW
    return response



def insertData(conn,Query):
    cursor=None
    response=None
    try:
        cursor = conn.cursor()
        cursor.execute(Query)
        conn.commit()
        print(cursor.rowcount, "Registros insertados correctamente!!")
        response="Row Inserted"+str(cursor.rowcount)
    except (Exception, psycopg2.Error) as error:
        logger.error("ERROR:INsertion Failed with error: {0}",str(error))
        response=str(error)

    return response


def updateData(conn,Query):
    cursor=None
    response=0
    try:
        cursor = conn.cursor()
        cursor.execute(Query)
        response ="Update rows: "+ cursor.rowcount
        conn.commit()      
        print(response, "registros modificados")
    except (Exception, psycopg2.Error) as error:
        logger.error("ERROR:Update Failed with error: {0}",str(error))
        response=str(error)
    return response
#returns a string
def queryData(conn,Query):
    cursor=None
    rows=None
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(Query)
        rows = cursor.fetchall()  
    except (Exception, psycopg2.Error) as error:
        logger.error("ERROR:Quering Failed with error {0}",str(error))
        rows=str(error)
    return json.dumps(rows,indent=2)



