import psycopg2

DB_HOST = 'localhost'
DB_NAME = 'clinrec'
DB_USER = 'postgres'
DB_PASS = 'Slender123'

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

cur = conn.cursor()

# cur.execute("INSERT INTO recommendation VALUES(1, 'raz dva tri chetire pyat', '10')")

print(cur.fetchall())

cur.close()

conn.close()
