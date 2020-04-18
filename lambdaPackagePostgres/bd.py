import psycopg2
import rds_config
def Creater():
    conn=None
    cursor=None
    try:
        conn = psycopg2.connect( host=rds_config.db_host,
          database=rds_config.db_name,
          user=rds_config.db_user,
          password=rds_config.db_password)
        cursor = conn.cursor()
        Query = """ CREATE TABLE role(
	    role_id serial PRIMARY KEY,
	    role_name VARCHAR (255) UNIQUE NOT None
            )    """

 
        cursor.executemany(Query)
        conn.commit()
        print(cursor.rowcount, "Registros insertados correctamente!!")

    except (Exception, psycopg2.Error) as error:
        print("Error al insertar registros {}".format(error))

    finally:
        if (conn):
            cursor.close()
            conn.close()
    return "SUccess"



def Insertar(registros):
    conn=None
    cursor=None
    try:
        conn = psycopg2.connect( host=rds_config.db_host,
          database=rds_config.db_name,
          user=rds_config.db_user,
          password=rds_config.db_password)
        cursor = conn.cursor()
        Query = """ INSERT INTO persona (idpersona, nombre, carnet) 
                           VALUES (%s,%s,%s) """

 
        cursor.executemany(Query, registros)
        conn.commit()
        print(cursor.rowcount, "Registros insertados correctamente!!")

    except (Exception, psycopg2.Error) as error:
        print("Error al insertar registros {}".format(error))

    finally:
        if (conn):
            cursor.close()
            conn.close()



def Modificar(registros):
    conn=None
    cursor=None
    try:
        conn = psycopg2.connect( host=rds_config.db_host,
          database=rds_config.db_name,
          user=rds_config.db_user,
          password=rds_config.db_password)
        cursor = conn.cursor()
        
        Query = """Update persona set nombre = %s where personaid = %s"""
        cursor.executemany(Query, registros)
        conn.commit()

        row_count = cursor.rowcount
        print(row_count, "registros modificados")

    except (Exception, psycopg2.Error) as error:
        print("Error while updating PostgreSQL table", error)

    finally:
      
        if (conn):
            cursor.close()
            conn.close()

        



def getPersonaDetail(ID):
    conn=None
    cursor=None
    try:
        conn = psycopg2.connect( host=rds_config.db_host,
          database=rds_config.db_name,
          user=rds_config.db_user,
          password=rds_config.db_password)
        cursor = conn.cursor()

       
        Query = "select * from persona where idpersona = %s"

        cursor.execute(Query, (ID,))
        registros = cursor.fetchall()
        for row in registros:
            print("Id = ", row[0], )
            print("Nombre = ", row[1])
            print("Carnet  = ", row[2])

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)

    finally:
        # closing database connection
        if (conn):
            cursor.close()
            conn.close()
           


def getnameDetail():
    conn=None
    cursor=None
    try:
        conn = psycopg2.connect( host=rds_config.db_host,
          database=rds_config.db_name,
          user=rds_config.db_user,
          password=rds_config.db_password)
        cursor = conn.cursor()
        Query = "select tablename from pg_catalog.pg_tables where schemaname!='pg_catalog' AND schemaname != 'information_schema';"

        cursor.execute(Query)
        registros = cursor.fetchall()
        for row in registros:
            print("table = ", row[0] )
		
    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)

    finally:
      
        if (conn):
            cursor.close()
            conn.close()			




def getableDetail():
    conn=None
    cursor=None
    try:
        conn = psycopg2.connect( host=rds_config.db_host,
          database=rds_config.db_name,
          user=rds_config.db_user,
          password=rds_config.db_password)
        cursor = conn.cursor()
        Query = """SELECT
  					    COLUMN_NAME
					 FROM
   						information_schema.COLUMNS
					 WHERE
   					 TABLE_NAME = 'persona';"""
        cursor.execute(Query)
        registros = cursor.fetchall()
        for row in registros:
            print("table = ", row[1] )
		
    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)

    finally:
      
        if (conn):
            cursor.close()
            conn.close()			




