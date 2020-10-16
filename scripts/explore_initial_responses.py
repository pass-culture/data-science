"""
Reshape initial cultural habits responses in a pandas dataframe and save it in data/dataframe_api_responses.csv.
"""
import json
import os
import re

import pandas as pd
from pandas_profiling import ProfileReport
from typeform import Typeform


API_KEY = os.getenv("TYPEFORM_API_KEY")
FORM_ID = os.getenv("NEW_PROD_FORM_ID")

# We use the python API to retrieve data on questions
typeform = Typeform(API_KEY)
form = typeform.forms.get(FORM_ID)
fields = (
    pd.DataFrame(form.get("fields"))
    .rename(columns={"id": "question_id"})
    .drop("type", axis=1)
)


# We open the json of saved answers obtained from the API
with open("data/api_responses_new_form.json") as json_file:
    responses = json.load(json_file)

authentified_responses = len([response.get('metadata').get('referer') for response in responses if 'userId=' in response.get('metadata').get('referer')])
# number of users (list of answers for each user)
print(f"User having answered: {len(responses)}")
print(f"Authentified users having answered: {authentified_responses}")


# we want one line for each user answer
dataframe = (
    pd.DataFrame(responses)
    .explode("answers")
    .dropna()
    .assign(
        network_id=lambda df: df.metadata.apply(
            lambda metadata: metadata.get("network_id")
        ),
        culturalSurveyId=lambda df: df.metadata.apply(
            lambda metadata: re.search(r"userId=(.*?)&", metadata.get("referer"))
        ).apply(lambda regexp: regexp.group(1) if regexp else None),
        question_id=lambda df: df["answers"].apply(
            lambda answer: answer.get("field").get("id") if answer else None
        ),
        question_type=lambda df: df["answers"].apply(
            lambda answer: answer.get("type") if answer else None
        ),
        answer=lambda df: df.apply(
            lambda row: row["answers"].get(row["question_type"])
            if row["answers"]
            else None,
            axis=1,
        ),
        answer_label=lambda df: df.apply(
            lambda row: row["answer"].get(
                "label" if row["question_type"] == "choice" else "labels"
            )
            if row["answer"]
            else None,
            axis=1,
        ),
    )
    .merge(fields, on="question_id", how="inner")
    .drop(
        [
            "landing_id",
            "token",
            "response_id",
            "metadata",
            "hidden",
            "calculated",
            "answers",
            "ref",
            "properties",
            "validations",
        ],
        axis=1,
    )
    .rename(columns={"title": "question"})
)


# Exploration

profile = ProfileReport(dataframe, title="Initial cultural habits answers")
profile.to_file(f"data/table_reports/initial_cultural_habits/answers.html")

# pandas profiling can not handle answer_label (does not support list type)
dataframe = dataframe.dropna(subset=["culturalSurveyId"])
for question in dataframe["question"].value_counts().index.tolist():
    print(question)
    print(dataframe.loc[lambda df: df.question == question].shape[0])
    print(dataframe.loc[lambda df: df.question == question]["answer_label"].values[:3])
    print()
