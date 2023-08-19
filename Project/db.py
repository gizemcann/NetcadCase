import psycopg2

#connect to the db
con = psycopg2.connect(
            host = "localhost",
            database = "dvdrental",
            user = "postgres",
            password = "123456")


#cursor
cur = con.cursor()

#execute the query
cur.execute("select id, name, salary from employees")

rows = cur.fetchall()

for r in rows:
    print(f"id {r[0]} name {r[1]} salary {r[2]}")

#close the cursor
cur.close()

#close the connection
con.close()