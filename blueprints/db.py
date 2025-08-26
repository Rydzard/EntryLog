import psycopg2

def connect_to_database():
    conn = psycopg2.connect(
        dbname='mydatabase',
        user='myuser',
        password='mypassword',
        host='192.168.51.40',
        port='5432'
    )
    return conn