from time import sleep

import docker
from docker.errors import NotFound

client = docker.from_env()
print("<<<<<|   STARTING DATABASE   |>>>>>")

try:
    database = client.containers.get("pass-culture-data-science")
except NotFound:
    client.containers.run(
        "postgres",
        name="pass-culture-data-science",
        ports={"5432/tcp": 5432},
        environment={
            "POSTGRES_USER": "data",
            "POSTGRES_PASSWORD": "data",
            "POSTGRES_DB": "pass-culture",
        },
        detach=True,
        volumes={
            "pc_data_postgres": {"bind": "/var/lib/postgresql/data", "mode": "rw"}
        },
    )
    sleep(3)
else:
    if database.attrs["State"]["Running"] is False:
        database.start()
        sleep(3)

print("<<<<<|   DATABASE STARTED   |>>>>>")
