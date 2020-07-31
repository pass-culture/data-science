import pandas as pd
from passculture_recommendations.data.functions_over_the_types import create_dataframe_of_the_name_of_all_the_types
from passculture_recommendations.data.functions_over_the_types import replace_dot_with_a_dash_in_the_column_type

def test_create_dataframe_of_all_the_types():
    # Given
    df_with_different_types = pd.DataFrame({'type' : ['ThingType.MUSIQUE',
                                                      'ThingType.MUSEES_PATRIMOINE_ABO',
                                                      'ThingType.MUSEES_PATRIMOINE_ABO',
                                                      'ThingType.MUSEES_PATRIMOINE_ABO',
                                                      'ThingType.MUSIQUE',
                                                      'ThingType.LIVRE_EDITION']})

    # When
    name_of_all_the_types = create_dataframe_of_the_name_of_all_the_types(df_with_different_types)

    # Then
    assert len(name_of_all_the_types) == 3

def test_replace_dot_with_a_dash_in_the_column_type():
    # Given
    df_with_different_types = pd.DataFrame({'type': ['ThingType.MUSIQUE',
                                                     'ThingType.MUSEES_PATRIMOINE_ABO',
                                                     'ThingType.MUSEES_PATRIMOINE_ABO',
                                                     'ThingType.MUSEES_PATRIMOINE_ABO',
                                                     'ThingType.MUSIQUE',
                                                     'ThingType.LIVRE_EDITION']})

    df_it_should_return = pd.DataFrame({'type': ['ThingType_MUSIQUE',
                                                 'ThingType_MUSEES_PATRIMOINE_ABO',
                                                 'ThingType_MUSEES_PATRIMOINE_ABO',
                                                 'ThingType_MUSEES_PATRIMOINE_ABO',
                                                 'ThingType_MUSIQUE',
                                                 'ThingType_LIVRE_EDITION']})

    # When
    dot_in_types_changed_by_dash = replace_dot_with_a_dash_in_the_column_type(df_with_different_types)

    # Then
    pd.testing.assert_frame_equal(df_it_should_return, dot_in_types_changed_by_dash)
