import math
from itertools import combinations
import pandas as pd

def compute_similarity_of_each_type(number_of_offer_per_type: pd.DataFrame, similarity_matrix: pd.DataFrame) -> float:
    number_of_offer_per_type.loc[:,'similarity_between_types'] = 0
    for type1 in number_of_offer_per_type['type']:
        similarity_between_types = 0
        for type2 in number_of_offer_per_type['type']:
            number_of_type2 = number_of_offer_per_type.loc[number_of_offer_per_type['type']==str(type2), 'total'].values
            similarity_between_types += number_of_type2[0] * similarity_matrix.loc[str(type1), str(type2)]

        similarity_between_types -= 1
        number_of_offer_per_type.loc[number_of_offer_per_type['type']==str(type1), 'similarity_between_types'] = similarity_between_types

    return number_of_offer_per_type


def compute_combination_of_k_among_n(k, n):
    return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))


def compute_similarity_between_offers_of_same_type(number_of_offers_per_type: pd.DataFrame):
    for i, row in number_of_offers_per_type.iterrows():
        if row['total'] > 1:
            number_of_offers_per_type.loc[i, 'number_of_possible_pairs_of_offers'] = compute_combination_of_k_among_n(2,
                                                                                                                      row[
                                                                                                                          'total'])
        else:
            number_of_offers_per_type.loc[i, 'number_of_possible_pairs_of_offers'] = 0
    return number_of_offers_per_type['number_of_possible_pairs_of_offers'].sum()


def compute_similarity_between_offers_of_different_types(type1, type2, number_of_offers_per_type, similarity_matrix):
    type1 = str(type1)
    type2 = str(type2)
    number_of_offers_of_type1 = number_of_offers_per_type.loc[
        number_of_offers_per_type['type'] == type1, 'total'].values
    number_of_offers_of_type2 = number_of_offers_per_type.loc[
        number_of_offers_per_type['type'] == type2, 'total'].values
    similarity_between_2_types = similarity_matrix.loc[type1, type2]
    return (number_of_offers_of_type1 * number_of_offers_of_type2) * similarity_between_2_types


def compute_similarity_of_the_set(number_of_offers_per_type: pd.DataFrame, similarity_matrix: pd.DataFrame, number_of_exchanges) -> float:
    similarity_of_the_set = compute_similarity_between_offers_of_same_type(
        number_of_offers_per_type)
    for type1, type2 in combinations(number_of_offers_per_type['type'], 2):
        type1 = str(type1)
        type2 = str(type2)
        similarity_between_offers_of_type1_and_type2 = compute_similarity_between_offers_of_different_types(
            type1, type2, number_of_offers_per_type, similarity_matrix)
        similarity_of_the_set += similarity_between_offers_of_type1_and_type2
    similarity_of_the_set = similarity_of_the_set / compute_combination_of_k_among_n(2, number_of_exchanges)
    return similarity_of_the_set
