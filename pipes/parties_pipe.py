import os.path
import pandas as pd
import numpy as np
import xmltodict
import psycopg2
from harmonize import harmonize_party

csv_path = 'data/preprocessed/parties.csv'


def preprocess_data():
    with open(os.path.join("data", "raw", "MemberOfParliament.tsv"), "r") as f:
        MoP = pd.read_csv(f, sep="\t")

    xml_dicts = MoP.XmlDataFi.apply(xmltodict.parse)
    parties = []
    for henkilo in xml_dicts:
        try:
            parties.append(henkilo['Henkilo']['Eduskuntaryhmat']['NykyinenEduskuntaryhma']['Nimi'])
        except KeyError:
            pass  # Ei nykyistä puoluetta
        try:
            parties.append(henkilo['Henkilo']['Eduskuntaryhmat']['EdellisetEduskuntaryhmat']['Eduskuntaryhma']['Nimi'])
        except TypeError:
            if henkilo['Henkilo']['Eduskuntaryhmat']['EdellisetEduskuntaryhmat']:
                for ekr in henkilo['Henkilo']['Eduskuntaryhmat']['EdellisetEduskuntaryhmat']['Eduskuntaryhma']:
                    parties.append(ekr['Nimi'])
    parties = [p for p in set(parties) if p is not None]

    party_keys = [harmonize_party(party) for party in parties]
    parties_df = pd.DataFrame({"id": party_keys, "name": parties})

    parties_df.to_csv(csv_path, index=False)


def import_data():
    conn = psycopg2.connect(database="postgres",
                            host="db",
                            user="postgres",
                            password="postgres",
                            port="5432")
    cursor = conn.cursor()

    with open(csv_path) as f:
        cursor.copy_expert("COPY parties(id, name) FROM stdin DELIMITERS ',' CSV HEADER QUOTE '\"';", f)

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
