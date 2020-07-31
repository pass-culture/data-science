from passculture_recommendations.diversification.algorithm_swap_using_the_confusion_matrix import add_one_offer_that_diversifies_the_recommended_offers

import pandas as pd


def test_add_one_offer_that_diversifies_the_recommended_offers():
    # Given
    most_relevant_offers_recommended_to_a_user = pd.DataFrame({'user_id': [1, 1, 1, 1, 1, 1],
                                                               'offer_id': [1, 2, 3, 4, 5, 6],
                                                               'type': ['ThingType.MUSIQUE',
                                                                        'ThingType.MUSIQUE',
                                                                        'ThingType.INSTRUMENT',
                                                                        'ThingType.CINEMA',
                                                                        'ThingType.CINEMA',
                                                                        'ThingType.MUSIQUE']
                                                               })

    least_relevant_offers_recommended_to_a_user = pd.DataFrame({'user_id': [1, 1, 1, 1],
                                                                'offer_id': [7, 8, 9, 10],
                                                                'type': ['ThingType.MUSIQUE',
                                                                         'ThingType.INSTRUMENT',
                                                                         'ThingType.CINEMA',
                                                                         'ThingType.MUSIQUE']
                                                                })

    similarity_matrix = pd.DataFrame({'ThingType.MUSIQUE': [1, 0.5, 0.2],
                                      'ThingType.INSTRUMENT': [0.5, 1, 0.4],
                                      'ThingType.CINEMA': [0.2, 0.4, 1],
                                      },
                                     index=['ThingType.MUSIQUE', 'ThingType.INSTRUMENT', 'ThingType.CINEMA'])

    # When
    most_relevant_offers_recommended_to_a_user, least_relevant_offers_recommended_to_a_user, number_of_offers_per_type = add_one_offer_that_diversifies_the_recommended_offers(
        most_relevant_offers_recommended_to_a_user,
        least_relevant_offers_recommended_to_a_user,
        similarity_matrix)

    it_should_exchange_the_offer_of_type_instrument_with_musique = pd.DataFrame({'user_id': [1, 1, 1, 1, 1, 1],
                                                                                 'offer_id': [8, 2, 3, 4, 5, 6],
                                                                                 'type': ['ThingType.INSTRUMENT',
                                                                                          'ThingType.MUSIQUE',
                                                                                          'ThingType.INSTRUMENT',
                                                                                          'ThingType.CINEMA',
                                                                                          'ThingType.CINEMA',
                                                                                          'ThingType.MUSIQUE']
                                                                                 })
    # Then
    pd.testing.assert_frame_equal(most_relevant_offers_recommended_to_a_user,
                                  it_should_exchange_the_offer_of_type_instrument_with_musique)


def test_drop_the_offer_that_diversifies_in_the_least_recommended_offers():
    # Given
    most_relevant_offers_recommended_to_a_user = pd.DataFrame({'user_id': [1, 1, 1, 1, 1, 1],
                                                               'offer_id': [1, 2, 3, 4, 5, 6],
                                                               'type': ['ThingType.MUSIQUE',
                                                                        'ThingType.MUSIQUE',
                                                                        'ThingType.INSTRUMENT',
                                                                        'ThingType.CINEMA',
                                                                        'ThingType.CINEMA',
                                                                        'ThingType.MUSIQUE']
                                                               })

    least_relevant_offers_recommended_to_a_user = pd.DataFrame({'user_id': [1, 1, 1, 1],
                                                                'offer_id': [7, 8, 9, 10],
                                                                'type': ['ThingType.MUSIQUE',
                                                                         'ThingType.INSTRUMENT',
                                                                         'ThingType.CINEMA',
                                                                         'ThingType.MUSIQUE']
                                                                })

    similarity_matrix = pd.DataFrame({'ThingType.MUSIQUE': [1, 0.5, 0.2],
                                      'ThingType.INSTRUMENT': [0.5, 1, 0.4],
                                      'ThingType.CINEMA': [0.2, 0.4, 1],
                                      },
                                     index=['ThingType.MUSIQUE', 'ThingType.INSTRUMENT', 'ThingType.CINEMA'])

    # When
    most_relevant_offers_recommended_to_a_user, least_relevant_offers_recommended_to_a_user, number_of_offers_per_type = add_one_offer_that_diversifies_the_recommended_offers(
        most_relevant_offers_recommended_to_a_user,
        least_relevant_offers_recommended_to_a_user,
        similarity_matrix)

    it_should_drop_the_offer_of_type_musique = pd.DataFrame({'user_id': [1, 1, 1],
                                                             'offer_id': [7, 9, 10],
                                                             'type': ['ThingType.MUSIQUE',
                                                                      'ThingType.CINEMA',
                                                                      'ThingType.MUSIQUE']
                                                             }, index=[0, 2, 3])

    # Then
    pd.testing.assert_frame_equal(least_relevant_offers_recommended_to_a_user, it_should_drop_the_offer_of_type_musique)


def test_compute_number_of_offer_per_type_with_their_similarity():
    # Given
    most_relevant_offers_recommended_to_a_user = pd.DataFrame({'user_id': [1, 1, 1, 1, 1, 1],
                                                               'offer_id': [1, 2, 3, 4, 5, 6],
                                                               'type': ['ThingType.MUSIQUE',
                                                                        'ThingType.MUSIQUE',
                                                                        'ThingType.INSTRUMENT',
                                                                        'ThingType.CINEMA',
                                                                        'ThingType.CINEMA',
                                                                        'ThingType.MUSIQUE']
                                                               })

    least_relevant_offers_recommended_to_a_user = pd.DataFrame({'user_id': [1, 1, 1, 1],
                                                                'offer_id': [7, 8, 9, 10],
                                                                'type': ['ThingType.MUSIQUE',
                                                                         'ThingType.INSTRUMENT',
                                                                         'ThingType.CINEMA',
                                                                         'ThingType.MUSIQUE']
                                                                })

    similarity_matrix = pd.DataFrame({'ThingType.MUSIQUE': [1, 0.5, 0.2],
                                      'ThingType.INSTRUMENT': [0.5, 1, 0.4],
                                      'ThingType.CINEMA': [0.2, 0.4, 1],
                                      },
                                     index=['ThingType.MUSIQUE', 'ThingType.INSTRUMENT', 'ThingType.CINEMA'])

    # When
    most_relevant_offers_recommended_to_a_user, least_relevant_offers_recommended_to_a_user, number_of_offers_per_type = add_one_offer_that_diversifies_the_recommended_offers(
        most_relevant_offers_recommended_to_a_user,
        least_relevant_offers_recommended_to_a_user,
        similarity_matrix)

    it_should_compute_number_of_offer_and_their_similarity = pd.DataFrame(
        {'type': ['ThingType.MUSIQUE', 'ThingType.CINEMA', 'ThingType.INSTRUMENT'],
         'total': [3, 2, 1],
         'similarity_between_types': [2.9, 2, 2.3]
         })

    # Then
    print(number_of_offers_per_type)
    pd.testing.assert_frame_equal(number_of_offers_per_type, it_should_compute_number_of_offer_and_their_similarity)
