import xml.etree.ElementTree as ET
import csv
import psycopg2

agenda_item_data = []

with open("SaliDBKohta.tsv") as fd:

    for row in csv.reader(fd, delimiter="\t", quotechar='"'):
        agenda_item_data.append(row)

conn = psycopg2.connect(database="postgres",
                        host="db",
                        user="postgres",
                        password="postgres",
                        port="5432")
cursor = conn.cursor()

agenda_item_data = agenda_item_data[1:]
for agenda_item in agenda_item_data:

    id = agenda_item[0]
    title = agenda_item[9]
    start_time = agenda_item[16]
    session = f"{agenda_item[1]}"
    sequence = agenda_item[6]
    number = agenda_item[7]

    cursor.execute("INSERT INTO agenda_items (id, title, start_time, session, sequence, number) VALUES (%s, %s, %s, %s, %s, %s);", 
                    (id, title, start_time, session, sequence, number))
    
conn.commit()
cursor.close()
conn.close()
