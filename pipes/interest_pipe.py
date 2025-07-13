import os.path
import xml.etree.ElementTree as ET
import csv
import psycopg2
import xmltodict
import pandas as pd

def interest_pipe():
    with open(os.path.join("data", "MemberOfParliament.tsv"), "r") as f:
        MoP = pd.read_csv(f, sep="\t")

    xml_dicts = MoP.XmlDataFi.apply(xmltodict.parse)
    rows = []
    for henkilo in xml_dicts:
        mp_id = henkilo['Henkilo']['HenkiloNro']

        if henkilo['Henkilo']['Sidonnaisuudet'] is None:
            continue

        interest = henkilo['Henkilo']['Sidonnaisuudet']['Sidonnaisuus']

        if isinstance(interest, dict):
            interest = [interest]

        rows.extend([
            {'mp_id': mp_id, 'category': x['RyhmaOtsikko'], 'interest': x['Sidonta']}
            for x in interest
            if 'Sidonta' in x and x['Sidonta'] not in [None, 'Ei ilmoitettavia sidonnaisuuksia', 'Ei ilmoitettavia tuloja']
        ])

    print("Writing csv...")
    with open('data/interests.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=["mp_id", "category", "interest"])
        writer.writerows(rows)
    print("Done!")

    print("Writing database...")
    conn = psycopg2.connect(database="postgres",
                            host="db",
                            user="postgres",
                            password="postgres",
                            port="5432")
    cursor = conn.cursor()
    with open('data/interests.csv') as f:
        cursor.copy_expert("COPY interests(mp_id, category, interest) FROM stdin DELIMITERS ',' CSV QUOTE '\"';", f)

    print("Done!")

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    interest_pipe()