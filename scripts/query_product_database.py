import ast
import json
import os

from src.data_access.product_database_connection import ProductDatabaseConnection


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

product_database_connection = ProductDatabaseConnection(
    private_key_path="~/id_rsa", **SSH
)
dataframe = product_database_connection.query_database(query=f'SELECT * FROM "stock" limit 10;', **CONNECTION)
