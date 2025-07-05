import os.path
import csv
import psycopg2

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

    vote_data = list(csv.reader(f, delimiter="\t", quotechar='"'))
        

conn = psycopg2.connect(database="postgres",
                        host="db",
                        user="postgres",
                        password="postgres",
                        port="5432")
cursor = conn.cursor()


cursor.execute("""SELECT id FROM members_of_parliament;""")

active_mps = [mp[0] for mp in cursor.fetchall()]

for vote_instance in vote_data[1:]:
    
    mp_id = int(vote_instance[4])

    if mp_id not in active_mps:
        continue

    ballot_id = vote_instance[1]
    vote = vote_instance[6].strip()
    
    cursor.execute("INSERT INTO votes (ballot_id, mp_id, vote) VALUES (%s, %s, %s);", 
                    (ballot_id, mp_id, vote_dict[vote]))
    
conn.commit()
cursor.close()
conn.close()