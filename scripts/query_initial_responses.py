"""
Query one page of initial cultural habits responses.
"""

import os

import pandas as pd

from src.data_access.query_initial_responses import QueryInitialResponses


API_KEY = os.getenv('TYPEFORM_API_KEY')


query_responses = QueryInitialResponses("prod", API_KEY)
responses = query_responses.query_all(nb_items_per_page=30, last_page=3)

df = pd.DataFrame(responses)
print(
    df.head()
)
