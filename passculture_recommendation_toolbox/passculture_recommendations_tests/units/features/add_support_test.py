import pandas as pd
import numpy as np
from passculture_recommendations.data.add_support import add_support_in_type

def test_add_support_in_type():
    # Given
    df_of_offers_with_column_type_to_add_support = pd.DataFrame(
        {'type' : ['ThingType.LIVRE', 'EventType.MUSIQUE', 'ThingType.AUDIOVISUEL'], 'url' : [None, 'url1', 'url2']})

    df_of_offers_with_column_type_with_support = pd.DataFrame(
        {'type': ['ThingType.LIVRE_physique', 'EventType.MUSIQUE_numerique', 'ThingType.AUDIOVISUEL_numerique'], 'url': [np.nan, 'url1', 'url2']})

    # When
    df_of_offers_with_column_type_to_add_support = add_support_in_type(df_of_offers_with_column_type_to_add_support)

    # Then
    pd.testing.assert_frame_equal(df_of_offers_with_column_type_to_add_support, df_of_offers_with_column_type_with_support)

