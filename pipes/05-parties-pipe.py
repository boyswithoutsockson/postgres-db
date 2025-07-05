import os.path
import pandas as pd
import numpy as np
import xmltodict
from db import pg_engine
from harmonize import harmonize_party


with open(os.path.join("data", "MemberOfParliament.tsv"), "r") as f:
    MoP = pd.read_csv(f, sep="\t")

xml_dicts = MoP.XmlDataFi.apply(xmltodict.parse)
parties = []
for henkilo in xml_dicts:
    try:
        parties.append(henkilo['Henkilo']['Eduskuntaryhmat']['NykyinenEduskuntaryhma']['Nimi'])
    except KeyError:
        pass  # Ei nykyistä puoluetta
    try:
        parties.append(henkilo['Henkilo']['Eduskuntaryhmat']['EdellisetEduskuntaryhmat']['Eduskuntaryhma']['Nimi'])
    except TypeError:
        if henkilo['Henkilo']['Eduskuntaryhmat']['EdellisetEduskuntaryhmat']:
            for ekr in henkilo['Henkilo']['Eduskuntaryhmat']['EdellisetEduskuntaryhmat']['Eduskuntaryhma']:
                parties.append(ekr['Nimi'])
parties = [p for p in set(parties) if p is not None]

party_keys = [harmonize_party(party) for party in parties]
parties = pd.DataFrame({"id": party_keys, "name": parties})

parties.to_sql(name="parties", con=pg_engine(), if_exists="append", index=False)
