import os.path
import csv
import psycopg2

def ballot_pipe():
    with open(os.path.join("data", "SaliDBAanestys.tsv")) as f:

        ballot_data = list(csv.reader(f, delimiter="\t", quotechar='"'))

    conn = psycopg2.connect(database="postgres",
                            host="db",
                            user="postgres",
                            password="postgres",
                            port="5432")
    cursor = conn.cursor()

    for ballot in ballot_data[1:]:

        id = ballot[0]
        title = ballot[12]
        session_item_title = ballot[21]
        start_time = f"{ballot[9]} Europe/Helsinki"
        parliament_id = ballot[31]
        minutes_url = ballot[30]
        results_url = ballot[28]

        cursor.execute("INSERT INTO ballots (id, title, session_item_title, start_time, minutes_url, results_url) VALUES (%s, %s, %s, %s, %s, %s);", 
                        (id, title, session_item_title, start_time, minutes_url, results_url))
        
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    ballot_pipe()
