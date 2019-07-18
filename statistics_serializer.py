# coding: utf-8
import pandas as pd
from repository import get_activation_stock_id, get_users, get_bookings, get_user_offerers, get_offerers, get_venues, \
    get_stocks, get_offers

MINISTERIAL_DECREE_DATE = '2019-02-04'


def get_beneficiary_users_having_created_an_account_table(connection, department=None):
    bookings = get_bookings(connection)
    users = get_users(connection)
    activation_stock_id = get_activation_stock_id(connection)

    is_activation_booking = (bookings['stockId'] == activation_stock_id)
    is_after_ministerial_decree = (bookings['dateCreated'] >= MINISTERIAL_DECREE_DATE)
    booking_columns_to_keep = ['userId', 'dateCreated']
    activation_bookings_after_ministerial_decree = bookings.loc[
        is_activation_booking & is_after_ministerial_decree, booking_columns_to_keep]
    user_columns_to_keep = ['id', 'departementCode', 'canBookFreeOffers']
    users_having_created_an_account = pd.merge(activation_bookings_after_ministerial_decree,
                                               users[user_columns_to_keep],
                                               how='inner', left_on='userId', right_on='id')
    del (users_having_created_an_account['id'])
    if department:
        return users_having_created_an_account.loc[users_having_created_an_account['departementCode'] == department]
    return users_having_created_an_account


def get_valid_offerer_table(connection):
    offerers = get_offerers(connection)
    user_offerers = get_user_offerers(connection)
    offerers_with_siren = offerers[offerers['siren'].notnull()]
    offerers_columns_to_keep = ['id', 'name', 'siren', 'address', 'postalCode', 'city']
    offerers_with_siren = offerers_with_siren[offerers_columns_to_keep]

    offerers_with_siren_and_user_offerer = pd.merge(user_offerers[['offererId']], offerers_with_siren, how='inner',
                                                    left_on='offererId', right_on='id',
                                                    left_index=True, sort=False)
    del (offerers_with_siren_and_user_offerer['offererId'])
    offerers_with_siren_and_user_offerer = offerers_with_siren_and_user_offerer.drop_duplicates()
    offerers_column_names_equivalences = {'id': 'offererId', 'name': 'offerer_name', 'address': 'offerer_address',
                                          'postalCode': 'offerer_postalCode', 'city': 'offerer_city'}
    offerers_with_siren_and_user_offerer.rename(columns=offerers_column_names_equivalences,
                                                inplace=True)
    return offerers_with_siren_and_user_offerer


def get_valid_venue_table(connection, department=None):
    venues = get_venues(connection)
    valid_offerers = get_valid_offerer_table(connection)
    venues = venues[['id', 'name', 'isVirtual', 'siret', 'address', 'postalCode', 'city', 'managingOffererId']]

    venues_with_valid_offerer = pd.merge(valid_offerers[['offererId']], venues, how='inner', left_on='offererId',
                                         right_on='managingOffererId',
                                         left_index=True, sort=False)
    del (venues_with_valid_offerer['offererId'])
    venues_with_valid_offerer = venues_with_valid_offerer.drop_duplicates()
    venues_column_names_equivalences = {'id': 'venueId', 'name': 'venue_name', 'address': 'venue_address',
                                        'postalCode': 'venue_postalCode'}
    venues_with_valid_offerer = venues_with_valid_offerer.rename(
        columns=venues_column_names_equivalences)
    if department:
        return venues_with_valid_offerer.loc[venues_with_valid_offerer['venue_postalCode'].str.startswith(department)]
    return venues_with_valid_offerer


def get_real_booking_after_ministerial_decree_table(connection, department=None):
    activation_stock_id = get_activation_stock_id(connection)

    bookings = get_bookings(connection)
    beneficiary_users = get_beneficiary_users_having_created_an_account_table(connection)
    bookings_with_user_information = _merge_bookings_with_beneficiary_users(beneficiary_users, bookings)

    real_bookings_after_ministerial_decree = _filter_real_bookings_and_users(
        bookings_with_user_information, activation_stock_id)
    if department:
        return venues_with_valid_offerer.loc[venues_with_valid_offerer['venue_postalCode'].str.startswith(department)]
    return venues_with_valid_offerer


    del (real_bookings_after_ministerial_decree['isUsed'])
    del (real_bookings_after_ministerial_decree['isCancelled'])

    real_bookings_after_ministerial_decree = real_bookings_after_ministerial_decree.rename(
        columns={'id': 'bookingId'})
    if department:
        return real_bookings_after_ministerial_decree.loc[
            real_bookings_after_ministerial_decree['userDepartementCode'] == department]
    return real_bookings_after_ministerial_decree


def get_stock_table(connection):
    stocks = get_stocks(connection)
    real_bookings_after_ministerial_decree = get_real_booking_after_ministerial_decree_table(connection)
    stocks.rename(columns={'id': 'stockId'}, inplace=True)

    stocks_with_stock_available = _add_stock_available(real_bookings_after_ministerial_decree, stocks)

    stock_columns_to_keep = ['stockId', 'offerId', 'price', 'available',
                             'stock_available', 'bookingLimitDatetime', 'endDatetime']
    stocks_with_stock_available = stocks_with_stock_available[stock_columns_to_keep]
    return stocks_with_stock_available


def get_offer_with_stocks_and_valid_venue_table(connection, department=None):
    offers = get_offers(connection)
    stocks = get_stock_table(connection)
    valid_venues = get_valid_venue_table(connection)


    offers_with_stocks_and_valid_venue = _keep_only_offers_with_stock_and_valid_venues(offers, stocks, valid_venues)

    offer_columns_to_keep = ['id', 'venueId', 'name', 'type']
    offers_with_stocks_and_valid_venue = offers_with_stocks_and_valid_venue[offer_columns_to_keep]
    offers_with_stocks_and_valid_venue.rename(columns={'id': 'offerId'}, inplace=True)

    offers_with_human_category = _add_human_category(offers_with_stocks_and_valid_venue)

    return offers_with_human_category


def get_correspondance_table_between_offer_venue_and_offerer(connection):
    valid_venues = get_valid_venue_table(connection)
    offers_with_stocks_and_valid_venue = get_offer_with_stocks_and_valid_venue_table(connection)

    venues_with_offerer_id = valid_venues[['venueId', 'managingOffererId']]
    offers_with_venue_id = offers_with_stocks_and_valid_venue[['offerId', 'venueId']]

    offers_with_venue_id_and_offerer_id = pd.merge(venues_with_offerer_id, offers_with_venue_id, how='outer',
                                                   left_on='venueId',
                                                   right_on='venueId', left_index=True, sort=False)
    offers_with_venue_id_and_offerer_id = offers_with_venue_id_and_offerer_id[
        ['offerId', 'venueId', 'managingOffererId']]
    return offers_with_venue_id_and_offerer_id


def get_correspondance_table_betwwen_booking_stock_and_offer(connection):
    real_bookings_after_ministerial_decree = get_real_booking_after_ministerial_decree_table(connection)
    stocks = get_stock_table(connection)
    bookings_with_stock_id = real_bookings_after_ministerial_decree[['bookingId', 'stockId']]
    stocks_with_offer_id = stocks[['stockId', 'offerId']]

    bookings_with_stock_id_and_offer_id = pd.merge(bookings_with_stock_id, stocks_with_offer_id, how='outer',
                                                   left_on='stockId',
                                                   right_on='stockId', left_index=True, sort=False)
    bookings_with_stock_id_and_offer_id = bookings_with_stock_id_and_offer_id[['bookingId', 'stockId', 'offerId']]
    return bookings_with_stock_id_and_offer_id


def get_booking_to_repay_table(connection, date):
    offers_with_stocks_and_valid_venue = get_offer_with_stocks_and_valid_venue_table(connection)
    valid_venues = get_valid_venue_table(connection)
    stocks = get_stock_table(connection)
    real_bookings_after_ministerial_decree = get_real_booking_after_ministerial_decree_table(connection)
    correspondance_table_between_booking_stock_and_offer = get_correspondance_table_betwwen_booking_stock_and_offer(
        connection)

    correspondance_table_between_booking_and_offer = correspondance_table_between_booking_stock_and_offer[
        ['bookingId', 'offerId']]

    offer_with_digital_information = _format_offer_and_add_digital_information(
        offers_with_stocks_and_valid_venue, valid_venues)

    bookings_with_type_and_digital_information = _add_offer_information_to_booking(
        correspondance_table_between_booking_and_offer,
        offer_with_digital_information,
        real_bookings_after_ministerial_decree)

    bookings_with_type_digital_and_date_information = _add_stock_information_to_booking(
        bookings_with_type_and_digital_information, stocks)

    bookings_with_type_digital_and_date_information = _add_quantity_and_amount_really_used_to_booking(
        bookings_with_type_digital_and_date_information, date)

    bookings_to_repay = _filter_booking_eligible_to_repayment(bookings_with_type_digital_and_date_information)
    eligible_booking_columns_to_keep = ['bookingId', 'quantity_really_used', 'quantity_net', 'amount_really_used',
                                        'amount_net', 'venueId']
    bookings_to_repay = bookings_to_repay[eligible_booking_columns_to_keep]
    return bookings_to_repay


def get_venues_to_repay_table(connection, date):
    bookings_to_repay = get_booking_to_repay_table(connection, date)
    valid_venues = get_valid_venue_table(connection)

    bookings_to_repay = bookings_to_repay.groupby(['venueId']).sum().reset_index()

    venues_to_repay = pd.merge(valid_venues, bookings_to_repay, how='inner', left_on='venueId', right_on='venueId',
                               left_index=True,
                               sort=False)

    venues_to_repay = _add_amount_net_paid_and_amount_really_used_paid(venues_to_repay)

    venues_to_repay = _format_venue(venues_to_repay)
    return venues_to_repay


def _merge_bookings_with_beneficiary_users(beneficiary_users, bookings):
    booking_columns_to_keep = ['id', 'dateCreated', 'stockId', 'quantity', 'amount', 'isCancelled', 'isUsed', 'userId']
    bookings = bookings[booking_columns_to_keep]
    bookings.rename(columns={'id': 'bookingId'}, inplace=True)
    user_columns_to_keep = ['userId', 'departementCode']
    beneficiary_users = beneficiary_users[user_columns_to_keep]
    bookings_with_user_information = pd.merge(bookings, beneficiary_users, how='inner', left_on='userId',
                                              right_on='userId', left_index=True, sort=False)
    bookings_with_user_information.rename(columns={'departementCode': 'userDepartementCode'}, inplace=True)
    return bookings_with_user_information


def _filter_real_bookings_and_users(bookings_with_user_information, activation_stock_id):
    user_department_code_is_not_null = bookings_with_user_information['userDepartementCode'].notnull()
    global_department_code = '00'
    user_has_non_global_department_code = (
            bookings_with_user_information['userDepartementCode'] != global_department_code)
    bookings_with_user_information = bookings_with_user_information.loc[
        user_department_code_is_not_null & user_has_non_global_department_code]
    bookings_on_non_activation_offer_with_user_information = bookings_with_user_information.loc[
        (bookings_with_user_information['stockId'] != activation_stock_id)]
    real_bookings_with_user_information_after_ministerial_decree = \
    bookings_on_non_activation_offer_with_user_information.loc[
        bookings_on_non_activation_offer_with_user_information['dateCreated'] > MINISTERIAL_DECREE_DATE]
    real_bookings_with_user_information_after_ministerial_decree = _add_quantity_and_amount_information_to_booking(
        real_bookings_with_user_information_after_ministerial_decree)
    return real_bookings_with_user_information_after_ministerial_decree


def _add_quantity_and_amount_information_to_booking(bookings):
    bookings_with_quantity_and_amount = bookings.copy()
    bookings_with_quantity_and_amount['quantity_used'] = bookings_with_quantity_and_amount['quantity'] * \
                                                         bookings_with_quantity_and_amount['isUsed']
    bookings_with_quantity_and_amount['amount_used'] = bookings_with_quantity_and_amount['amount'] * \
                                                       bookings_with_quantity_and_amount['isUsed']
    bookings_with_quantity_and_amount['quantity_cancelled'] = bookings_with_quantity_and_amount['quantity'] * \
                                                              bookings_with_quantity_and_amount['isCancelled']
    bookings_with_quantity_and_amount['amount_cancelled'] = bookings_with_quantity_and_amount['amount'] * \
                                                            bookings_with_quantity_and_amount['isCancelled']
    bookings_with_quantity_and_amount['quantity_net'] = bookings_with_quantity_and_amount['quantity'] - \
                                                        bookings_with_quantity_and_amount['quantity_cancelled']
    bookings_with_quantity_and_amount['amount_net'] = bookings_with_quantity_and_amount['amount'] - \
                                                      bookings_with_quantity_and_amount['amount_cancelled']
    return bookings_with_quantity_and_amount


def _add_stock_available(real_bookings_after_ministerial_decree, stocks):
    bookings_per_stock = real_bookings_after_ministerial_decree[['stockId', 'quantity_net']].groupby(
        ['stockId']).sum().reset_index()
    stocks = pd.merge(stocks, bookings_per_stock, how='left', left_on='stockId', right_on='stockId',
                      left_index=True,
                      sort=False)
    stocks['stock_available'] = stocks['available'] - \
                                stocks['quantity_net']
    del (stocks['quantity_net'])
    return stocks


def _keep_only_offers_with_stock_and_valid_venues(offers, stocks, valid_venues):
    ids_of_offers_with_stocks = stocks.offerId.unique()
    offers_with_stocks = offers.loc[offers.id.isin(ids_of_offers_with_stocks)]
    ids_of_valid_venues = valid_venues['venueId'].unique()
    offers_with_stocks_and_valid_venues = offers_with_stocks.loc[
        offers_with_stocks['venueId'].isin(ids_of_valid_venues)]
    return offers_with_stocks_and_valid_venues


def _add_human_category(offers):
    type_correspondance_path = 'helpers_data/type_correspondance.csv'
    type_correspondance = pd.read_csv(type_correspondance_path, sep=';', encoding='utf-8')
    offers_with_human_category = pd.merge(type_correspondance, offers,
                                          how='inner', left_on='type', right_on='type')
    return offers_with_human_category


def _format_offer_and_add_digital_information(offers, venues):
    offer_columns_to_keep = ['venueId', 'offerId', 'type', 'name']
    offers_with_digital_information = offers[offer_columns_to_keep]
    offers_with_digital_information = offers_with_digital_information.fillna('Autre')
    offers_with_digital_information = pd.merge(offers_with_digital_information, venues[['venueId', 'isVirtual']],
                                               how='left',
                                               left_on='venueId',
                                               right_on='venueId', left_index=True, sort=False)
    return offers_with_digital_information


def _filter_booking_eligible_to_repayment(bookings):
    is_eligible_to_repayment = (bookings['type'] == 'ThingType.LIVRE_EDITION') | (bookings['isVirtual'] == False)
    bookings_to_repay = bookings[is_eligible_to_repayment]
    return bookings_to_repay


def _add_quantity_and_amount_really_used_to_booking(bookings, date):
    ids_of_bookings_on_automatically_validated_events = _get_booking_ids_on_automatically_validated_events(
        bookings,
        date)
    is_booking_on_used_event = (bookings['bookingId'].isin(ids_of_bookings_on_automatically_validated_events))
    quantity_of_bookings_on_event_automatically_validated = bookings['quantity_net'] * is_booking_on_used_event
    bookings['quantity_really_used'] = bookings['quantity_used'] + quantity_of_bookings_on_event_automatically_validated
    amount_for_bookings_on_event_automatically_validated = bookings['amount_net'] * is_booking_on_used_event
    bookings['amount_really_used'] = bookings['amount_used'] + amount_for_bookings_on_event_automatically_validated
    return bookings


def _get_booking_ids_on_automatically_validated_events(bookings, date):
    is_not_used = (bookings['amount_used'] == 0)
    is_passed_booking_cancellation_limit_date = (date > bookings['endDatetime'])
    bookings_on_automatically_validated_events = bookings.loc[
        is_not_used & is_passed_booking_cancellation_limit_date].bookingId.unique()
    return bookings_on_automatically_validated_events


def _add_stock_information_to_booking(bookings, stocks):
    bookings_with_stock_information = pd.merge(bookings,
                                               stocks[['stockId', 'endDatetime']], how='left',
                                               left_on='stockId',
                                               right_on='stockId', left_index=True, sort=False)
    return bookings_with_stock_information


def _add_offer_information_to_booking(correspondance_table_between_booking_and_offer, offers,
                                      bookings):
    bookings_with_offer_information = pd.merge(correspondance_table_between_booking_and_offer, offers,
                                               how='left', left_on='offerId', right_on='offerId', left_index=True,
                                               sort=False)
    bookings_with_offer_information = pd.merge(bookings, bookings_with_offer_information,
                                               how='left', left_on='bookingId', right_on='bookingId', left_index=True,
                                               sort=False)
    bookings_with_offer_information = bookings_with_offer_information.drop_duplicates()
    return bookings_with_offer_information


def _format_venue(venues):
    venues[['siret', 'venue_address', 'venue_postalCode', 'city']] = venues[
        ['siret', 'venue_address', 'venue_postalCode', 'city']].fillna('')
    return venues


def _add_amount_net_paid_and_amount_really_used_paid(venues):
    repayment_threshold = 20000
    venues['amount_net_paid'] = venues['amount_net']
    amount_net_is_over_repayment_threshold = venues['amount_net'] > repayment_threshold
    venues.loc[
        amount_net_is_over_repayment_threshold, 'amount_net_paid'] = repayment_threshold
    venues['amount_really_used_paid'] = venues['amount_really_used']
    amount_used_is_over_repayment_threshold = venues['amount_really_used'] > repayment_threshold
    venues.loc[
        amount_used_is_over_repayment_threshold, 'amount_really_used_paid'] = repayment_threshold
    return venues


def create_activated_users_table(connection, department=None):
    users = pd.read_sql_query('select * FROM "user";', connection)
    activated_users = users.loc[users['canBookFreeOffers'] == True]
    if department:
        return activated_users.loc[activated_users['departementCode']==department]
    return activated_users