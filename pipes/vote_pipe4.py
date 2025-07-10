import polars as pl
import time
from pathlib import Path
from db import URI

VOTE_MAPPING = {
    "Jaa": "yes",
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
    "Blank": "abstain",
}
COLUMN_MAPPING = {
    "EdustajaHenkiloNumero": "mp_id",
    "AanestysId": "ballot_id",
    "EdustajaAanestys": "vote",
}
FILEPATH = Path("data", "SaliDBAanestysEdustaja.tsv")

if __name__ == "__main__":
    start = time.perf_counter()
    count = (
        pl.read_csv(FILEPATH, separator="\t")
        .select(
            pl.col("EdustajaHenkiloNumero"),
            pl.col("AanestysId"),
            pl.col("EdustajaAanestys").replace(VOTE_MAPPING),
        )
        .rename(COLUMN_MAPPING)
        .write_database(
            table_name="votes",
            connection=URI,
            engine="adbc",
        )
    )
    end = time.perf_counter()
    print(f"Executed in {end - start:.2f} seconds. Created {count} rows.")
