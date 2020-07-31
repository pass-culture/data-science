from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from stop_words import get_stop_words
import pandas as pd
import numpy as np


def get_cosinus_similarity_using_the_tfidf(words_used_for_tfidf):
    vectorizer = TfidfVectorizer(analyzer='word',
                                 stop_words=get_stop_words('french'),
                                 strip_accents='ascii',
                                 lowercase=True)

    tfidf_matrix = vectorizer.fit_transform(words_used_for_tfidf)

    # Linear kernel = cosine_similarity when you have a very large amount of features (linear kernel is faster)
    cosinus_similarity = linear_kernel(tfidf_matrix, tfidf_matrix)

    return cosinus_similarity


def get_the_most_similar(words_used_for_tfidf, cosinus_similarity):
    the_most_similar = {}
    for idx, ligne in words_used_for_tfidf.iterrows():
        similar_indexes = cosinus_similarity[idx].argsort()[:-12:-1]
        similar_feature = [(cosinus_similarity[idx][i], words_used_for_tfidf['rayon'][i]) for i in similar_indexes]
        the_most_similar[ligne['rayon']] = similar_feature[1:]
    return the_most_similar


def get_the_words_that_describe(df_of_the_columns_to_get_tfidf, column):
    tfidf_of_the_columns = pd.DataFrame(columns=np.arange(len(df_of_the_columns_to_get_tfidf)))

    vectorizer = TfidfVectorizer(analyzer='word',
                                 stop_words=get_stop_words('french'),
                                 strip_accents='ascii',
                                 lowercase=True)
    tfidf_matrix = vectorizer.fit_transform(df_of_the_columns_to_get_tfidf[column])

    for i, row in df_of_the_columns_to_get_tfidf.iterrows():
        tfidf_of_this_column = tfidf_matrix[i]
        # On met les tf-idf dans un dataframe
        df_tfidf = pd.DataFrame(tfidf_of_this_column.T.todense(), index=vectorizer.get_feature_names(),
                                columns=["tfidf"])
        df_tfidf = df_tfidf.sort_values(by=["tfidf"], ascending=False)
        df_tfidf = df_tfidf.head(10)
        tfidf_of_the_columns[i] = df_tfidf.index

    return tfidf_of_the_columns
