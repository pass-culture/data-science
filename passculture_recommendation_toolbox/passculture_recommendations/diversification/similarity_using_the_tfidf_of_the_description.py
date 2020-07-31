import numpy as np
import math


def compute_similarity_of_the_offer_with_offers_using_the_index(index_of_the_offer, index_of_the_other_offers,
                                                                similarity_matrix):
    return np.mean(similarity_matrix[index_of_the_offer, index_of_the_other_offers])


def get_index_to_exchange_in_the_least_relevant_offers(dataframe_of_least_relevant_offers,
                                                       dataframe_of_most_relevant_offers,
                                                       real_index_of_the_offer_with_the_highest_similarity,
                                                       index_of_the_offer_with_the_highest_similarity,
                                                       similarity_matrix):
    value_of_the_highest_similarity = dataframe_of_most_relevant_offers.loc[
        index_of_the_offer_with_the_highest_similarity, 'similarite']
    most_relevant_offers_without_the_offer_with_the_highest_similarity = dataframe_of_most_relevant_offers[
        dataframe_of_most_relevant_offers['index'] != real_index_of_the_offer_with_the_highest_similarity]
    index_of_the_most_relevant_offers_without_the_offer_with_the_highest_similarity = \
    most_relevant_offers_without_the_offer_with_the_highest_similarity['index'].values
    for i, row in dataframe_of_least_relevant_offers.iterrows():
        similarity_of_offer_in_the_least_relevant_offers = compute_similarity_of_the_offer_with_offers_using_the_index(
            row['index'], index_of_the_most_relevant_offers_without_the_offer_with_the_highest_similarity,
            similarity_matrix)
        if similarity_of_offer_in_the_least_relevant_offers < value_of_the_highest_similarity:
            dataframe_of_least_relevant_offers.loc[dataframe_of_least_relevant_offers['index'] == row[
                'index'], 'similarite'] = similarity_of_offer_in_the_least_relevant_offers
            return row['index']


def compute_similarity_for_each_offer(most_relevant_offers_recommended_to_a_user, similarity_matrix):
    for index, row in most_relevant_offers_recommended_to_a_user.iterrows():
        other_offers = most_relevant_offers_recommended_to_a_user[
            most_relevant_offers_recommended_to_a_user['index'] != index]
        index_of_the_other_offers = other_offers['index'].values
        similarite = compute_similarity_of_the_offer_with_offers_using_the_index(index, index_of_the_other_offers,
                                                                                 similarity_matrix)
        most_relevant_offers_recommended_to_a_user.loc[index, 'similarite'] = similarite
    return most_relevant_offers_recommended_to_a_user

def get_index_in_the_df_of_the_offer_with_the_highest_similarity(dataframe_of_most_relevant_offers):
    offer_with_the_highest_similarity = dataframe_of_most_relevant_offers[dataframe_of_most_relevant_offers['similarite'] == dataframe_of_most_relevant_offers['similarite'].max()]
    index_of_the_offer_with_the_highest_similarity = offer_with_the_highest_similarity['index'].values
    index_of_the_offer_with_the_highest_similarity = dataframe_of_most_relevant_offers[dataframe_of_most_relevant_offers['index'] == index_of_the_offer_with_the_highest_similarity[0]].index[0]
    return index_of_the_offer_with_the_highest_similarity


def get_column_index_of_the_offer_with_the_highest_similarity(dataframe_of_most_relevant_offers):
    offer_with_the_highest_similarity = dataframe_of_most_relevant_offers[dataframe_of_most_relevant_offers['similarite'] == dataframe_of_most_relevant_offers['similarite'].max()]
    index_of_the_offer_with_the_highest_similarity = offer_with_the_highest_similarity['index'].values
    return index_of_the_offer_with_the_highest_similarity


def compute_combination_of_k_among_n(k, n):
    return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))


def compute_similarity_of_the_set(df1, similarity_matrix, K):
    similarity_of_the_set = 0.
    for i, row in df1.iterrows():
        for j in range(i + 1, len(df1)):
            similarity_of_the_set += (similarity_matrix[df1.loc[i, 'index'], df1.loc[j, 'index']])
    similarity_of_the_set = similarity_of_the_set / compute_combination_of_k_among_n(2, K)
    return similarity_of_the_set
