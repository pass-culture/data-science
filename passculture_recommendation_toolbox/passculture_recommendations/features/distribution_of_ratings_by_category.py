from passculture_recommendations.data.number_of_offer_per_category import compute_number_of_offer_per_category


def distribution_of_ratings(df_with_user_offer_rate_category, category):
    number_of_rates_per_category = compute_number_of_offer_per_category(df_with_user_offer_rate_category, category, 'total')

    number_of_rate_0_per_type = compute_number_of_offer_per_category(
        df_with_user_offer_rate_category[df_with_user_offer_rate_category['note'] == 0], category, 'total_note0')
    number_of_rate_1_per_type = compute_number_of_offer_per_category(
        df_with_user_offer_rate_category[df_with_user_offer_rate_category['note'] == 1], category, 'total_note1')

    number_of_rates_per_category = number_of_rates_per_category.merge(number_of_rate_0_per_type, left_on=category, right_on=category, how='outer')
    number_of_rates_per_category = number_of_rates_per_category.merge(number_of_rate_1_per_type, left_on=category, right_on=category, how='outer')

    number_of_rates_per_category['pourcentage_note0'] = number_of_rates_per_category['total_note0'] * 100 / number_of_rates_per_category['total']
    number_of_rates_per_category['pourcentage_note1'] = number_of_rates_per_category['total_note1'] * 100 / number_of_rates_per_category['total']

    return number_of_rates_per_category
