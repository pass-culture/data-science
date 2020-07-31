import pandas as pd

from passculture_recommendations.features.number_of_offer_per_category import compute_number_of_offer_per_category


def test_return_number_of_offer_per_type():
    # Given
    offers = pd.DataFrame({
        'user_id': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        'offer_id': [657082, 15925, 31768, 552808, 543, 5675, 43456, 46448, 43234, 54324],
        'type': ['ThingType.MUSEES_PATRIMOINE_ABO_physique', 'ThingType.CINEMA_ABO_physique',
                 'ThingType.INSTRUMENT_physique',
                 'ThingType.LIVRE_EDITION_physique', 'ThingType.MUSEES_PATRIMOINE_ABO_physique',
                 'ThingType.LIVRE_EDITION_physique',
                 'ThingType.LIVRE_EDITION_physique', 'ThingType.LIVRE_EDITION_physique',
                 'ThingType.MUSEES_PATRIMOINE_ABO_physique', 'ThingType.INSTRUMENT_physique']
    })

    dataframe_of_what_it_should_return = pd.DataFrame({
        'type': ['ThingType.LIVRE_EDITION_physique',
                 'ThingType.MUSEES_PATRIMOINE_ABO_physique',
                 'ThingType.INSTRUMENT_physique',
                 'ThingType.CINEMA_ABO_physique'],
        'total': [4, 3, 2, 1],
    })

    # When
    number_of_offer_per_type = compute_number_of_offer_per_category(offers, 'type', 'total')

    # Then
    pd.testing.assert_frame_equal(dataframe_of_what_it_should_return, number_of_offer_per_type)


def test_return_number_of_offer_per_column_isVirtual():
    # Given
    offers = pd.DataFrame({
        'user_id': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        'offer_id': [657082, 15925, 31768, 552808, 543, 5675, 43456, 46448, 43234, 54324],
        'isVirtual': ['False', 'True', 'True', 'False', 'True', 'True', 'False', 'True', 'True', 'True']
    })

    dataframe_of_what_it_should_return = pd.DataFrame({
        'isVirtual': ['True', 'False'],
        'total': [7, 3]
    })

    # When
    number_of_offer_per_column_isVirtual = compute_number_of_offer_per_category(offers, 'isVirtual', 'total')

    # Then
    pd.testing.assert_frame_equal(dataframe_of_what_it_should_return, number_of_offer_per_column_isVirtual)
