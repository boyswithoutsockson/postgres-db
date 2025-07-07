from sqlalchemy import create_engine

URI = "postgresql://postgres:postgres@db:5432/postgres"

def pg_engine():
    return create_engine(
        URI,
        use_insertmanyvalues=True,
    )
