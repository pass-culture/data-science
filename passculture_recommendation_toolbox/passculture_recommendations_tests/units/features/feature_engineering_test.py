from sqlalchemy import create_engine
engine = create_engine('postgres://pytest:pytest@localhost:5433/pass_culture?sslmode=prefer')
from passculture_recommendations.data.feature_engineering import get_user_offer_interaction_and_put_a_grade
from passculture_recommendations.data.feature_engineering import get_a_df_from_sql_query

import pandas as pd

df = pd.DataFrame({'userId': [1, 2, 3], 'offerId': [23, 32, 45]})
df.to_sql('users_offers', con=engine, if_exists='replace')
df_with_grade_4 = pd.DataFrame({'userId': [1, 2, 3], 'offerId': [23, 32, 45], 'note': [4, 4, 4]})

def test_get_a_df_from_sql_query():
    # Given
    query = """ SELECT * FROM users_offers """
    connection = engine.connect()

    # When
    df_users_offers = get_a_df_from_sql_query(query, connection)
    del df_users_offers['index']

    # Then
    pd.testing.assert_frame_equal(df, df_users_offers)


def test_get_user_offer_interaction_and_put_a_grade():
    # Given
    query = """ SELECT * FROM users_offers """
    grade = 4
    connection = engine.connect()

    # When
    df_users_offers_with_grade = get_user_offer_interaction_and_put_a_grade(query, grade, connection)
    del df_users_offers_with_grade['index']

    # Then
    pd.testing.assert_frame_equal(df_with_grade_4, df_users_offers_with_grade)

