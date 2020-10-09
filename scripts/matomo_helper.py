# -*- coding: utf-8 -*-

import logging
import os
import shlex
import subprocess
import json
import mysql.connector


class Matomo:
    def __init__(self, identity_file: str = "~/id_rsa", is_prod: bool = False):
        self.identity_file = identity_file
        self.tunnel = None
        self.mydb = None
        self.is_prod = is_prod
        if self.is_prod:
            self.matomo_infos = json.loads(os.environ.get("MATOMO_PROD"))
        else:
            self.matomo_infos = json.loads(os.environ.get("MATOMO_STAGING"))
        self.connect()

    def connect(self):
        """
        Creates a tunnel between two hosts. Like ssh -L <LOCAL_PORT>:host:<REMOTE_PORT>.
        Hard coded in for now. Down the line, it will pull from connections panel.
        """

        local_port = 10000
        database_host = self.matomo_infos["host"]
        database_port = self.matomo_infos["port"]

        ssh_tunnel_command = """ssh -L {local_port}:{database_host}:{database_port} -i {identity_file} git@{ssh_hostname} -N""".format(
            local_port=local_port,
            database_host=database_host,
            database_port=database_port,
            identity_file=self.identity_file,
            ssh_hostname="ssh.osc-fr1.scalingo.com",
        )

        print(
            "Opening tunnel with command : {ssh_tunnel_command}".format(
                ssh_tunnel_command=ssh_tunnel_command
            )
        )

        args = shlex.split(ssh_tunnel_command)
        print("Creating tunnel")
        self.tunnel = subprocess.Popen(args)

        print("Connecting to the MySQL database")
        self.mydb = mysql.connector.connect(
            host="localhost",
            user=self.matomo_infos["user"],
            password=self.matomo_infos["password"],
            port=local_port,
            database=self.matomo_infos["dbname"],
        )

    def run_query(self, query: str):
        if not self.mydb:
            self.connect()

        cursor = self.mydb.cursor()
        cursor.execute(query)
        return cursor

    def kill_tunnel(self):
        if not self.tunnel:
            print("No existing tunnel")
        else:
            print("Terminating tunnel")
            self.tunnel.kill()
            self.tunnel = None
