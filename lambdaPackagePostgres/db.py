from psycopg2.extras import RealDictCursor
import json
import psycopg2
import rds_config
def Creater(Query):
    conn=None
    cursor=None
    response="noting happened"
    try:
        conn = psycopg2.connect( 
        host=rds_config.db_host,
        database=rds_config.db_name,
        user=rds_config.db_user,
        password=rds_config.db_password
        )
        cursor = conn.cursor()
        cursor.execute(Query)
        conn.commit()
        response="Success"
    except (Exception, psycopg2.Error) as error:
        response="something wrong happened"
        #write error to CW

    finally:
        if (conn):
            cursor.close()
            conn.close()
    return response



def insertData(Query):
    conn=None
    cursor=None
    response=None
    try:
        conn = psycopg2.connect( host=rds_config.db_host,
          database=rds_config.db_name,
          user=rds_config.db_user,
          password=rds_config.db_password)
        cursor = conn.cursor()
        cursor.execute(Query)
        conn.commit()
        print(cursor.rowcount, "Registros insertados correctamente!!")
        response="Row Inserted"+str(cursor.rowcount)
    except (Exception, psycopg2.Error) as error:
        print("Error al insertar registros {}".format(error))
        response=str(error)

    finally:
        if (conn is not None):
            cursor.close()
            conn.close()
    return response


def updateData(Query):
    conn=None
    cursor=None
    response=0
    try:
        conn = psycopg2.connect( host=rds_config.db_host,
          database=rds_config.db_name,
          user=rds_config.db_user,
          password=rds_config.db_password)
        cursor = conn.cursor()
        cursor.execute(Query)
        response ="Update rows: "+ cursor.rowcount
        conn.commit()

        
        print(response, "registros modificados")

    except (Exception, psycopg2.Error) as error:
        print("Error while updating PostgreSQL table", error)
        response=str(error)

    finally:
      
        if (conn is not None):
            cursor.close()
            conn.close()
    return response
#returns a string
def queryData(Query):
    conn=None
    cursor=None
    rows=None
    try:
        conn = psycopg2.connect( host=rds_config.db_host,
          database=rds_config.db_name,
          user=rds_config.db_user,
          password=rds_config.db_password)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(Query)
        rows = cursor.fetchall()
        
    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)
        rows=str(error)

    finally:
        # closing database connection
        if (conn):
            cursor.close()
            conn.close()
    return json.dumps(rows,indent=2)



