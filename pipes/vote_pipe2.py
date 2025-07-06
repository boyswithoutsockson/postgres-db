import os.path
import csv
import psycopg2
import pandas as pd
from db import pg_engine


vote_dict = {"Jaa": "yes",
            "Ja": "yes",
            "Yes": "yes",
            "Ei": "no",
            "Nej": "no",
            "No": "no",
            "Poissa": "absent",
            "Frånvarande": "absent",
            "Absent": "absent",
            "Tyhjää": "abstain",
            "Avstår": "abstain",
            "Blank": "abstain"}

def vote_pipe():
    with open(os.path.join("data", "SaliDBAanestysEdustaja.tsv")) as f:
        print("Reading file...")
        vote_data = pd.read_csv(f, sep="\t")[["EdustajaHenkiloNumero", "AanestysId", "EdustajaAanestys"]]
        print("Done!")

    vote_data["EdustajaAanestys"] = vote_data["EdustajaAanestys"].str.strip().apply(
        lambda x: vote_dict[x]
    )

    print("Writing csv...")
    vote_data.columns = ["mp_id", "ballot_id", "vote"]
    vote_data.to_csv("data/votes.csv", index=False, header=False)
    print("Done!")


    print("Writing database...")
    conn = psycopg2.connect(database="postgres",
                            host="db",
                            user="postgres",
                            password="postgres",
                            port="5432")
    cursor = conn.cursor()
    with open('data/votes.csv') as f:
        cursor.copy_from(f, 'votes', columns=('mp_id', 'ballot_id', 'vote'), sep=",")

    print("Done!")


if __name__ == '__main__':
    vote_pipe()
