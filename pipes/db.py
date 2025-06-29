from sqlalchemy import create_engine


def pg_engine():
    return create_engine('postgresql://postgres:postgres@db:5432/postgres')
