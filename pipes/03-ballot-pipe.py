import csv
import psycopg2

ballot_data = []

with open("SaliDBAanestys.tsv") as fd:

    for row in csv.reader(fd, delimiter="\t", quotechar='"'):
        ballot_data.append(row)


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

ballot_data = ballot_data[1:]
for ballot in ballot_data:

    id = ballot[0]
    title = ballot[12]
    session_item_title = ballot[21]
    start_time = f"{ballot[9]} Europe/Helsinki"
    minutes_url = ballot[30]
    results_url = ballot[28]

    cursor.execute("INSERT INTO ballots (id, title, session_item_title, start_time, minutes_url, results_url) VALUES (%s, %s, %s, %s, %s, %s);", 
                    (id, title, session_item_title, start_time, minutes_url, results_url))
    
conn.commit()
cursor.close()
conn.close()
