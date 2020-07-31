import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgres://pass_culture:passq@localhost:5434/pass_culture?sslmode=prefer')
connection = engine.connect()


def get_a_df_from_sql_query(query, connection):
    df = pd.read_sql_query(query, connection)
    return df


def get_user_offer_interaction_and_put_a_grade(sql_query, grade, connection):
    interaction_of_the_user = pd.read_sql_query(sql_query, connection)
    interaction_of_the_user['note'] = grade
    return interaction_of_the_user


def get_dataframe_of_all_the_interactions_from_0_to_5():
    query_for_offers_reserved_by_the_user = """SELECT booking."userId" as user_id, stock."offerId" as offer_id, type, "isVirtual"
               FROM booking
               LEFT JOIN stock ON booking."stockId" = stock.id
               LEFT JOIN offer ON stock."offerId"=offer."id"
               LEFT JOIN venue ON offer."venueId"=venue."id"
               WHERE booking."isUsed"=True AND booking."isCancelled"=False
               AND offer.type!='EventType.ACTIVATION' AND offer.type != 'ThingType.ACTIVATION'
            """
    grade_for_offers_reserved_by_the_user = 5

    offers_reserved_by_the_user = get_user_offer_interaction_and_put_a_grade(query_for_offers_reserved_by_the_user,
                                                                             grade_for_offers_reserved_by_the_user,
                                                                             connection)
    query_for_offers_reserved_by_the_user_but_not_consumed = """SELECT booking."userId" as user_id, stock."offerId" as offer_id, type, "isVirtual"
               FROM  booking
               LEFT JOIN stock ON booking."stockId" = stock.id
               LEFT JOIN offer ON stock."offerId"=offer."id"
               LEFT JOIN venue ON offer."venueId"=venue."id"
               WHERE booking."isUsed"=False AND booking."isCancelled"=False
               AND offer.type!='EventType.ACTIVATION' AND offer.type != 'ThingType.ACTIVATION'
            """
    grade_for_offers_reserved_by_the_user_but_not_consumed = 4

    offers_reserved_by_the_user_but_not_consumed = get_user_offer_interaction_and_put_a_grade(
        query_for_offers_reserved_by_the_user_but_not_consumed,
        grade_for_offers_reserved_by_the_user_but_not_consumed,
        connection)

    query_for_offers_reserved_by_the_user_but_canceled = """SELECT booking."userId" as user_id, stock."offerId" as offer_id, type, "isVirtual"
               FROM booking
               LEFT JOIN stock ON booking."stockId" = stock.id
               LEFT JOIN offer ON stock."offerId"=offer."id"
               LEFT JOIN venue ON offer."venueId"=venue."id"
               WHERE booking."isUsed"=False AND booking."isCancelled"=True
               AND offer.type!='EventType.ACTIVATION' AND offer.type != 'ThingType.ACTIVATION'
            """
    grade_for_offers_reserved_by_the_user_but_canceled = 3

    offers_reserved_by_the_user_but_canceled = get_user_offer_interaction_and_put_a_grade(
        query_for_offers_reserved_by_the_user_but_canceled,
        grade_for_offers_reserved_by_the_user_but_canceled,
        connection)

    query_for_offers_favored_by_the_user = """SELECT favorite."userId" as user_id, favorite."offerId" as offer_id, type, "isVirtual"
               FROM favorite
               LEFT JOIN "user" ON favorite."userId" = "user"."id"
               LEFT JOIN offer ON favorite."offerId"=offer."id"
               LEFT JOIN venue ON offer."venueId"=venue."id"
               WHERE "user"."canBookFreeOffers" = True
               AND offer.type!='EventType.ACTIVATION' AND offer.type != 'ThingType.ACTIVATION'
            """
    grade_for_offers_favored_by_the_user = 2

    offers_favored_by_the_user = get_user_offer_interaction_and_put_a_grade(query_for_offers_favored_by_the_user,
                                                                            grade_for_offers_favored_by_the_user,
                                                                            connection)

    query_for_offers_clicked_by_the_user = """SELECT "userId" as user_id, offer."id" as offer_id, type, "isVirtual"
               FROM recommendation
               LEFT JOIN "user" ON recommendation."userId" = "user"."id"
               LEFT JOIN offer ON recommendation."offerId" = offer."id"
               LEFT JOIN venue ON offer."venueId"=venue."id"
               WHERE recommendation."search" IS NULL
               AND recommendation."dateRead" IS NOT NULL
               AND offer."id" IS NOT NULL
               AND "isClicked"='True'
               AND "user"."canBookFreeOffers" = True
               AND offer.type!='EventType.ACTIVATION' AND offer.type!='ThingType.ACTIVATION'
            """
    grade_for_offers_clicked_by_the_user = 1

    offers_clicked_by_the_user = get_user_offer_interaction_and_put_a_grade(query_for_offers_clicked_by_the_user,
                                                                            grade_for_offers_clicked_by_the_user,
                                                                            connection)

    query_for_offers_ignored_by_the_user = """SELECT "userId" as user_id, "offerId" as offer_id, type, "isVirtual"
               FROM recommendation
               LEFT JOIN "user" ON recommendation."userId" = "user"."id"
               LEFT JOIN offer ON recommendation."offerId" = offer."id"
               LEFT JOIN venue ON offer."venueId"=venue."id"
               WHERE recommendation."search" IS NULL
               AND recommendation."dateRead" IS NOT NULL
               AND "offerId" IS NOT NULL
               AND "isClicked"='False'
               AND "user"."canBookFreeOffers" = True
               AND offer.type!='EventType.ACTIVATION' AND offer.type != 'ThingType.ACTIVATION'
            """
    grade_for_offers_ignored_by_the_user = 0

    offers_ignored_by_the_user = get_user_offer_interaction_and_put_a_grade(query_for_offers_ignored_by_the_user,
                                                                            grade_for_offers_ignored_by_the_user,
                                                                            connection)

    offers_graded_from_0_to_5 = pd.concat([offers_reserved_by_the_user,
                                           offers_reserved_by_the_user_but_not_consumed,
                                           offers_reserved_by_the_user_but_canceled,
                                           offers_favored_by_the_user,
                                           offers_clicked_by_the_user,
                                           offers_ignored_by_the_user])
    offers_graded_from_0_to_5 = offers_graded_from_0_to_5.sort_values('note', ascending=True).drop_duplicates(subset=['user_id','offer_id'], keep='last')

    return offers_graded_from_0_to_5


def get_offers_that_interest_and_dont_interest_the_users(offers_graded_from_0_to_5):
    offers_graded_from_0_to_1 = offers_graded_from_0_to_5
    offers_graded_from_0_to_1['note'] = offers_graded_from_0_to_1['note'].apply(lambda x: 0 if x == 1 or x == 0 else 1)
    return offers_graded_from_0_to_1
