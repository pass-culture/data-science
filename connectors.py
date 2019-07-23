import os

import pygsheets
from sqlalchemy import create_engine


DASHBOARD_GSHEET_SECRET = 'secrets/credentials.json'

def get_worksheet(sheet_name, tab_name):
    gc = pygsheets.authorize(
        client_secret=DASHBOARD_GSHEET_SECRET)
    sheet_name = sheet_name
    dashboard_sheet = gc.open(sheet_name)
    global_tab_name = tab_name
    global_dashboard_worksheet = dashboard_sheet.worksheet_by_title(global_tab_name)
    return global_dashboard_worksheet


def connect_to_postgres():
    engine = create_engine('postgres://data:data@localhost:5432/pass-culture')
    connection = engine.connect()
    return connection
