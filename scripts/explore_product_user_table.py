import ast
import json
import os

from pandas_profiling import ProfileReport

from src.data_access.database_connection import DatabaseConnection


SSH = os.getenv("PRODUCT_DATABASE_SSH")
CONNECTION = os.getenv("PRODUCT_DATABASE_CONNECTION")

if type(SSH) == str:
    SSH = ast.literal_eval(SSH)
else:
    SSH = json.loads(SSH)

if type(CONNECTION) == str:
    CONNECTION = ast.literal_eval(CONNECTION)
else:
    CONNECTION = json.loads(CONNECTION)

database_connection = DatabaseConnection(
    private_key_path="~/id_rsa", **SSH
)

for table_index, table in enumerate([
    "user",
    "offer",
    "product",
    "stock",
    "seen_offer",
    "venue",
    "venue_provider",
    "recommendation",
    "booking",
    "provider",
    "offerer"
    "seen_offer"
]):
    print(table)
    dataframe = database_connection.query_database(query=f'SELECT count(*) FROM "{table}";', **CONNECTION)
    nb_rows = dataframe['count'].values[0]
    if nb_rows < 300000:
        dataframe = database_connection.query_database(query=f'SELECT * FROM "{table}";', **CONNECTION)
        profile = ProfileReport(dataframe, title=f"{table_index + 1}. Table product.{table}")
        profile.to_file(f"data/table_reports/product/{table_index + 1}_{table}.html")
    else:
        print(nb_rows)
