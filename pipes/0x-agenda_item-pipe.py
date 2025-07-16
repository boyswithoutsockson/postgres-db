import os.path
import xml.etree.ElementTree as ET
import csv
import psycopg2

csv_path = 'data/preprocessed/agenda_items.csv'

def preprocess_data():
    with open(os.path.join("data", "raw", "SaliDBKohta.tsv")) as fd:
        agenda_item_data = list(csv.reader(fd, delimiter="\t", quotechar='"'))[1:]  # Skip header

    rows = []
    for agenda_item in agenda_item_data:
        rows.append({
            "id": agenda_item[0],
            "title": agenda_item[9],
            "start_time": agenda_item[16],
            "session": f"{agenda_item[1]}",
            "sequence": agenda_item[6],
            "number": agenda_item[7]
        })

    with open(csv_path, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "title", "start_time", "session", "sequence", "number"])
        writer.writeheader()
        writer.writerows(rows)

def import_data():
    conn = psycopg2.connect(database="postgres",
                            host="db",
                            user="postgres",
                            password="postgres",
                            port="5432")
    cursor = conn.cursor()

    with open(csv_path) as f:
        cursor.copy_expert("COPY agenda_items(id, title, start_time, session, sequence, number) FROM stdin DELIMITERS ',' CSV HEADER QUOTE '\"';", f)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--preprocess-data", help="preprocess the data", action="store_true")
    parser.add_argument("--import-data", help="import preprocessed data", action="store_true")
    args = parser.parse_args()
    if args.preprocess_data:
        preprocess_data()
    if args.import_data:
        import_data()
    if not args.preprocess_data and not args.import_data:
        preprocess_data()
        import_data()
