from passculture_recommendations.diversification.algorithm_swap_using_the_description import \
    add_x_offers_that_diversifies_the_recommended_offers_using_the_description
import pandas as pd
import numpy as np


def test_add_x_offers_that_diversifies_the_recommended_offers_using_the_description():
    # Given
    offers_recommended_to_a_user = pd.DataFrame({'user_id': [1, 1, 1, 1, 1, 1],
                                                 'offer_id': [1, 2, 3, 4, 5, 6],
                                                 'type': ['ThingType.LIVRE',
                                                          'ThingType.MUSIQUE',
                                                          'ThingType.LIVRE',
                                                          'ThingType.LIVRE',
                                                          'ThingType.MUSIQUE',
                                                          'ThingType.INSTRUMENT'],
                                                 'url': [np.nan,
                                                         'abc.com',
                                                         np.nan,
                                                         np.nan,
                                                         np.nan,
                                                         'abcd.com'],
                                                 'score': [0., 0.1, 0.2, 0.1, 0.3, 0.4]
                                                 })

    cosinus_similarity = np.array([[1., 0.2, 0.3, 0.9, 0.6, 0.3],
                                   [0.2, 1., 0.8, 0.7, 0.4, 0.3],
                                   [0.3, 0.8, 1., 0.4, 0.8, 0.1],
                                   [0.9, 0.7, 0.4, 1., 0.4, 0.2],
                                   [0.6, 0.4, 0.8, 0.4, 1., 0.3],
                                   [0.3, 0.3, 0.1, 0.2, 0.3, 1.]])

    # When
    most_relevant_offers_recommended_to_a_user_with_diversification, number_of_offers_per_type, sum_of_the_score, similarity_of_the_set = add_x_offers_that_diversifies_the_recommended_offers_using_the_description(
        3, offers_recommended_to_a_user, cosinus_similarity)

    # Then
    df_it_should_return = pd.DataFrame({'user_id': [1, 1, 1],
                                        'offer_id': [1, 2, 6],
                                        'type': ['ThingType.LIVRE',
                                                 'ThingType.MUSIQUE',
                                                 'ThingType.INSTRUMENT'],
                                        'url': [np.nan,
                                                'abc.com',
                                                'abcd.com'],
                                        'score': [0., 0.1, 0.4],
                                        'index': [0, 1, 5],
                                        'similarite': [0.25, 0.25, 0.40]
                                        })
    print(most_relevant_offers_recommended_to_a_user_with_diversification)
    pd.testing.assert_frame_equal(df_it_should_return, most_relevant_offers_recommended_to_a_user_with_diversification)
