import os.path
import pandas as pd
import numpy as np
from db import pg_engine
from harmonize import harmonize_party


with open(os.path.join("data", "MemberOfParliament.tsv"), "r") as f:
    parties = pd.read_csv(f, sep="\t").party.unique()

parties = parties[~pd.isnull(parties)]
party_keys = [harmonize_party(party) for party in parties]
parties = pd.DataFrame({"id": party_keys, "name": parties})


parties.to_sql(name="parties", con=pg_engine(), if_exists="append", index=False)