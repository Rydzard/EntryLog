import psycopg2

def connect_to_database(dbname, user, password, host='localhost', port='5432'):
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    return conn