import pandas as pd
import numpy as np
from passculture_recommendations.diversification.similarity_using_the_tfidf_of_the_description import \
    compute_similarity_of_the_offer_with_offers_using_the_index, \
    get_index_to_exchange_in_the_least_relevant_offers, \
    compute_similarity_for_each_offer, \
    get_index_in_the_df_of_the_offer_with_the_highest_similarity, \
    get_column_index_of_the_offer_with_the_highest_similarity,\
    compute_combination_of_k_among_n,\
    compute_similarity_of_the_set


def test_compute_similarity_and_return_mean_of_similarity_with_target_offer():
    # Given
    similarity_matrix = np.array([[1., 0.2, 0.3, 0.9],
                                  [0.2, 1, 0.8, 0.7],
                                  [0.3, 0.8, 1, 0.4],
                                  [0.9, 0.7, 0.4, 1]])

    index = 1

    index_of_the_other_offers = [0, 2]

    # When
    sim = compute_similarity_of_the_offer_with_offers_using_the_index(index, index_of_the_other_offers,
                                                                      similarity_matrix)

    # Then
    assert sim == 0.5


def test_get_index_to_exchange_in_the_least_relevant_offers():
    # Given
    dataframe_of_most_relevant_offers = pd.DataFrame(
        [[1, 34, 0.0, 0.512879, 'ThingType.MUSIQUE', False, 1, 93, 93.0,
          'Retrouvez pour la première fois les albums de ...', 0, 0.25],
         [1, 54, 0.0, 0.507554, 'ThingType.MUSEES_PATRIMOINE_ABO', False, 1, 93, 75.0,
          'Pour réserver vos billets, appelez le', 1, 0.5],
         [1, 64, 0.0, 0.469921, 'ThingType.MUSIQUE', False, 1, 93, 93.0,
          'Retrouvez pour la première fois les albums de ...', 2, 0.55]],
        columns=['user_id', 'offer_id', 'note', 'score', 'type', 'isVirtual', 'score_avec_seuil', 'user_cp', 'offer_cp',
                 'description', 'index', 'similarite'])

    dataframe_of_least_relevant_offers = pd.DataFrame(
        [[1, 78, 1.0, 0.150278, 'ThingType.INSTRUMENT', False, 1, 93, 93.0,
          'ampli Basse 15 watts rms pour Basse.\nParfait ...', 3],
         [1, 96, 0.0, 0.150109, 'EventType.MUSIQUE', False, 1, 93, 75.0,
          'CARTE BLANCHE À EMILIE MARSH\n\nEmilie Marsh n...', 4],
         [1, 9, 0.0, 0.148882, 'EventType.MUSIQUE', False, 1, 93, 75.0,
          'Un merveilleux programme "4 x Bach" de concert...', 5]],
        columns=['user_id', 'offer_id', 'note', 'score', 'type', 'isVirtual', 'score_avec_seuil', 'user_cp', 'offer_cp',
                 'description', 'index'])

    real_index_of_the_offer_with_the_highest_similarity = 2
    index_of_the_offer_with_the_highest_similarity = 2

    similarity_matrix = np.array([[1., 0.2, 0.3, 0.9, 0.6, 0.3],
                                  [0.2, 1., 0.8, 0.7, 0.4, 0.3],
                                  [0.3, 0.8, 1., 0.4, 0.8, 0.1],
                                  [0.9, 0.7, 0.4, 1., 0.4, 0.2],
                                  [0.6, 0.4, 0.8, 0.4, 1., 0.3],
                                  [0.3, 0.3, 0.1, 0.2, 0.3, 1.]])
    # When
    index = get_index_to_exchange_in_the_least_relevant_offers(
        dataframe_of_least_relevant_offers,
        dataframe_of_most_relevant_offers,
        real_index_of_the_offer_with_the_highest_similarity,
        index_of_the_offer_with_the_highest_similarity,
        similarity_matrix)
    # Then
    assert index == 4


def test_compute_similarity_for_each_offer():
    # Given
    dataframe_of_most_relevant_offers = pd.DataFrame(
        [[1, 34, 0.0, 0.512879, 'ThingType.MUSIQUE', False, 1, 93, 93.0,
          'Retrouvez pour la première fois les albums de ...', 0],
         [1, 54, 0.0, 0.507554, 'ThingType.MUSEES_PATRIMOINE_ABO', False, 1, 93, 75.0,
          'Pour réserver vos billets, appelez le', 1],
         [1, 64, 0.0, 0.469921, 'ThingType.MUSIQUE', False, 1, 93, 93.0,
          'Retrouvez pour la première fois les albums de ...', 2]],
        columns=['user_id', 'offer_id', 'note', 'score', 'type', 'isVirtual', 'score_avec_seuil', 'user_cp',
                 'offer_cp',
                 'description', 'index'])

    similarity_matrix = np.array([[1., 0.2, 0.3, 0.9, 0.6, 0.3],
                                  [0.2, 1., 0.8, 0.7, 0.4, 0.3],
                                  [0.3, 0.8, 1., 0.4, 0.8, 0.1],
                                  [0.9, 0.7, 0.4, 1., 0.4, 0.2],
                                  [0.6, 0.4, 0.8, 0.4, 1., 0.3],
                                  [0.3, 0.3, 0.1, 0.2, 0.3, 1.]])

    # When
    dataframe_of_most_relevant_offers_with_column_similarity_added = compute_similarity_for_each_offer(dataframe_of_most_relevant_offers, similarity_matrix)

    # Then
    columns_it_should_return = ['user_id', 'offer_id', 'note', 'score', 'type', 'isVirtual', 'score_avec_seuil', 'user_cp', 'offer_cp', 'description', 'index', 'similarite']
    assert list(dataframe_of_most_relevant_offers_with_column_similarity_added.columns) == columns_it_should_return

def test_get_index_of_the_offer_with_the_highest_similarity():
    # Given
    dataframe_of_most_relevant_offers = pd.DataFrame(
        [[1, 34, 0.0, 0.512879, 'ThingType.MUSIQUE', False, 1, 93, 93.0,
          'Retrouvez pour la première fois les albums de ...', 0, 0.25],
         [1, 54, 0.0, 0.507554, 'ThingType.MUSEES_PATRIMOINE_ABO', False, 1, 93, 75.0,
          'Pour réserver vos billets, appelez le', 1, 0.5],
         [1, 64, 0.0, 0.469921, 'ThingType.MUSIQUE', False, 1, 93, 93.0,
          'Retrouvez pour la première fois les albums de ...', 2, 0.55]],
        columns=['user_id', 'offer_id', 'note', 'score', 'type', 'isVirtual', 'score_avec_seuil', 'user_cp',
                 'offer_cp',
                 'description', 'index', 'similarite'])

    # When
    index = get_index_in_the_df_of_the_offer_with_the_highest_similarity(dataframe_of_most_relevant_offers)

    # Then
    assert index == 2

def test_get_index_of_the_offer_with_the_highest_similarity():
    # Given
    dataframe_of_most_relevant_offers = pd.DataFrame(
        [[1, 34, 0.0, 0.512879, 'ThingType.MUSIQUE', False, 1, 93, 93.0,
          'Retrouvez pour la première fois les albums de ...', 3, 0.25],
         [1, 54, 0.0, 0.507554, 'ThingType.MUSEES_PATRIMOINE_ABO', False, 6, 93, 75.0,
          'Pour réserver vos billets, appelez le', 1, 0.5],
         [1, 64, 0.0, 0.469921, 'ThingType.MUSIQUE', False, 1, 93, 93.0,
          'Retrouvez pour la première fois les albums de ...', 8, 0.55]],
        columns=['user_id', 'offer_id', 'note', 'score', 'type', 'isVirtual', 'score_avec_seuil', 'user_cp',
                 'offer_cp',
                 'description', 'index', 'similarite'])

    # When
    index = get_column_index_of_the_offer_with_the_highest_similarity(dataframe_of_most_relevant_offers)

    # Then
    assert index == 8

def test_compute_combination_of_k_among_n():
    # Given
    n = 3
    k = 2

    # When
    combination_of_k_among_n = compute_combination_of_k_among_n(k, n)

    # Then
    assert combination_of_k_among_n == 3

def test_compute_similarity_of_the_set():
    # Given
    similarity_matrix = np.array([[1., 0.2, 0.3, 0.9],
                                  [0.2, 1, 0.8, 0.7],
                                  [0.3, 0.8, 1, 0.4],
                                  [0.9, 0.7, 0.4, 1]])

    dataframe_of_most_relevant_offers = pd.DataFrame(
        [[1, 34, 0.0, 0.512879, 'ThingType.MUSIQUE', False, 1, 93, 93.0,
          'Retrouvez pour la première fois les albums de ...', 0, 0.25],
         [1, 54, 0.0, 0.507554, 'ThingType.MUSEES_PATRIMOINE_ABO', False, 1, 93, 75.0,
          'Pour réserver vos billets, appelez le', 1, 0.5],
         [1, 64, 0.0, 0.469921, 'ThingType.MUSIQUE', False, 1, 93, 93.0,
          'Retrouvez pour la première fois les albums de ...', 2, 0.55]],
        columns=['user_id', 'offer_id', 'note', 'score', 'type', 'isVirtual', 'score_avec_seuil', 'user_cp', 'offer_cp',
                 'description', 'index', 'similarite'])

    number_of_exchanges = 50

    # When
    similarity_of_the_set = compute_similarity_of_the_set(dataframe_of_most_relevant_offers, similarity_matrix, number_of_exchanges)

    # Then
    assert similarity_of_the_set == 1.3 / compute_combination_of_k_among_n(2, number_of_exchanges)
