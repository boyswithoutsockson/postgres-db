import os.path
import xml.etree.ElementTree as ET
import csv
import psycopg2

csv_path = 'data/preprocessed/interests.csv'

def preprocess_data():
    with open(os.path.join("data", "raw", "MemberOfParliament.tsv")) as f:
        mp_data = list(csv.reader(f, delimiter="\t", quotechar='"'))[1:]  # Skip header

    rows = []
    for mp in mp_data:
        mp_id = mp[0]
        xml = mp[7]
        tree = ET.fromstring(xml)

        interests = {}
        for i in tree.find("Sidonnaisuudet").findall("Sidonnaisuus"):
            interest = i.find("Sidonta")

            if interest is None:
                continue

            if interest.text is None or interest.text == "None" or "Ei ilmoitettavia" in interest.text:
                continue

            interest_type = i.find("RyhmaOtsikko")

            try:
                interests[interest_type.text] = interests[interest_type.text].append(interest.text)
            except:
                interests[interest_type.text] = [interest.text]

        for type in interests:
            if interests[type]:
                for interest in interests[type]:
                    rows.append({
                        "mp_id": mp_id,
                        "category": type,
                        "interest": interest
                    })

    with open(csv_path, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=["mp_id", "category", "interest"])
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
        cursor.copy_expert("COPY interests(mp_id, category, interest) FROM stdin DELIMITERS ',' CSV HEADER QUOTE '\"';", f)

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