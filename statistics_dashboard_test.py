# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
import unidecode

from statistics_dashboard import create_usage_indicators, create_departments_ranked_by_number_of_bookings, \
    create_offerer_indicators, create_offer_indicators, create_booking_indicators, \
    create_offer_indicators_by_category_and_digital, create_booking_indicators_by_category_and_digital, \
    create_finance_indicators, create_ranking_of_most_booked_offers, \
    create_ranking_of_most_booked_offerers_ordered_by_amount, create_ranking_of_most_booked_offerers_ordered_by_quantity


def skip_test_create_usage_indicators():
    # Given
    engine = create_engine('postgres://pass_culture:passq@localhost:5432')
    connection = engine.connect()
    expected_table = pd.read_csv('/Users/louiseanfray/passculture/csv_from_jupyter/indicateurs_utilisation.csv',
                                 index_col='Unnamed: 0')
    expected_table['Valeur'] = expected_table['Valeur'].round(decimals=2)
    expected_table['Valeur'] = expected_table['Valeur'].astype('object')

    # When
    usage_indicators_table = create_usage_indicators(connection)

    # Then
    usage_indicators_table['Valeur'] = usage_indicators_table['Valeur'].astype(float)
    usage_indicators_table['Valeur'] = usage_indicators_table['Valeur'].round(decimals=2)
    usage_indicators_table['Valeur'] = usage_indicators_table['Valeur'].astype('object')
    assert expected_table.equals(usage_indicators_table)


def skip_test_create_departments_ranked_by_number_of_bookings():
    # Given
    engine = create_engine('postgres://pass_culture:passq@localhost:5432')
    connection = engine.connect()
    expected_table = pd.read_csv('/Users/louiseanfray/passculture/csv_from_jupyter/top_by_departement.csv',
                                 index_col='userDepartementCode', dtype={'Département utilisateur': 'object'})
    expected_table.reset_index(drop=True, inplace=True)
    department_list = ['29', '22', '35', '56', '34', '84', '67', '08', '93', '94', '973', '58', '71', '25']

    # When
    departments_ranking_on_bookings = create_departments_ranked_by_number_of_bookings(connection, department_list)

    # Then
    departments_ranking_on_bookings.reset_index(drop=True, inplace=True)
    assert expected_table.equals(departments_ranking_on_bookings)


def skip_test_create_offerer_indicators():
    # Given
    engine = create_engine('postgres://pass_culture:passq@localhost:5432')
    connection = engine.connect()
    expected_table = pd.read_csv('/Users/louiseanfray/passculture/csv_from_jupyter/indicateurs_offreurs.csv',
                                 index_col='Unnamed: 0')

    T = '2019-07-05'
    # When
    offerers_indicators = create_offerer_indicators(connection, T)

    # Then
    assert expected_table.equals(offerers_indicators)


def skip_test_create_offer_indicators():
    # Given
    engine = create_engine('postgres://pass_culture:passq@localhost:5432')
    connection = engine.connect()
    expected_table = pd.read_csv('/Users/louiseanfray/passculture/csv_from_jupyter/indicateurs_offres.csv',
                                 index_col='Unnamed: 0')

    T = '2019-07-05'
    # When
    offer_indicators = create_offer_indicators(connection, T)

    # Then
    print(expected_table)
    print(offer_indicators)
    assert expected_table.equals(offer_indicators)


def skip_test_create_booking_indicators():
    # Given
    engine = create_engine('postgres://pass_culture:passq@localhost:5432')
    connection = engine.connect()
    expected_table = pd.read_csv('/Users/louiseanfray/passculture/csv_from_jupyter/indicateurs_reservations.csv',
                                 index_col='Unnamed: 0')

    # When
    booking_indicators = create_booking_indicators(connection)

    # Then
    assert expected_table.equals(booking_indicators)


def skip_test_create_offer_indicators_by_category_and_digital():
    # Given
    engine = create_engine('postgres://pass_culture:passq@localhost:5432')
    connection = engine.connect()
    expected_table = pd.read_csv('/Users/louiseanfray/passculture/csv_from_jupyter/offer_by_type_and_virtual.csv',
                                 index_col='Unnamed: 0', encoding='utf-8')

    # When
    offer_indicators_by_category_and_digital_table = create_offer_indicators_by_category_and_digital(connection)

    # Then
    offer_indicators_by_category_and_digital_table['Support'] = offer_indicators_by_category_and_digital_table[
        'Support'].str.decode('utf-8', errors='ignore')

    assert expected_table.equals(offer_indicators_by_category_and_digital_table)


def skip_test_create_booking_indicators_by_category_and_digital():
    # Given
    engine = create_engine('postgres://pass_culture:passq@localhost:5432')
    connection = engine.connect()
    expected_table = pd.read_csv('/Users/louiseanfray/passculture/csv_from_jupyter/booking_by_type_and_virtual.csv',
                                 index_col='Unnamed: 0', encoding='utf-8')

    # When
    booking_indicators_by_category_and_digital_table = create_booking_indicators_by_category_and_digital(connection)

    # Then

    booking_indicators_by_category_and_digital_table['Support'] = booking_indicators_by_category_and_digital_table[
        'Support'].str.decode('utf-8', errors='ignore')
    booking_indicators_by_category_and_digital_table.columns = booking_indicators_by_category_and_digital_table.columns.str.decode(
        'utf-8')
    assert expected_table.equals(booking_indicators_by_category_and_digital_table)


def skip_test_create_finance_indicators():
    # Given
    engine = create_engine('postgres://pass_culture:passq@localhost:5432')
    connection = engine.connect()
    expected_table = pd.read_csv('/Users/louiseanfray/passculture/csv_from_jupyter/indicateurs_finance.csv',
                                 index_col='Unnamed: 0', encoding='utf-8')

    date = '2019-07-05'
    # When
    finance_indicators = create_finance_indicators(connection, date)
    finance_indicators['Indicateur'] = finance_indicators['Indicateur'].str.decode('utf-8')

    # Then
    assert expected_table.equals(finance_indicators)


def skip_test_create_ranking_of_most_booked_offers():
    # Given
    engine = create_engine('postgres://pass_culture:passq@localhost:5432')
    connection = engine.connect()
    expected_table = pd.read_csv('/Users/louiseanfray/passculture/csv_from_jupyter/top_by_offer_quantity.csv',
                                 index_col='Unnamed: 0', encoding='utf-8')

    # When
    ranking_of_most_booked_offers = create_ranking_of_most_booked_offers(connection)

    # Then
    ranking_of_most_booked_offers.columns = ranking_of_most_booked_offers.columns.str.decode('utf-8')
    assert expected_table.equals(ranking_of_most_booked_offers)


def skip_test_create_ranking_of_most_booked_offerers_ordered_by_quantity():
    # Given
    engine = create_engine('postgres://pass_culture:passq@localhost:5432')
    connection = engine.connect()
    expected_table = pd.read_csv('/Users/louiseanfray/passculture/csv_from_jupyter/top_by_offerer_quantity.csv',
                                 index_col='Unnamed: 0', encoding='utf-8')
    expected_table[u'€ dépensés'] = expected_table[u'€ dépensés'].round(decimals=2)

    # When
    ranking_of_most_booked_offerers_sorted_by_quantity = create_ranking_of_most_booked_offerers_ordered_by_quantity(
        connection)

    # Then

    ranking_of_most_booked_offerers_sorted_by_quantity.columns = ranking_of_most_booked_offerers_sorted_by_quantity.columns.str.decode(
        'utf-8')
    ranking_of_most_booked_offerers_sorted_by_quantity[u'€ dépensés'] = \
        ranking_of_most_booked_offerers_sorted_by_quantity[u'€ dépensés'].round(decimals=2)

    assert expected_table.equals(ranking_of_most_booked_offerers_sorted_by_quantity)


def skip_test_create_ranking_of_most_booked_offerers_ordered_by_amount():
    # Given
    engine = create_engine('postgres://pass_culture:passq@localhost:5432')
    connection = engine.connect()
    expected_table = pd.read_csv('/Users/louiseanfray/passculture/csv_from_jupyter/top_by_offerer_amount.csv',
                                 index_col='Unnamed: 0', encoding='utf-8')
    expected_table[u'€ dépensés'] = expected_table[u'€ dépensés'].round(decimals=2)

    # When
    ranking_of_most_booked_offerers_sorted_by_amount = create_ranking_of_most_booked_offerers_ordered_by_amount(
        connection)

    # Then
    ranking_of_most_booked_offerers_sorted_by_amount.columns = ranking_of_most_booked_offerers_sorted_by_amount.columns.str.decode(
        'utf-8')
    ranking_of_most_booked_offerers_sorted_by_amount[u'€ dépensés'] = ranking_of_most_booked_offerers_sorted_by_amount[
        u'€ dépensés'].round(decimals=2)
    assert expected_table.equals(ranking_of_most_booked_offerers_sorted_by_amount)


def skip_test_create_usage_indicators_for_department_29():
    # Given
    engine = create_engine('postgres://pass_culture:passq@localhost:5432')
    connection = engine.connect()
    expected_table = pd.read_csv('/Users/louiseanfray/passculture/csv_from_jupyter/indicateurs_utilisation_29.csv',
                                 index_col='Unnamed: 0')
    expected_table['Valeur'] = expected_table['Valeur'].round(decimals=2)
    expected_table['Valeur'] = expected_table['Valeur'].astype('object')

    # When
    usage_indicators_table_29 = create_usage_indicators(connection, department='29')

    # Then
    usage_indicators_table_29['Valeur'] = usage_indicators_table_29['Valeur'].astype(float)
    usage_indicators_table_29['Valeur'] = usage_indicators_table_29['Valeur'].round(decimals=2)
    usage_indicators_table_29['Valeur'] = usage_indicators_table_29['Valeur'].astype('object')
    print(expected_table)
    print(usage_indicators_table_29)
    assert expected_table.equals(usage_indicators_table_29)


def test_create_ranking_of_most_booked_offerers_ordered_by_quantity_29():
    # Given
    engine = create_engine('postgres://pass_culture:passq@localhost:5432')
    connection = engine.connect()
    expected_table = pd.read_csv('/Users/louiseanfray/passculture/csv_from_jupyter/top_by_offerer_quantity_29.csv',
                                 index_col='Unnamed: 0', encoding='utf-8')
    expected_table[u'€ dépensés'] = expected_table[u'€ dépensés'].round(decimals=2)
    expected_table.reset_index(drop=True, inplace=True)

    # When
    ranking_of_most_booked_offerers_sorted_by_quantity_29 = create_ranking_of_most_booked_offerers_ordered_by_quantity(
        connection, department='29')

    # Then

    ranking_of_most_booked_offerers_sorted_by_quantity_29.columns = ranking_of_most_booked_offerers_sorted_by_quantity_29.columns.str.decode(
        'utf-8')
    ranking_of_most_booked_offerers_sorted_by_quantity_29[u'€ dépensés'] = \
        ranking_of_most_booked_offerers_sorted_by_quantity_29[u'€ dépensés'].round(decimals=2)
    ranking_of_most_booked_offerers_sorted_by_quantity_29.reset_index(drop=True, inplace=True)
    print(expected_table.eq(ranking_of_most_booked_offerers_sorted_by_quantity_29))
    assert expected_table.equals(ranking_of_most_booked_offerers_sorted_by_quantity_29)

