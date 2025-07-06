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



import concurrent.futures
import numpy as np

# Number of splits/files/connections for parallel processing
NUM_SPLITS = 12  # Set this to the desired number of parallel files/connections

def vote_pipe():
    with open(os.path.join("data", "SaliDBAanestysEdustaja.tsv")) as f:
        print("Reading file...")
        vote_data = pd.read_csv(f, sep="\t")[["EdustajaHenkiloNumero", "AanestysId", "EdustajaAanestys"]]
        print("Done!")

    vote_data["EdustajaAanestys"] = vote_data["EdustajaAanestys"].str.strip().apply(
        lambda x: vote_dict[x]
    )

    print(f"Writing {NUM_SPLITS} csv files...")
    vote_data.columns = ["mp_id", "ballot_id", "vote"]
    # Split the DataFrame into NUM_SPLITS parts
    split_dfs = np.array_split(vote_data, NUM_SPLITS)
    csv_paths = []
    for i, split_df in enumerate(split_dfs):
        csv_path = f"data/votes/{i}.csv"
        split_df.to_csv(csv_path, index=False, header=False)
        csv_paths.append(csv_path)
    print("Done!")

    def copy_from_csv(csv_path):
        conn = psycopg2.connect(database="postgres",
                                host="db",
                                user="postgres",
                                password="postgres",
                                port="5432")
        cursor = conn.cursor()
        with open(csv_path) as f:
            cursor.copy_from(f, 'votes', columns=('mp_id', 'ballot_id', 'vote'), sep=",")
        conn.commit()
        cursor.close()
        conn.close()

    print(f"Writing database in parallel with {NUM_SPLITS} connections...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_SPLITS) as executor:
        list(executor.map(copy_from_csv, csv_paths))
    print("Done!")


if __name__ == '__main__':
    vote_pipe()
