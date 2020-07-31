import pandas as pd

def get_the_prediction_for_one_user(user_id, recommendable_offers_to_all_the_users, algo):

    recommendable_offers_for_one_user = recommendable_offers_to_all_the_users[recommendable_offers_to_all_the_users['user_id'] == user_id]

    offers_recommended_to_a_user = []

    for _, row in recommendable_offers_for_one_user.iterrows():
        offers_recommended_to_a_user.append(algo.predict(user_id, row.id))

    offers_recommended_to_a_user = pd.DataFrame(data=offers_recommended_to_a_user,
                                                columns=['user_id', 'offer_id', 'real_rate', 'score', 'details'])
    offers_recommended_to_a_user = offers_recommended_to_a_user.sort_values(by='score', ascending=False)


    return offers_recommended_to_a_user
