import os
import pandas as pd
import xml.etree.ElementTree as ET
import csv
import psycopg2
from harmonize import harmonize_party

with open(os.path.join("data", "MemberOfParliament.tsv")) as f:
    df = pd.read_csv(f, sep="\t")
    mp_data = list(csv.reader(f, delimiter="\t", quotechar='"'))

conn = psycopg2.connect(database="postgres",
                        host="db",
                        user="postgres",
                        password="postgres",
                        port="5432")
cursor = conn.cursor()

photo_filenames = os.listdir("frontend/src/assets/")
photo_filename_dict = {
    filename.split(".")[0].split("-")[-1]: filename for filename in photo_filenames
}

for mp in df.iterrows():
    mp = mp[1]

    id = mp['personId']

    minister = True if mp['minister'] == 't' else False

    xml = mp['XmlDataFi']
    tree = ET.fromstring(xml)

    first_name = mp['firstname'].strip()
    last_name = mp['lastname'].strip()
    full_name = f"{tree[1].text} {tree[2].text}"
    phone_number = tree[6].text
    email = tree[7].text
    occupation = tree[9].text
    year_of_birth = tree[10].text
    place_of_birth = tree[11].text
    place_of_residence = tree[15].text
    constituency = tree[26][0][0].text
    try:
        photo = photo_filename_dict[id]
    except KeyError:
        photo = None  # No photo available

    cursor.execute("INSERT INTO members_of_parliament (id, first_name, last_name, full_name, minister, phone_number, email, occupation, year_of_birth, place_of_birth, place_of_residence, constituency, photo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", 
                   (id, first_name, last_name, full_name, minister, phone_number, email, occupation, year_of_birth, place_of_birth, place_of_residence, constituency, photo))
    
conn.commit()
cursor.close()
conn.close()