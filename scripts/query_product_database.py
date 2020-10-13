"""
Query the product database.
Database schema is available in docs/product_database_schema.png
"""
import ast
import os

from src.data_access.product_database_connection import ProductDatabaseConnection

SSH = os.getenv("PRODUCT_DATABASE_SSH")
CONNECTION = os.getenv("PRODUCT_DATABASE_CONNECTION")

if type(SSH) == str:
    SSH = ast.literal_eval(SSH)
if type(CONNECTION) == str:
    CONNECTION = ast.literal_eval(CONNECTION)

product_database_connection = ProductDatabaseConnection(
    private_key_path="/home/jean/.ssh/id_rsa", **SSH
)
dataframe = product_database_connection.query_database(query=f'SELECT * FROM "stock" limit 10;', **CONNECTION)

print(dataframe)
