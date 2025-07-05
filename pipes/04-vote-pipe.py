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

with open(os.path.join("data", "SaliDBAanestysEdustaja.tsv")) as f:
    print("Reading file...")
    vote_data = pd.read_csv(f, sep="\t")[["EdustajaHenkiloNumero", "AanestysId", "EdustajaAanestys"]]
    print("Done!")

#for vote_instance in vote_data[1:]:
#    mp_id = int(vote_instance[4])
#    ballot_id = vote_instance[1]
#    vote = vote_instance[6].strip()
#    cursor.execute("INSERT INTO votes (ballot_id, mp_id, vote) VALUES (%s, %s, %s);", 
#                    (ballot_id, mp_id, vote_dict[vote]))

vote_data["EdustajaAanestys"] = vote_data["EdustajaAanestys"].str.strip().apply(
    lambda x: vote_dict[x]
)

vote_data.columns = ["mp_id", "ballot_id", "vote"]

print("Writing...")
vote_data.to_sql(name="votes", con=pg_engine(), if_exists="append", index=False)
print("Done!")
