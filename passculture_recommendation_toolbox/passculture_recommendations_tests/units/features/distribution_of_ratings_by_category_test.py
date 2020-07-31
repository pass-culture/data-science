from passculture_recommendations.data.distribution_of_ratings_by_category import distribution_of_ratings
import pandas as pd

def test_should_return_df_with_column_type_total_totalnote0_total_note1_pctgnote0_pctgnote1():
    # Given
    offers = pd.DataFrame({'user' : [1,1,2,2,3],
                           'offer' : [32,34,54,43,43],
                           'note' : [0,1,1,0,0],
                           'type' : ['ThingType.LIVRE_EDITION',
                                     'ThingType.LIVRE_EDITION',
                                     'ThingType.MUSIQUE',
                                     'ThingType.AUDIOVISUEL',
                                     'ThingType.INSTRUMENT']
                          })
    columns_it_should_return = ['type', 'total', 'total_note0', 'total_note1', 'pourcentage_note0', 'pourcentage_note1']

    # When
    number_of_rates_per_category = distribution_of_ratings(offers, 'type')

    # Then
    assert list(number_of_rates_per_category.columns) == columns_it_should_return
