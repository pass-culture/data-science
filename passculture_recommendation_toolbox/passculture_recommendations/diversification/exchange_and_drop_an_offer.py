def get_the_index_of_the_offer_in_the_least_relevant_offers_that_diversifies_the_set \
        (least_relevant_offers_recommended_to_a_user, similarity_matrix,
         number_of_offers_per_type, type_with_the_highest_similarity):
    for index_of_the_offer_that_diversifies_the_set in least_relevant_offers_recommended_to_a_user.index:
        type_of_the_offer = \
        least_relevant_offers_recommended_to_a_user.loc[index_of_the_offer_that_diversifies_the_set]['type']

        type_of_the_offer = str(type_of_the_offer)

        similarity_of_the_offer = number_of_offers_per_type.loc[number_of_offers_per_type['type'] == type_of_the_offer, \
                                                                'similarity_between_types'].values
        similarity_of_the_offer = similarity_of_the_offer + 1  # because we add this type to the list of recommendation
        similarity_of_the_offer = similarity_of_the_offer - similarity_matrix.loc[
            type_of_the_offer, type_with_the_highest_similarity]  # because we delete the type that we exchange
        if similarity_of_the_offer < number_of_offers_per_type['similarity_between_types'].max():
            break

    return index_of_the_offer_that_diversifies_the_set


def exchange_an_offer_from_one_df_to_another(df1, df2, index1, index2):
    df1.loc[index1] = df2.loc[index2]
    return df1


def drop_the_exchange_offer_from_the_least_relevant_offers(dataframe_of_offers, index_of_offer_to_drop):
    dataframe_of_offers.drop(index_of_offer_to_drop, axis=0, inplace=True)
    return dataframe_of_offers
