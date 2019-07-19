# coding: utf-8
import os

import pandas as pd
from sqlalchemy import create_engine
import unidecode

from statistics_dashboard import get_usage_indicators, get_departments_ranked_by_number_of_bookings, \
    get_offerer_indicators, get_offer_indicators, get_booking_indicators, \
    get_offer_indicators_by_category_and_digital, get_booking_indicators_by_category_and_digital, \
    get_finance_indicators, get_ranking_of_most_booked_offers, \
    get_ranking_of_most_booked_offerers_ordered_by_amount, get_ranking_of_most_booked_offerers_ordered_by_quantity
from test_utils import connect_to_database

PATH_TO_TEST_OUTPUT = os.environ['PATH_TO_TEST_OUTPUT']


def test_get_usage_indicators():
    # Given
    connection = connect_to_database()
    expected_table = pd.read_csv(PATH_TO_TEST_OUTPUT + 'indicateurs_utilisation.csv',
                                 index_col='Unnamed: 0')
    expected_table['Valeur'] = expected_table['Valeur'].round(decimals=2)
    expected_table['Valeur'] = expected_table['Valeur'].astype('object')

    # When
    usage_indicators_table = get_usage_indicators(connection)

    # Then
    usage_indicators_table['Valeur'] = usage_indicators_table['Valeur'].astype(float)
    usage_indicators_table['Valeur'] = usage_indicators_table['Valeur'].round(decimals=2)
    usage_indicators_table['Valeur'] = usage_indicators_table['Valeur'].astype('object')
    assert expected_table.equals(usage_indicators_table)


def test_get_departments_ranked_by_number_of_bookings():
    # Given
    connection = connect_to_database()
    expected_table = pd.read_csv(PATH_TO_TEST_OUTPUT + 'top_by_departement.csv',
                                 index_col='userDepartementCode', dtype={'Département utilisateur': 'object'})
    expected_table.reset_index(drop=True, inplace=True)
    department_list = ['29', '22', '35', '56', '34', '84', '67', '08', '93', '94', '973', '58', '71', '25']

    # When
    departments_ranking_on_bookings = get_departments_ranked_by_number_of_bookings(connection, department_list)

    # Then
    departments_ranking_on_bookings.reset_index(drop=True, inplace=True)
    assert expected_table.equals(departments_ranking_on_bookings)


def test_get_offerer_indicators():
    # Given
    connection = connect_to_database()
    expected_table = pd.read_csv(PATH_TO_TEST_OUTPUT + 'indicateurs_offreurs.csv',
                                 index_col='Unnamed: 0')

    T = '2019-07-05'
    # When
    offerers_indicators = get_offerer_indicators(connection, T)

    # Then
    assert expected_table.equals(offerers_indicators)


def test_get_offer_indicators():
    # Given
    connection = connect_to_database()
    expected_table = pd.read_csv(PATH_TO_TEST_OUTPUT + 'indicateurs_offres.csv',
                                 index_col='Unnamed: 0')

    T = '2019-07-05'
    # When
    offer_indicators = get_offer_indicators(connection, T)

    # Then
    assert expected_table.equals(offer_indicators)


def test_get_booking_indicators():
    # Given
    connection = connect_to_database()
    expected_table = pd.read_csv(PATH_TO_TEST_OUTPUT + 'indicateurs_reservations.csv',
                                 index_col='Unnamed: 0')

    # When
    booking_indicators = get_booking_indicators(connection)

    # Then
    assert expected_table.equals(booking_indicators)


def test_get_offer_indicators_by_category_and_digital():
    # Given
    connection = connect_to_database()
    expected_table = pd.read_csv(PATH_TO_TEST_OUTPUT + 'offer_by_type_and_virtual.csv',
                                 index_col='Unnamed: 0', encoding='utf-8')

    # When
    offer_indicators_by_category_and_digital_table = get_offer_indicators_by_category_and_digital(connection)

    # Then
    offer_indicators_by_category_and_digital_table['Support'] = offer_indicators_by_category_and_digital_table[
        'Support'].str.decode('utf-8', errors='ignore')

    assert expected_table.equals(offer_indicators_by_category_and_digital_table)


def test_get_booking_indicators_by_category_and_digital():
    # Given
    connection = connect_to_database()
    expected_table = pd.read_csv(PATH_TO_TEST_OUTPUT + 'booking_by_type_and_virtual.csv',
                                 index_col='Unnamed: 0', encoding='utf-8')

    # When
    booking_indicators_by_category_and_digital_table = get_booking_indicators_by_category_and_digital(connection)

    # Then

    booking_indicators_by_category_and_digital_table['Support'] = booking_indicators_by_category_and_digital_table[
        'Support'].str.decode('utf-8', errors='ignore')
    booking_indicators_by_category_and_digital_table.columns = booking_indicators_by_category_and_digital_table.columns.str.decode(
        'utf-8')
    assert expected_table.equals(booking_indicators_by_category_and_digital_table)


def test_get_finance_indicators():
    # Given
    connection = connect_to_database()
    expected_table = pd.read_csv(PATH_TO_TEST_OUTPUT + 'indicateurs_finance.csv',
                                 index_col='Unnamed: 0', encoding='utf-8')

    date = '2019-07-05'
    # When
    finance_indicators = get_finance_indicators(connection, date)
    finance_indicators['Indicateur'] = finance_indicators['Indicateur'].str.decode('utf-8')

    # Then
    assert expected_table.equals(finance_indicators)


def test_get_ranking_of_most_booked_offers():
    # Given
    connection = connect_to_database()
    expected_table = pd.read_csv(PATH_TO_TEST_OUTPUT + 'top_by_offer_quantity.csv',
                                 index_col='Unnamed: 0', encoding='utf-8')

    # When
    ranking_of_most_booked_offers = get_ranking_of_most_booked_offers(connection)

    # Then
    ranking_of_most_booked_offers.columns = ranking_of_most_booked_offers.columns.str.decode('utf-8')
    assert expected_table.equals(ranking_of_most_booked_offers)


def test_get_ranking_of_most_booked_offerers_ordered_by_quantity():
    # Given
    connection = connect_to_database()
    expected_table = pd.read_csv(PATH_TO_TEST_OUTPUT + 'top_by_offerer_quantity.csv',
                                 index_col='Unnamed: 0', encoding='utf-8')
    expected_table[u'€ dépensés'] = expected_table[u'€ dépensés'].round(decimals=2)

    # When
    ranking_of_most_booked_offerers_sorted_by_quantity = get_ranking_of_most_booked_offerers_ordered_by_quantity(
        connection)

    # Then

    ranking_of_most_booked_offerers_sorted_by_quantity.columns = ranking_of_most_booked_offerers_sorted_by_quantity.columns.str.decode(
        'utf-8')
    ranking_of_most_booked_offerers_sorted_by_quantity[u'€ dépensés'] = \
        ranking_of_most_booked_offerers_sorted_by_quantity[u'€ dépensés'].round(decimals=2)

    assert expected_table.equals(ranking_of_most_booked_offerers_sorted_by_quantity)


def test_get_ranking_of_most_booked_offerers_ordered_by_amount():
    # Given
    connection = connect_to_database()
    expected_table = pd.read_csv(PATH_TO_TEST_OUTPUT + 'top_by_offerer_amount.csv',
                                 index_col='Unnamed: 0', encoding='utf-8')
    expected_table[u'€ dépensés'] = expected_table[u'€ dépensés'].round(decimals=2)

    # When
    ranking_of_most_booked_offerers_sorted_by_amount = get_ranking_of_most_booked_offerers_ordered_by_amount(
        connection)

    # Then
    ranking_of_most_booked_offerers_sorted_by_amount.columns = ranking_of_most_booked_offerers_sorted_by_amount.columns.str.decode(
        'utf-8')
    ranking_of_most_booked_offerers_sorted_by_amount[u'€ dépensés'] = ranking_of_most_booked_offerers_sorted_by_amount[
        u'€ dépensés'].round(decimals=2)
    assert expected_table.equals(ranking_of_most_booked_offerers_sorted_by_amount)
