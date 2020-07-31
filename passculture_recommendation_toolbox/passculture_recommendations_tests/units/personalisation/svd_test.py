import pandas as pd
from passculture_recommendations.personalisation.svd import svd_for_the_recommendation_testing
from passculture_recommendations.personalisation.svd import svd_for_the_recommendation_training


def test_svd_for_the_recommendation_testing():
    # Given
    df_of_userid_offerid_and_the_grade = pd.DataFrame(
        data=[[0, 1, 0], [1, 23, 1], [23, 43, 1], [46, 57, 1], [34, 43, 0]], columns=['user_id', 'offer_id', 'note'])

    algo, testset = svd_for_the_recommendation_training(df_of_userid_offerid_and_the_grade)

    # When
    df_of_the_predictions_of_the_grades = svd_for_the_recommendation_testing(algo, testset)

    # Then
    assert list(df_of_the_predictions_of_the_grades.columns) == ['user_id', 'offer_id', 'note', 'score']
