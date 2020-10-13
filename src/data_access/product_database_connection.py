import pandas as pd
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine


class DatabaseQueryError(Exception):
    pass


class ProductDatabaseConnection:
    def __init__(
            self,
            private_key_path,
            ssh_host,
            ssh_port,
            ssh_user_name,
            ssh_local_bind_host,
            ssh_local_bind_port,
            ssh_remote_bind_host,
            ssh_remote_bind_port
    ):
        self.private_key_path = private_key_path
        self.ssh_host = ssh_host
        self.ssh_port = ssh_port
        self.ssh_user_name = ssh_user_name
        self.ssh_local_bind_host = ssh_local_bind_host
        self.ssh_local_bind_port = ssh_local_bind_port
        self.ssh_remote_bind_host = ssh_remote_bind_host
        self.ssh_remote_bind_port = ssh_remote_bind_port

    def define_server(self):
        return SSHTunnelForwarder(
            (self.ssh_host, self.ssh_port),
            ssh_username=self.ssh_user_name,
            ssh_pkey=self.private_key_path,
            local_bind_address=(self.ssh_local_bind_host, self.ssh_local_bind_port),
            remote_bind_address=(self.ssh_remote_bind_host, self.ssh_remote_bind_port)
        )

    def query_database(self, query, password, database, user, host, port):
        server = self.define_server()
        server.daemon_forward_servers = True

        server.start()
        try:
            engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
            data = pd.read_sql(query, engine)
            server.stop()
            return data
        except:
            server.stop()
            raise DatabaseQueryError("Database could not be queried.")
