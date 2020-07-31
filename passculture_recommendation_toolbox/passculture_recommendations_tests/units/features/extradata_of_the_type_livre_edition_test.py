from passculture_recommendations.data.extradata_of_the_type_livre_edition import get_feature_of_the_book, \
    add_columns_of_the_features_in_df_extradata_livre
import pandas as pd


def test_get_feature_of_the_book():
    # Given
    extradata_livres = pd.DataFrame({'offer_id': [1, 2, 3],
                                     'extraData': [{'author': 'Jacques', 'isbn': '1234'},
                                                   {'author': 'Pierre', 'prix_livre': '9.99'},
                                                   {'author': 'Paul', 'rayon': 'Littérature Romans Poche'}]

                                     })

    # When
    feature_of_the_book = get_feature_of_the_book(extradata_livres)

    # Then
    feature_of_the_book_it_should_return = ['author', 'isbn', 'prix_livre', 'rayon']
    assert feature_of_the_book == feature_of_the_book_it_should_return


def test_add_columns__of_the_features_in_df_extradata_livre():
    # Given
    extradata_livres = pd.DataFrame({'offer_id': [1, 2, 3],
                                     'extraData': [{'author': 'Jacques', 'isbn': '1234'},
                                                   {'author': 'Pierre', 'prix_livre': '9.99'},
                                                   {'author': 'Paul', 'rayon': 'Littérature Romans Poche'}]

                                     })

    feature_of_the_book = ['author', 'isbn', 'prix_livre', 'rayon']

    # When
    extradata_livres = add_columns_of_the_features_in_df_extradata_livre(extradata_livres, feature_of_the_book)

    # Then
    columns_it_should_return = ['offer_id', 'extraData', 'author', 'isbn', 'prix_livre', 'rayon']
    assert list(extradata_livres.columns) == columns_it_should_return
