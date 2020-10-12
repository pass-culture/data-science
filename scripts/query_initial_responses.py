"""
Query one page of initial cultural habits responses.
"""
import json
import os

from src.data_access.query_initial_responses import QueryInitialResponses


API_KEY = os.getenv("TYPEFORM_API_KEY")


query_responses = QueryInitialResponses("prod", API_KEY)
responses = query_responses.query_all()

with open("data/api_responses.json", "w") as json_file:
    json.dump(responses, json_file)
