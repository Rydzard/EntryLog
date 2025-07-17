import psycopg2

con = psycopg2.connect(
    host="localhost",
    database="mydatabase",
    user="myuser",
    password="mypassword"
)

cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS mytable (id integer, name text)")
cur.execute("INSERT INTO mytable (id, name) VALUES (1, 'John')")
con.commit()

cur.execute("SELECT * FROM mytable")
rows = cur.fetchall()
print(rows)