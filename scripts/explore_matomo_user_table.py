import ast
import json
import os

from pandas_profiling import ProfileReport

from src.data_access.database_connection import DatabaseConnection


SSH = os.getenv("STAGING_MATOMO_DATABASE_SSH")
CONNECTION = os.getenv("STAGING_MATOMO_DATABASE_CONNECTION")

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
dataframe = database_connection.query_database(query=f'SELECT * FROM user;', **CONNECTION)

profile = ProfileReport(dataframe, title="Table matomo.user")
profile.to_file(f"data/table_reports/matomo/user.html")
