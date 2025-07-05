import os.path
import csv
import psycopg2
import pandas as pd
from .db import pg_engine


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

    vote_data.columns = ["mp_id", "ballot_id", "vote"]

    print("Writing...")
    vote_data.to_sql(name="votes",
                     con=pg_engine(),
                     if_exists="append",
                     index=False,
                     chunksize=5000,
                     method='multi')
    print("Done!")


if __name__ == '__main__':
    vote_pipe()
