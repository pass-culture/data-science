from sqlalchemy import create_engine


def connect_to_database():
    engine = create_engine('postgres://data:data@localhost:5432/pass-culture')
    connection = engine.connect()
    return connection