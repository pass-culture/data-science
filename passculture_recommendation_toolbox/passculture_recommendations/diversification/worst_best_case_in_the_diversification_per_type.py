from passculture_recommendations.data.functions_over_the_types import create_dataframe_of_the_name_of_all_the_types
from passculture_recommendations.data.number_of_offer_per_category import compute_number_of_offer_per_category
from passculture_recommendations.diversification.similarity_using_the_confusion_matrix import compute_similarity_of_the_set
import pandas as pd
import math
from random import choices
from random import shuffle


def worst_case_in_the_diversification_per_type(number_of_offers_recommended):
    worst_case = pd.DataFrame({'type': 'ThingType.LIVRE_EDITION_physique',
                               'total': [number_of_offers_recommended]})
    similarity_of_the_set_in_the_worst_case = 0
    for types in worst_case['type']:
        if worst_case.loc[worst_case['type'] == types, 'total'].values == 1:
            similarity_of_the_set_in_the_worst_case += 0
        else:
            n = worst_case.loc[worst_case['type'] == types, 'total'].values
            k = 2
            Cnk = math.factorial(n) / (math.factorial(k) * math.factorial(n - k))
            similarity_of_the_set_in_the_worst_case += Cnk
            similarity_of_the_set_in_the_worst_case = similarity_of_the_set_in_the_worst_case / Cnk
    return similarity_of_the_set_in_the_worst_case

def best_case_in_the_diversification_per_type(most_relevant_offers_recommended_to_a_user, number_of_offers_recommended, similarity_matrix):
    group_of_types = create_dataframe_of_the_name_of_all_the_types(most_relevant_offers_recommended_to_a_user)
    group_of_types = list(group_of_types['type'])
    list_of_similarities_in_the_best_case = []
    for i in range(1000):
        random_types = choices(group_of_types, k=number_of_offers_recommended)
        dataframe_of_random_types = pd.DataFrame(random_types, columns=['type'])
        number_of_offers_per_type = compute_number_of_offer_per_category(dataframe_of_random_types, 'type', 'total')
        list_of_similarities_in_the_best_case.append(compute_similarity_of_the_set(number_of_offers_per_type, similarity_matrix, number_of_offers_recommended)[0])
        shuffle(random_types)
    return list_of_similarities_in_the_best_case
