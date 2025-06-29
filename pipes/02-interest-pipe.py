import os.path
import xml.etree.ElementTree as ET
import csv
import psycopg2

with open(os.path.join("data", "MemberOfParliament.tsv")) as f:

    mp_data = [row for row in csv.reader(f, delimiter="\t", quotechar='"')]


conn = psycopg2.connect(database="postgres",
                        host="db",
                        user="postgres",
                        password="postgres",
                        port="5432")
cursor = conn.cursor()

mp_data = mp_data[1:]

for mp in mp_data:

    mp_id = mp[0]

    xml = mp[7]
    tree = ET.fromstring(xml)

    interests = {}

    for i in tree.find("Sidonnaisuudet").findall("Sidonnaisuus"):
        interest = i.find("Sidonta")

        if interest is None:
            continue

        if interest.text is None or interest.text == "None" or "Ei ilmoitettavia" in interest.text:
            continue

        interest_type = i.find("RyhmaOtsikko")

        try:
            interests[interest_type.text] = interests[interest_type.text].append(interest.text)
        except:
            interests[interest_type.text] = [interest.text]

    for type in interests:
        type = type
        if interests[type]:
            for interest in interests[type]:
                cursor.execute("INSERT INTO Interests (mp_id, category, interest) VALUES (%s, %s, %s);", 
                               (mp_id, type, interest))
                

conn.commit()

cursor.close()
conn.close()
