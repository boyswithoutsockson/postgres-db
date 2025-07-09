import os
import pandas as pd
from db import pg_engine
import xmltodict
import psycopg2

def committee_pipe():
    
    committees = {"Suuri valiokunta": "SuV",
                    "Perustuslakivaliokunta": "PeV",
                    "Ulkoasiainvaliokunta": "UaV",
                    "Valtiovarainvaliokunta": "VaV",
                    "Tarkastusvaliokunta": "TrV",
                    "Hallintovaliokunta": "HaV",
                    "Lakivaliokunta": "LaV",
                    "Liikenne- ja viestintävaliokunta": "LiV",
                    "Maa- ja metsätalousvaliokunta": "MmV",
                    "Puolustusvaliokunta": "PuV",
                    "Sivistysvaliokunta": "SiV",
                    "Sosiaali- ja terveysvaliokunta": "StV",
                    "Talousvaliokunta": "TaV",
                    "Tiedusteluvalvontavaliokunta": "TiV",
                    "Tulevaisuusvaliokunta": "TuV",
                    "Työelämä- ja tasa-arvovaliokunta": "TyV",
                    "Ympäristövaliokunta": "YmV"}

    earliest_retirement_date = "2000-01-01"

    roles = {"jäsen": "member",
          "varajäsen": "associate",
          "lisäjäsen": "additional",
          "puheenjohtaja": "chair",
          "varapuheenjohtaja": "first vice",
          "ensimmäinen varapuheenjohtaja": "first vice",
          "toinen varapuheenjohtaja": "second vice"}

    with open(os.path.join("data", "MemberOfParliament.tsv"), "r") as f:
        MoP = pd.read_csv(f, sep="\t")

    xml_dicts = MoP.XmlDataFi.apply(xmltodict.parse)
    committee_df = pd.DataFrame(columns=["committee_name"])
    for henkilo in xml_dicts:
        mp_id = int(henkilo['Henkilo']["HenkiloNro"])
        if henkilo['Henkilo']['KansanedustajuusPaattynytPvm']:
            retirement_date = "-".join(list(reversed((henkilo['Henkilo']['KansanedustajuusPaattynytPvm']).split("."))))
        else:
            continue

        if retirement_date < earliest_retirement_date:
            continue

        cur_committees = henkilo['Henkilo']['NykyisetToimielinjasenyydet']['Toimielin']

        if isinstance(cur_committees, dict):
            cur_committees = [cur_committees]
        
        try:
            prev_committees = henkilo['Henkilo']['AiemmatToimielinjasenyydet']['Toimielin']
        except TypeError:
            prev_committees = []

        if isinstance(prev_committees, dict):
            prev_committees = [prev_committees]

        for committee in cur_committees + prev_committees:
            if committee['Nimi']:
                if committee["@OnkoValiokunta"] == 'true':
                    committee_df.loc[len(committee_df)] = committee["Nimi"]
    
    committee_df = committee_df.drop_duplicates()
    committee_df.to_csv("data/committees.csv", index=False, header=False)

    print("Writing database...")
    conn = psycopg2.connect(database="postgres",
                            host="db",
                            user="postgres",
                            password="postgres",
                            port="5432")
    cursor = conn.cursor()
    with open('data/committees.csv') as f:
        cursor.copy_from(f, 'committees', sep=",")
    conn.commit()
    cursor.close()
    conn.close()

    print("Done!")

if __name__ == "__main__":
    committee_pipe()