import os.path
import pandas as pd
import numpy as np
import psycopg2
import xmltodict
from db import pg_engine

def mp_committee_membership_pipe():

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
    membership_df = pd.DataFrame(columns=["mp_id", "committee_name", "start_date", "end_date", "role"])
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
                    committee_name = committee["Nimi"]
                    try:
                        memberships = committee["Jasenyys"] if isinstance(committee["Jasenyys"], list) else [committee["Jasenyys"]]
                    except KeyError:
                        continue

                    for membership in memberships:
                        if membership["AlkuPvm"]:
                            start_date = "-".join(list(reversed((membership["AlkuPvm"]).split("."))))
                            if len(start_date) < 10:
                                start_date = f"{start_date[:4]}-01-01"
                            if membership["LoppuPvm"]:
                                end_date = "-".join(list(reversed((membership["LoppuPvm"]).split("."))))
                                if len(end_date) < 10:
                                    end_date = f"{end_date[:4]}-12-31"
                            role = roles[membership["Rooli"].lower()]
                            membership_df.loc[len(membership_df)] = [mp_id, committee_name, start_date, end_date, role]
        
    membership_df.to_csv("data/mp_committee_memberships.csv", index=False, header=False)

    print("Writing database...")
    conn = psycopg2.connect(database="postgres",
                            host="db",
                            user="postgres",
                            password="postgres",
                            port="5432")
    cursor = conn.cursor()
    with open('data/mp_committee_memberships.csv') as f:
        cursor.copy_from(f, 'mp_committee_memberships', columns=('mp_id', 'committee_name', 'start_date', 'end_date', 'role'), sep=",")
    conn.commit()
    cursor.close()
    conn.close()

    print("Done!")

if __name__ == '__main__':
    mp_committee_membership_pipe()