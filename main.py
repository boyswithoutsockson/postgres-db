import psycopg2
from pipes.run_pipes import run_pipes


conn = psycopg2.connect(database="postgres",
                        host="db",
                        user="postgres",
                        password="postgres",
                        port="5432")
cursor = conn.cursor()

print("Dropping all tables...")
cursor.execute(open("DELETE ALL TABLES.sql", "r").read())
conn.commit()
print("Done!")

print("Creating tables...")
cursor.execute(open("postgres-init-scripts/01_create_tables.sql", "r").read())
conn.commit()
print("Done!")

print("Start running pipes")
run_pipes()
