from passculture_recommendations.features.number_of_offer_per_category import compute_number_of_offer_per_category
from passculture_recommendations.diversification.similarity_using_the_confusion_matrix import compute_similarity_of_each_type
from passculture_recommendations.diversification.exchange_and_drop_an_offer import \
    get_the_index_of_the_offer_in_the_least_relevant_offers_that_diversifies_the_set, \
    exchange_an_offer_from_one_df_to_another, \
    drop_the_exchange_offer_from_the_least_relevant_offers

def add_one_offer_that_diversifies_the_recommended_offers(most_relevant_offers_recommended_to_a_user,
                                                          least_relevant_offers_recommended_to_a_user,
                                                          similarity_matrix):
    number_of_offers_per_type = compute_number_of_offer_per_category(most_relevant_offers_recommended_to_a_user, 'type',
                                                                     'total')

    similarity_of_each_type = compute_similarity_of_each_type(number_of_offers_per_type, similarity_matrix)

    type_with_the_highest_similarity = similarity_of_each_type.loc[
        similarity_of_each_type['similarity_between_types'] == similarity_of_each_type[
            'similarity_between_types'].max(), 'type'].values[0]

    type_with_the_highest_similarity = str(type_with_the_highest_similarity)

    index_of_the_offer_to_exchange_in_the_most_relevant_offers = most_relevant_offers_recommended_to_a_user[
        most_relevant_offers_recommended_to_a_user['type'] == type_with_the_highest_similarity].index[0]

    index_of_the_offer_to_exchange_in_the_least_relevant_offers = get_the_index_of_the_offer_in_the_least_relevant_offers_that_diversifies_the_set(
        least_relevant_offers_recommended_to_a_user, similarity_matrix,
        number_of_offers_per_type, type_with_the_highest_similarity)

    most_relevant_offers_recommended_to_a_user = exchange_an_offer_from_one_df_to_another(
        most_relevant_offers_recommended_to_a_user,
        least_relevant_offers_recommended_to_a_user,
        index_of_the_offer_to_exchange_in_the_most_relevant_offers,
        index_of_the_offer_to_exchange_in_the_least_relevant_offers)

    least_relevant_offers_recommended_to_a_user = drop_the_exchange_offer_from_the_least_relevant_offers(
        least_relevant_offers_recommended_to_a_user, index_of_the_offer_to_exchange_in_the_least_relevant_offers)

    return most_relevant_offers_recommended_to_a_user, least_relevant_offers_recommended_to_a_user, number_of_offers_per_type
