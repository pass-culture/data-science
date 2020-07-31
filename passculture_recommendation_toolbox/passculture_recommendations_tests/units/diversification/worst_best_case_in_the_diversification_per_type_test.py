from passculture_recommendations.diversification.worst_best_case_in_the_diversification_per_type import \
    worst_case_in_the_diversification_per_type, \
    best_case_in_the_diversification_per_type
import pandas as pd


def test_worst_case_in_the_diversification_per_type():
    # Given
    number_of_offers_recommended = 50

    # When
    similarity_of_the_set_in_the_worst_case = worst_case_in_the_diversification_per_type(number_of_offers_recommended)

    # Then
    assert similarity_of_the_set_in_the_worst_case == 1.


def test_best_case_in_the_diversification_per_type():
    # Given
    most_relevant_offers_recommended_to_a_user = pd.DataFrame({'user_id': [1, 1, 1, 1, 1, 1, 1],
                                                               'offer_id': [1, 2, 3, 4, 5, 6, 7],
                                                               'type': ['ThingType.LIVRE',
                                                                        'ThingType.CINEMA',
                                                                        'ThingType.AUDIOVISUEL',
                                                                        'ThingType.CINEMA',
                                                                        'ThingType.LIVRE',
                                                                        'ThingType.LIVRE',
                                                                        'ThingType.MUSIQUE']

                                                               })

    similarity_matrix = pd.DataFrame({'ThingType.MUSIQUE': [1, 0.5, 0.2, 0.3],
                                      'ThingType.AUDIOVISUEL': [0.5, 1, 0.4, 0.6],
                                      'ThingType.CINEMA': [0.2, 0.4, 1, 0.9],
                                      'ThingType.LIVRE': [0.3, 0.6, 0.9, 1],
                                      },
                                     index=['ThingType.MUSIQUE', 'ThingType.AUDIOVISUEL', 'ThingType.CINEMA',
                                            'ThingType.LIVRE'])

    # When
    list_of_similarities = best_case_in_the_diversification_per_type(most_relevant_offers_recommended_to_a_user, 50,
                                                                     similarity_matrix)

    # Then
    assert len(list_of_similarities) == 1000
