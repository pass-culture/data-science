from surprise import SVD
from surprise import Dataset
from surprise import Reader
from surprise.model_selection import train_test_split
import pandas as pd


def svd_for_the_recommendation_training(df_of_userid_offerid_and_the_grade):

    reader = Reader(rating_scale=(0, 1))
    data = Dataset.load_from_df(df_of_userid_offerid_and_the_grade[['user_id', 'offer_id', 'note']], reader)

    trainset, testset = train_test_split(data, train_size=0.75, test_size=0.25)

    algo = SVD(n_factors=100)
    algo.fit(trainset)

    return algo, testset

def svd_for_the_recommendation_testing(algo, testset):
    predictions_of_the_grades = algo.test(testset)

    df_of_the_predictions_of_the_grades = pd.DataFrame(predictions_of_the_grades)
    df_of_the_predictions_of_the_grades.columns = ['user_id', 'offer_id', 'note', 'score', 'details']
    del df_of_the_predictions_of_the_grades['details']

    return df_of_the_predictions_of_the_grades
