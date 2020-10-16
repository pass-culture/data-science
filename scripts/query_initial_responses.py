"""
Query one page of initial cultural habits responses.
"""
import json
import os

from src.data_access.query_initial_responses import QueryInitialResponses


API_KEY = os.getenv("TYPEFORM_API_KEY")
FORM_ID = os.getenv("NEW_PROD_FORM_ID")


query_responses = QueryInitialResponses(API_KEY, FORM_ID)
responses = query_responses.query_all()

with open("data/api_responses_new_form.json", "w") as json_file:
    json.dump(responses, json_file)
