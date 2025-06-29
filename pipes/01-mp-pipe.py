import xml.etree.ElementTree as ET
import csv
import psycopg2
from harmonize import harmonize_party

mp_data = []

with open("data/MemberOfParliament.tsv") as fd:

    for row in csv.reader(fd, delimiter="\t", quotechar='"'):
        mp_data.append(row)

conn = psycopg2.connect(database="postgres",
                        host="db",
                        user="postgres",
                        password="postgres",
                        port="5432")
cursor = conn.cursor()

mp_data = mp_data[1:]

for mp in mp_data:

    id = mp[0]

    if len(mp[3]) == 0:
        continue
    party = harmonize_party(mp[3])

    minister = True if mp[4] == 't' else False

    xml = mp[7]
    tree = ET.fromstring(xml)

    first_name = tree[4].text
    full_name = f"{tree[1].text} {tree[2].text}"
    phone_number = tree[6].text
    email = tree[7].text
    occupation = tree[9].text
    year_of_birth = tree[10].text
    place_of_birth = tree[11].text
    place_of_residence = tree[15].text
    constituency = tree[26][0][0].text
    
    cursor.execute("INSERT INTO members_of_parliament (id, first_name, full_name, party, minister, phone_number, email, occupation, year_of_birth, place_of_birth, place_of_residence, constituency) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", 
                   (id, first_name, full_name, party, minister, phone_number, email, occupation, year_of_birth, place_of_birth, place_of_residence, constituency))
    
conn.commit()
cursor.close()
conn.close()