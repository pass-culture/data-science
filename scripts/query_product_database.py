"""
Query the product database.
Database schema is available in docs/product_database_schema.png
"""
import os

from src.data_access.product_database_connection import ProductDatabaseConnection

PASSWORD = os.getenv('PRODUCT_POSTGRES_PASSWORD')

product_database_connection = ProductDatabaseConnection(private_key_path="/home/jean/.ssh/id_rsa")
dataframe = product_database_connection.query_database(password=PASSWORD, query=f"SELECT * FROM \"stock\" limit 10;")
