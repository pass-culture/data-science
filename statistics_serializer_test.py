import os

import pandas as pd
from sqlalchemy import create_engine

PATH_TO_TEST_OUTPUT = os.environ['PATH_TO_TEST_OUTPUT']

from statistics_serializer import get_beneficiary_users_having_created_an_account_table, \
    get_valid_offerer_table, \
    get_valid_venue_table, get_real_booking_after_ministerial_decree_table, get_stock_table, \
    get_offer_with_stocks_and_valid_venue_table, \
    get_correspondance_table_between_offer_venue_and_offerer, \
    get_correspondance_table_betwwen_booking_stock_and_offer, \
    get_venues_to_repay_table, get_booking_to_repay_table


def test_create_beneficiary_users_having_created_an_account_table():
    # Given
    engine = create_engine('postgres://data:data@localhost:5432/pass-culture')
    connection = engine.connect()
    expected_table = pd.read_csv(PATH_TO_TEST_OUTPUT + 'activationxp.csv',
                                 index_col='Unnamed: 0', dtype={'departementCode': 'object'})
    expected_table['dateCreated'] = pd.to_datetime(expected_table['dateCreated'])

    # When
    activation_table = get_beneficiary_users_having_created_an_account_table(connection)

    # Then
    assert expected_table.equals(activation_table)


def test_create_valid_offerer_table():
    # Given
    engine = create_engine('postgres://data:data@localhost:5432/pass-culture')
    connection = engine.connect()
    expected_table = pd.read_csv(PATH_TO_TEST_OUTPUT + 'offererxp.csv',
                                 index_col='Unnamed: 0', dtype={'siren': 'object', 'offerer_postalCode': 'object'},
                                 encoding='utf-8')

    # When
    offerer_table = get_valid_offerer_table(connection)

    # Then
    assert expected_table.equals(offerer_table)


def test_create_valid_venue_table():
    # Given
    engine = create_engine('postgres://data:data@localhost:5432/pass-culture')
    connection = engine.connect()
    expected_table = pd.read_csv(PATH_TO_TEST_OUTPUT + 'venuexp.csv',
                                 index_col='Unnamed: 0', dtype={'siret': 'object', 'venue_postalCode': 'object'},
                                 encoding='utf-8')

    # When
    venue_table = get_valid_venue_table(connection)

    # Then
    assert expected_table.equals(venue_table)


def test_create_real_booking_after_ministerial_decree_table():
    # Given
    engine = create_engine('postgres://data:data@localhost:5432/pass-culture')
    connection = engine.connect()
    expected_table = pd.read_csv(PATH_TO_TEST_OUTPUT + 'bookingxp.csv',
                                 index_col='Unnamed: 0',
                                 dtype={'userDepartementCode': 'object'},
                                 encoding='utf-8')
    expected_table['dateCreated'] = pd.to_datetime(expected_table['dateCreated'])

    # When
    booking_table = get_real_booking_after_ministerial_decree_table(connection)

    # Then
    assert expected_table.equals(booking_table)


def test_create_stock_table():
    # Given
    engine = create_engine('postgres://data:data@localhost:5432/pass-culture')
    connection = engine.connect()
    expected_table = pd.read_csv(PATH_TO_TEST_OUTPUT + 'stockxp.csv',
                                 index_col='Unnamed: 0',
                                 dtype={},
                                 encoding='utf-8')
    expected_table['bookingLimitDatetime'] = pd.to_datetime(expected_table['bookingLimitDatetime'])
    expected_table['endDatetime'] = pd.to_datetime(expected_table['endDatetime'])

    # When
    stock_table = get_stock_table(connection)

    # Then
    assert expected_table.equals(stock_table)


def test_create_offer_with_stocks_and_valid_venue_table():
    # Given
    engine = create_engine('postgres://data:data@localhost:5432/pass-culture')
    connection = engine.connect()
    expected_table = pd.read_csv(PATH_TO_TEST_OUTPUT + 'offerxp.csv',
                                 index_col='Unnamed: 0',
                                 dtype={},
                                 encoding='utf-8')
    expected_table = expected_table.fillna('')
    ordered_expected_table = expected_table.sort_values(by='offerId')
    ordered_expected_table.reset_index(inplace=True, drop=True)

    # When
    offer_table = get_offer_with_stocks_and_valid_venue_table(connection)

    # Then
    ordered_offer_table = offer_table.sort_values(by='offerId')
    ordered_offer_table.reset_index(inplace=True, drop=True)
    assert ordered_expected_table.equals(ordered_offer_table)


def test_create_correspondance_table_between_offer_venue_and_offerer():
    # Given
    engine = create_engine('postgres://data:data@localhost:5432/pass-culture')
    connection = engine.connect()
    expected_table = pd.read_csv(PATH_TO_TEST_OUTPUT + 'data_offer_ID.csv',
                                 index_col='Unnamed: 0',
                                 dtype={},
                                 encoding='utf-8')
    ordered_expected_table = expected_table.sort_values(by=['managingOffererId', 'venueId', 'offerId'])
    ordered_expected_table.reset_index(inplace=True, drop=True)

    # When
    correspondance_table = get_correspondance_table_between_offer_venue_and_offerer(connection)

    # Then
    ordered_correspondance_table = correspondance_table.sort_values(by=['managingOffererId', 'venueId', 'offerId'])
    ordered_correspondance_table.reset_index(inplace=True, drop=True)

    assert ordered_expected_table.equals(ordered_correspondance_table)


def test_create_correspondance_table_betwwen_booking_stock_and_offer():
    # Given
    engine = create_engine('postgres://data:data@localhost:5432/pass-culture')
    connection = engine.connect()
    expected_table = pd.read_csv(PATH_TO_TEST_OUTPUT + 'data_booking_ID.csv',
                                 index_col='Unnamed: 0',
                                 dtype={},
                                 encoding='utf-8')

    # When
    data_booking_ID_table = get_correspondance_table_betwwen_booking_stock_and_offer(connection)

    # Then
    assert expected_table.equals(data_booking_ID_table)


def test_create_booking_to_repay_table():
    # Given
    engine = create_engine('postgres://data:data@localhost:5432/pass-culture')
    connection = engine.connect()
    expected_table = pd.read_csv(PATH_TO_TEST_OUTPUT + 'booking_eligible.csv',
                                 index_col='Unnamed: 0',
                                 dtype={'siret': 'object', 'venue_postalCode': 'object'},
                                 encoding='utf-8')

    expected_table = expected_table.fillna('')
    expected_table.reset_index(inplace=True, drop=True)
    reference_date_to_consider_who_is_eligible_to_be_paid = '2019-07-05'

    # When
    booking_to_repay_table = get_booking_to_repay_table(connection, reference_date_to_consider_who_is_eligible_to_be_paid)

    # Then
    booking_to_repay_table.reset_index(inplace=True, drop=True)
    assert expected_table.equals(booking_to_repay_table)


def test_create_venues_to_repay_table():
    # Given
    engine = create_engine('postgres://data:data@localhost:5432/pass-culture')
    connection = engine.connect()
    expected_table = pd.read_csv(PATH_TO_TEST_OUTPUT + 'venue_eligible_calculation.csv',
                                 index_col='Unnamed: 0',
                                 dtype={'siret': 'object', 'venue_postalCode': 'object'},
                                 encoding='utf-8')

    expected_table = expected_table.fillna('')
    expected_table[
        ['amount_net', 'amount_net_paid', 'amount_really_used', 'amount_really_used_paid']] = expected_table[
        ['amount_net', 'amount_net_paid', 'amount_really_used', 'amount_really_used_paid']].round(
        decimals=2)
    pd.set_option('display.max_columns', None)
    reference_date_to_consider_who_is_eligible_to_be_paid = '2019-07-05'

    # When
    venues_to_repay = get_venues_to_repay_table(connection, reference_date_to_consider_who_is_eligible_to_be_paid)

    # Then
    venues_to_repay[
        ['amount_net', 'amount_net_paid', 'amount_really_used', 'amount_really_used_paid']] = \
        venues_to_repay[
            ['amount_net', 'amount_net_paid', 'amount_really_used', 'amount_really_used_paid']].round(
            decimals=2)

    assert expected_table.equals(venues_to_repay)
