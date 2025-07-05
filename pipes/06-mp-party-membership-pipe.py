import os.path
from lxml import etree
import csv
import psycopg2
from harmonize import harmonize_party

with open(os.path.join("data", "MemberOfParliament.tsv")) as f:

    vote_data = list(csv.reader(f, delimiter="\t", quotechar='"'))
        

conn = psycopg2.connect(database="postgres",
                        host="db",
                        user="postgres",
                        password="postgres",
                        port="5432")
cursor = conn.cursor()

cursor.execute("""SELECT id FROM members_of_parliament;""")

active_mps = [mp[0] for mp in cursor.fetchall()]

with open(os.path.join("data", "MemberOfParliament.tsv")) as f:

    mp_data = [row for row in csv.reader(f, delimiter="\t", quotechar='"')]

for mp in mp_data[1:]:

    mp_id = int(mp[0])

    if mp_id not in active_mps:
        continue

    xml = mp[7]
    root = etree.fromstring(xml)

    namespaces = root[0].nsmap

    # Current group
    cur_group = root.find("./Eduskuntaryhmat/NykyinenEduskuntaryhma", namespaces)
    party = harmonize_party(cur_group[0].text)
    AlkuPvm = cur_group.find("./AlkuPvm", namespaces)
    start_date = "-".join(list(reversed((AlkuPvm.text).split("."))))
    end_date = None

    cursor.execute("INSERT INTO mp_party_memberships (mp_id, party_id, start_date, end_date) VALUES (%s, %s, %s, %s);", 
                               (mp_id, party, start_date, end_date))

    for group in root.find("./Eduskuntaryhmat/EdellisetEduskuntaryhmat", namespaces):
        if group[0].text:
            party = harmonize_party(group[0].text)
            
            for membership in group.findall("./Jasenyys", namespaces):
                
                AlkuPvm = membership.find("./AlkuPvm", namespaces)
                start_date = "-".join(list(reversed((AlkuPvm.text).split("."))))
                
                LoppuPvm = membership.find("./LoppuPvm", namespaces)
                end_date = "-".join(list(reversed((LoppuPvm.text).split("."))))

                cursor.execute("INSERT INTO mp_party_memberships (mp_id, party_id, start_date, end_date) VALUES (%s, %s, %s, %s);", 
                               (mp_id, party, start_date, end_date))
                
conn.commit()
cursor.close()
conn.close()