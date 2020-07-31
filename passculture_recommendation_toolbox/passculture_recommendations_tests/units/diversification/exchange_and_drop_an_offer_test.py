import pandas as pd
from passculture_recommendations.diversification.exchange_and_drop_an_offer import get_the_index_of_the_offer_in_the_least_relevant_offers_that_diversifies_the_set, \
    exchange_an_offer_from_one_df_to_another, \
    drop_the_exchange_offer_from_the_least_relevant_offers

def test_get_the_index_of_the_offer_in_the_least_relevant_offers_that_diversifies_the_set():
    # Given
    least_relevant_offers_recommended_to_a_user = pd.DataFrame({'user_id': [1, 1, 1, 1, 1, 1, 1],
                                                                'offer_id': [1, 2, 3, 4, 5, 6, 7],
                                                                'type': ['ThingType.LIVRE_EDITION',
                                                                         'ThingType.MUSIQUE',
                                                                         'ThingType.INSTRUMENT',
                                                                         'ThingType.LIVRE_EDITION',
                                                                         'ThingType.LIVRE_EDITION',
                                                                         'ThingType.LIVRE_EDITION',
                                                                         'ThingType.INSTRUMENT']

                                                                })

    similarity_matrix = pd.DataFrame({
        'ThingType.LIVRE_EDITION': [1, 0.5, 0.6],
        'ThingType.MUSIQUE': [0.5, 1, 0.7],
        'ThingType.INSTRUMENT': [0.6, 0.7, 1]},
        index=['ThingType.LIVRE_EDITION', 'ThingType.MUSIQUE',
               'ThingType.INSTRUMENT'])

    number_of_offers_per_type = pd.DataFrame({'type': ['ThingType.LIVRE_EDITION',
                                                       'ThingType.MUSIQUE',
                                                       'ThingType.INSTRUMENT'],
                                              'similarity_between_types': [0.4, 0.3, 0.7]

                                              })

    type_with_the_highest_similarity = 'ThingType.INSTRUMENT'

    # When
    index_that_diversifies_the_set = get_the_index_of_the_offer_in_the_least_relevant_offers_that_diversifies_the_set(
        least_relevant_offers_recommended_to_a_user,
        similarity_matrix,
        number_of_offers_per_type,
        type_with_the_highest_similarity)

    # Then
    assert index_that_diversifies_the_set == 1


def test_exchange_an_offer_from_one_df_to_another():
    # Given
    df1 = pd.DataFrame({'user_id': [1, 2],
                        'offer_id': [11, 22]})
    df2 = pd.DataFrame({'user_id': [3, 4],
                        'offer_id': [33, 44]})
    index1 = 1
    index2 = 1

    # When
    df_with_the_exchanged_offer = exchange_an_offer_from_one_df_to_another(df1, df2, index1, index2)

    df_it_should_return = pd.DataFrame({'user_id': [1, 4],
                                        'offer_id': [11, 44]})

    # Then
    pd.testing.assert_frame_equal(df_it_should_return, df_with_the_exchanged_offer)


def test_drop_the_exchange_offer_from_the_least_relevant_offers():
    # Given
    dataframe_of_offers = pd.DataFrame({'user_id': [1, 2],
                                        'offer_id': [11, 22]})

    index_of_offer_to_drop = 1

    length_of_the_df = len(dataframe_of_offers)

    # When
    dataframe_of_offers = drop_the_exchange_offer_from_the_least_relevant_offers(dataframe_of_offers,
                                                                                 index_of_offer_to_drop)

    # Then
    assert len(dataframe_of_offers) == length_of_the_df - 1
