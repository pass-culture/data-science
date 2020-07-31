import pandas as pd
from passculture_recommendations.diversification.similarity_using_the_confusion_matrix import compute_similarity_of_each_type,\
    compute_combination_of_k_among_n, \
    compute_similarity_between_offers_of_same_type, \
    compute_similarity_between_offers_of_different_types, \
    compute_similarity_of_the_set


def test_compute_similarity_of_each_type_return_0_if_there_is_just_one_offer():
    # Given
    similarity_matrix = pd.DataFrame({
        'ThingType.MUSEES_PATRIMOINE_ABO_physique': [1, 0.5, 0.6, 0.2],
        'ThingType.CINEMA_ABO_physique': [0.5, 1, 0.2, 0.3],
        'ThingType.INSTRUMENT_physique': [0.6, 0.2, 1, 0.4],
        'ThingType.LIVRE_EDITION_physique': [0.2, 0.3, 0.4, 1]},
        index=['ThingType.MUSEES_PATRIMOINE_ABO_physique', 'ThingType.CINEMA_ABO_physique',
               'ThingType.INSTRUMENT_physique', 'ThingType.LIVRE_EDITION_physique'])

    number_of_offer_per_type = pd.DataFrame({
        'type': 'ThingType.MUSEES_PATRIMOINE_ABO_physique',
        'total': [1]
    })

    # When
    number_of_offer_per_type_with_similarity = compute_similarity_of_each_type(number_of_offer_per_type,
                                                                               similarity_matrix)

    # Then
    assert number_of_offer_per_type_with_similarity['similarity_between_types'].values == 0


def test_compute_similarity_of_each_type_return_1point3_1_1point2_0point9_if_there_is_one_offer_per_type():
    # Given
    similarity_matrix = pd.DataFrame({
        'ThingType.LIVRE_EDITION_physique': [1, 0.51, 0.62, 0.75],
        'ThingType.MUSIQUE_physique': [0.51, 1, 0.46, 0.12],
        'ThingType.MUSEES_PATRIMOINE_ABO_physique': [0.62, 0.46, 1, 0.36],
        'ThingType.INSTRUMENT_physique': [0.75, 0.12, 0.36, 1]
        },
        index=['ThingType.LIVRE_EDITION_physique', 'ThingType.MUSIQUE_physique',
               'ThingType.MUSEES_PATRIMOINE_ABO_physique', 'ThingType.INSTRUMENT_physique'])

    number_of_offer_per_type = pd.DataFrame({
        'type': ['ThingType.LIVRE_EDITION_physique',
                 'ThingType.MUSIQUE_physique',
                 'ThingType.MUSEES_PATRIMOINE_ABO_physique',
                 'ThingType.INSTRUMENT_physique'
                 ],
        'total': [3, 2, 1, 1],
        'similarity_between_types' : [0,0,0,0]
    })

    df_it_should_return = pd.DataFrame({
        'type': ['ThingType.LIVRE_EDITION_physique',
                 'ThingType.MUSIQUE_physique',
                 'ThingType.MUSEES_PATRIMOINE_ABO_physique',
                 'ThingType.INSTRUMENT_physique'
                 ],
        'total': [3, 2, 1, 1],
        'similarity_between_types' : [4.39, 3.11, 3.14, 2.85]
    })

    # When
    number_of_offer_per_type_with_similarity = compute_similarity_of_each_type(number_of_offer_per_type,
                                                                               similarity_matrix)

    # Then
    pd.testing.assert_frame_equal(df_it_should_return, number_of_offer_per_type_with_similarity)

def test_compute_combination_of_k_among_n():
    # Given
    n = 3
    k = 2

    # When
    combination_of_k_among_n = compute_combination_of_k_among_n(k, n)

    # Then
    assert combination_of_k_among_n == 3

def test_compute_similarity_between_offers_of_same_type_when_there_is_2_livres():
    # Given
    number_of_offers_per_type = pd.DataFrame({
        'type': ['ThingType.LIVRE_EDITION', 'ThingType.MUSIQUE', 'ThingType.AUDIOVISUEL'],
        'total': [2, 0, 0]})

    # When
    similarity_between_offers_of_same_type = compute_similarity_between_offers_of_same_type(
        number_of_offers_per_type)

    # Then
    assert similarity_between_offers_of_same_type == 1

def test_compute_similarity_between_offers_of_different_types():
    # Given
    similarity_matrix = pd.DataFrame({
        'ThingType.LIVRE_EDITION': [1, 0.5, 0.6],
        'ThingType.MUSIQUE': [0.5, 1, 0.2],
        'ThingType.AUDIOVISUEL': [0.6, 0.2, 1]},
        index=['ThingType.LIVRE_EDITION', 'ThingType.MUSIQUE', 'ThingType.AUDIOVISUEL'])


    number_of_offers_per_type = pd.DataFrame({
        'type': ['ThingType.LIVRE_EDITION', 'ThingType.MUSIQUE', 'ThingType.AUDIOVISUEL'],
        'total': [1, 1, 0]})


    type1 = 'ThingType.LIVRE_EDITION'
    type2 = 'ThingType.MUSIQUE'

    # When
    similarity_between_livre_musique = compute_similarity_between_offers_of_different_types(type1, type2,
                                                                                            number_of_offers_per_type,
                                                                                            similarity_matrix)

    # Then
    assert similarity_between_livre_musique == 0.5

def test_compute_similarity_of_the_set():
    # Given
    similarity_matrix = pd.DataFrame({
        'ThingType.LIVRE_EDITION': [1, 0.5, 0.6],
        'ThingType.MUSIQUE': [0.5, 1, 0.2],
        'ThingType.AUDIOVISUEL': [0.6, 0.2, 1]},
        index=['ThingType.LIVRE_EDITION', 'ThingType.MUSIQUE', 'ThingType.AUDIOVISUEL'])


    number_of_offers_per_type = pd.DataFrame({
        'type': ['ThingType.LIVRE_EDITION', 'ThingType.MUSIQUE', 'ThingType.AUDIOVISUEL'],
        'total': [4, 2, 1]})

    number_of_exchanges = 50

    # When
    similarity_of_the_set = compute_similarity_of_the_set(number_of_offers_per_type, similarity_matrix, number_of_exchanges)

    # Then
    assert similarity_of_the_set == 13.8 / compute_combination_of_k_among_n(2, number_of_exchanges)
