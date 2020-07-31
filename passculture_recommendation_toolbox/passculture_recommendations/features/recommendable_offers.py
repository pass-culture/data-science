from passculture_recommendations.data.feature_engineering import get_a_df_from_sql_query
from sqlalchemy import create_engine
engine = create_engine('postgres://pass_culture:passq@localhost:5434/pass_culture?sslmode=prefer')
connection = engine.connect()

def get_all_the_recommendable_offers():
    query = """SELECT * FROM discovery_view"""
    recommendable_offers = get_a_df_from_sql_query(query, connection)

    recommendable_digital_offers = recommendable_offers[recommendable_offers['url'].notna()]

    query = """ SELECT "user"."id" as user_id FROM "user" """
    users = get_a_df_from_sql_query(query, connection)

    recommendable_digital_offers['key'] = 1
    users['key'] = 1

    recommendable_digital_offers = recommendable_digital_offers.merge(users, on='key').drop('key', axis=1)

    recommendable_physical_offers = recommendable_offers[recommendable_offers['url'].isna()]

    query = """SELECT "id" as "venueId",  "departementCode" as offer_pc FROM "venue" """
    venue = get_a_df_from_sql_query(query, connection)

    recommendable_physical_offers = recommendable_physical_offers.merge(venue, left_on='venueId', right_on='venueId')

    query = """ SELECT "user"."id" as user_id, "departementCode" as user_pc FROM "user" """
    users_pc = get_a_df_from_sql_query(query, connection)

    nearby_departments = {
        '08': ['02', '08', '51', '55', '59'],
        '22': ['22', '29', '35', '56'],
        '25': ['21', '25', '39', '68', '70', '71', '90'],
        '29': ['22', '35', '29', '56'],
        '34': ['11', '12', '13', '30', '31', '34', '48', '66', '81', '84'],
        '35': ['22', '29', '35', '44', '49', '50', '53', '56'],
        '56': ['22', '29', '35', '44', '56'],
        '58': ['03', '18', '21', '45', '58', '71', '89'],
        '67': ['54', '55', '57', '67', '68', '88'],
        '71': ['01', '03', '21', '39', '42', '58', '69', '71'],
        '84': ['04', '07', '13', '26', '30', '83', '84'],
        '93': ['75', '77', '78', '91', '92', '93', '94', '95'],
        '94': ['75', '77', '78', '91', '92', '93', '94', '95'],
        '97': ['97', '971', '972', '973'],
        '973': ['97', '971', '972', '973'],
    }

    keys = []
    values = []
    for key, value_list in nearby_departments.items():
        keys += [key] * len(value_list)
        values += value_list
    nearby_departments = pd.DataFrame({'user_pc': keys, 'offer_pc': values})

    recommendable_physical_offers = recommendable_physical_offers.merge(nearby_departments, left_on='offer_pc', right_on='offer_pc')
    recommendable_physical_offers = recommendable_physical_offers.merge(users_pc, left_on='user_pc', right_on='user_pc')

    recommendable_offers_to_all_the_users = pd.concat([recommendable_physical_offers, recommendable_digital_offers], sort=False)

    return recommendable_offers_to_all_the_users

def get_all_the_recommendable_offers_from_bretagne(recommendable_offers_to_all_the_users):
    bretagne = ['22', '29', '35', '56']
    recommendable_offers_to_all_the_users_in_bretagne = recommendable_offers_to_all_the_users[recommendable_offers_to_all_the_users['offer_pc'].isin(bretagne)]

    return recommendable_offers_to_all_the_users_in_bretagne
