from passculture_recommendations.features.tfidf import get_cosinus_similarity_using_the_tfidf
from passculture_recommendations.features.tfidf import get_the_most_similar
from passculture_recommendations.features.tfidf import get_the_words_that_describe
import pandas as pd


def test_get_cosinus_similarity_using_the_tfidf():
    # Given
    words_used_for_tfidf = pd.DataFrame({'rayon': ['Spectacle de danse',
                                                   'La danse de la colère',
                                                   '5 ans magique',
                                                   'Cotisation de danse moderne Jazz']

                                         })

    # When
    cosinus_similarity = get_cosinus_similarity_using_the_tfidf(words_used_for_tfidf['rayon'])

    # Then
    assert len(cosinus_similarity) == len(words_used_for_tfidf)


def test_get_the_most_similar_rayon():
    # Given
    words_used_for_tfidf = pd.DataFrame({'rayon': ['Spectacle de danse',
                                                   'La danse de la colère',
                                                   '5 ans magique',
                                                   'Cotisation de danse moderne Jazz']

                                         })

    cosinus_similarity = get_cosinus_similarity_using_the_tfidf(words_used_for_tfidf['rayon'])

    # When
    the_most_similar = get_the_most_similar(words_used_for_tfidf, cosinus_similarity)

    # Then
    assert len(the_most_similar) == len(words_used_for_tfidf)


def test_get_the_words_that_describe_rayon():
    # Given
    df_of_the_columns_to_get_tfidf = pd.DataFrame({'rayon': ['Spectacle de danse',
                                                             'La danse de la colère',
                                                             '5 ans magique',
                                                             'Cotisation de danse moderne Jazz']

                                                   })

    # When
    tfidf_of_the_columns = get_the_words_that_describe(df_of_the_columns_to_get_tfidf, 'rayon')

    # Then
    assert len(tfidf_of_the_columns.columns) == len(df_of_the_columns_to_get_tfidf)
