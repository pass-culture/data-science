from passculture_recommendations.data.add_support import add_support_in_type
from passculture_recommendations.data.functions_over_the_types import create_dataframe_of_the_name_of_all_the_types, \
    replace_dot_with_a_dash_in_the_column_type
from passculture_recommendations.diversification.similarity_using_the_tfidf_of_the_description import compute_similarity_for_each_offer, \
    get_index_in_the_df_of_the_offer_with_the_highest_similarity, \
    get_column_index_of_the_offer_with_the_highest_similarity, \
    get_index_to_exchange_in_the_least_relevant_offers, \
    compute_similarity_of_the_set
from passculture_recommendations.diversification.exchange_and_drop_an_offer import exchange_an_offer_from_one_df_to_another, \
    drop_the_exchange_offer_from_the_least_relevant_offers
from passculture_recommendations.data.number_of_offer_per_category import compute_number_of_offer_per_category


def add_x_offers_that_diversifies_the_recommended_offers_using_the_description(offers_recommended_to_a_user,
                                                                               cosinus_similarity):
    K = int(len(offers_recommended_to_a_user) / 2)
    N = len(offers_recommended_to_a_user)

    print(1)
    offers_recommended_to_a_user = add_support_in_type(offers_recommended_to_a_user)
    print(offers_recommended_to_a_user)
    offers_recommended_to_a_user['index'] = offers_recommended_to_a_user.index
    most_relevant_offers_recommended_to_a_user = offers_recommended_to_a_user[0:K]
    least_relevant_offers_recommended_to_a_user = offers_recommended_to_a_user[K + 1:N]

    sum_of_the_score = []
    similarity_of_the_set = []

    number_of_offers_per_type = create_dataframe_of_the_name_of_all_the_types(offers_recommended_to_a_user)
    number_of_offers_per_type = replace_dot_with_a_dash_in_the_column_type(number_of_offers_per_type)

    number_of_exchanges = K

    for i in range(0, number_of_exchanges):
        sum_of_the_score.append(sum(most_relevant_offers_recommended_to_a_user['score']) / K)

        most_relevant_offers_recommended_to_a_user = compute_similarity_for_each_offer(
            most_relevant_offers_recommended_to_a_user, cosinus_similarity)

        real_index_of_the_offer_with_the_highest_similarity = get_column_index_of_the_offer_with_the_highest_similarity(
            most_relevant_offers_recommended_to_a_user)

        index_of_the_offer_with_the_highest_similarity = get_index_in_the_df_of_the_offer_with_the_highest_similarity(
            most_relevant_offers_recommended_to_a_user)

        index_to_exchange_in_the_least_relevant_offers = get_index_to_exchange_in_the_least_relevant_offers(
            least_relevant_offers_recommended_to_a_user, most_relevant_offers_recommended_to_a_user,
            real_index_of_the_offer_with_the_highest_similarity[0], index_of_the_offer_with_the_highest_similarity,
            cosinus_similarity)

        if index_to_exchange_in_the_least_relevant_offers is not None:
            most_relevant_offers_recommended_to_a_user = exchange_an_offer_from_one_df_to_another(
                most_relevant_offers_recommended_to_a_user, least_relevant_offers_recommended_to_a_user,
                index_of_the_offer_with_the_highest_similarity, index_to_exchange_in_the_least_relevant_offers)
            least_relevant_offers_recommended_to_a_user = drop_the_exchange_offer_from_the_least_relevant_offers(
                least_relevant_offers_recommended_to_a_user, index_to_exchange_in_the_least_relevant_offers)
            similarity_of_the_set.append(
                compute_similarity_of_the_set(most_relevant_offers_recommended_to_a_user, cosinus_similarity, number_of_exchanges))
            number_of_offers_per_type_for_this_iteration = compute_number_of_offer_per_category(
                most_relevant_offers_recommended_to_a_user, 'type', i)
            number_of_offers_per_type_for_this_iteration = replace_dot_with_a_dash_in_the_column_type(
                number_of_offers_per_type_for_this_iteration)
            number_of_offers_per_type = number_of_offers_per_type.merge(number_of_offers_per_type_for_this_iteration,
                                                                        how='outer', left_on='type', right_on='type')

    return most_relevant_offers_recommended_to_a_user, number_of_offers_per_type, sum_of_the_score, similarity_of_the_set

