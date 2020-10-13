"""
Reshape initial cultural habits responses in a pandas dataframe and save it in data/dataframe_api_responses.csv.
"""
import json
import os
import re

import pandas as pd
from typeform import Typeform


API_KEY = os.getenv("TYPEFORM_API_KEY")
FORM_ID = os.getenv("PROD_FORM_ID")

# We use the python API to retrieve data on questions
typeform = Typeform(API_KEY)
form = typeform.forms.get(FORM_ID)
fields = (
    pd.DataFrame(form.get("fields"))
    .rename(columns={"id": "question_id"})
    .drop("type", axis=1)
)


# We open the json of saved answers obtained from the API
with open("data/api_responses.json") as json_file:
    responses = json.load(json_file)

# number of users (list of answers for each user)
print(len(responses))


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

# we obtain only 65,692 different culturalSurveyId, and only 78,977 network_id !!!
dataframe["culturalSurveyId"].nunique()
dataframe["network_id"].nunique()

# we compare with downloaded data
downloaded_data = pd.read_csv("data/responses.csv")
downloaded_data["Network ID"].nunique()

# 78 310 different Network ID (less recent data)

# There are 21 questions

# We compute the number of answers to each of the 21 questions, along with 3 answer values
# We remove lines without ID
dataframe = dataframe.dropna(subset=["culturalSurveyId"])
for question in dataframe["question"].value_counts().index.tolist():
    print(question)
    print(dataframe.loc[lambda df: df.question == question].shape[0])
    print(dataframe.loc[lambda df: df.question == question]["answer_label"].values[:3])
    print()


# We visualize the first values of each column and we compare with downloaded data
for col in downloaded_data.columns:
    print(f"{col} : {downloaded_data[col].values[:3]}")

for col in dataframe.columns:
    print(f"{col} : {dataframe[col].values[:3]}")

dataframe.to_csv("data/dataframe_api_responses.csv", index=None)
