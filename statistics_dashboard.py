# coding: utf-8

import pandas as pd
import numpy as np
import unidecode

from statistics_serializer import get_beneficiary_users_having_created_an_account_table, \
    get_real_booking_after_ministerial_decree_table, get_valid_offerer_table, \
    get_correspondance_table_between_booking_stock_and_offer, get_offer_with_stocks_and_valid_venue_table, \
    get_stock_table, get_correspondance_table_between_offer_venue_and_offerer, get_valid_venue_table, \
    get_venues_to_repay_table, get_activated_users_table


def get_usage_indicators(connection):
    beneficiary_users_having_created_an_account = get_beneficiary_users_having_created_an_account_table(connection)
    activated_users = get_activated_users_table(connection)
    bookings = get_real_booking_after_ministerial_decree_table(connection)
    number_of_created_accounts = str(beneficiary_users_having_created_an_account.userId.nunique())
    number_of_activated_accounts = str(activated_users['id'].nunique())
    number_of_accounts_with_at_least_one_booking = str(bookings['userId'].nunique())
    mean_number_of_booking = float(bookings.quantity_net.sum()) / float(number_of_accounts_with_at_least_one_booking)
    mean_expensed_amount = float(bookings.amount_net.sum()) / float(number_of_accounts_with_at_least_one_booking)
    usage_indicators = pd.DataFrame({"Indicateur": ["# Comptes créés", "# Comptes activés",
                                                           "# Comptes ayant réservé",
                                                           "# Moyen de réservations", "€ Moyen de dépenses"],
                                            "Valeur": [number_of_created_accounts, number_of_activated_accounts,
                                                       number_of_accounts_with_at_least_one_booking, mean_number_of_booking, mean_expensed_amount]},
                                           columns=["Indicateur", "Valeur"])
    usage_indicators['Valeur'] = usage_indicators['Valeur'].astype(float).round(decimals=2)
    return usage_indicators


def get_departments_ranked_by_number_of_bookings(connection, department_list):
    bookings = get_real_booking_after_ministerial_decree_table(connection)
    booking_columns_to_keep = ['userDepartementCode', 'quantity_net']
    bookings = bookings[booking_columns_to_keep]
    is_in_department_list = bookings['userDepartementCode'].isin(department_list)
    bookings_on_department_list = bookings.loc[is_in_department_list]
    bookings_by_department = pd.pivot_table(bookings_on_department_list, values=['quantity_net'],
                                            index=['userDepartementCode'],
                                            aggfunc={'quantity_net': np.sum})
    bookings_by_department['userDepartementCode'] = bookings_by_department.index
    departments_ranked_by_number_of_bookings = bookings_by_department.sort_values('quantity_net', ascending=False)
    departments_ranking_on_booking_columns_to_keep = ['userDepartementCode', 'quantity_net']
    departments_ranked_by_number_of_bookings = departments_ranked_by_number_of_bookings[
        departments_ranking_on_booking_columns_to_keep]
    departments_ranked_by_number_of_bookings.rename(
        columns={'quantity_net': '# réservations', 'userDepartementCode': 'Département utilisateur'}, inplace=True)
    return departments_ranked_by_number_of_bookings


def get_offerer_indicators(connection, date):
    valid_offerers = get_valid_offerer_table(connection)
    bookings = get_real_booking_after_ministerial_decree_table(connection)
    correspondance_table_between_booking_stock_and_offer = get_correspondance_table_between_booking_stock_and_offer(
        connection)
    offers = get_offer_with_stocks_and_valid_venue_table(connection)
    stocks = get_stock_table(connection)
    correspondance_table_between_offer_venue_and_offerer = get_correspondance_table_between_offer_venue_and_offerer(
        connection)

    total_number_of_valid_offerers = _get_total_number_of_valid_offerers(valid_offerers)

    number_of_offerers_having_created_an_offer = _get_number_of_offerers_having_created_an_offer(
        correspondance_table_between_offer_venue_and_offerer, offers)

    number_of_offerers_with_an_available_offer = _get_number_of_offerers_with_an_available_offer(
        correspondance_table_between_offer_venue_and_offerer, date, offers, stocks)

    number_of_offerers_with_a_booked_offer = _get_number_of_offerers_with_a_booked_offer(
        correspondance_table_between_offer_venue_and_offerer, bookings,
        correspondance_table_between_booking_stock_and_offer)

    offerer_indicators = pd.DataFrame(
        {"Indicateur": ["# Offreurs depuis le début du pass", "# Offreurs ayant mis une offre depuis le début du pass",
                        "# Offreurs ayant une offre disponible",
                        "#Offreurs réservés"],
         "Valeur": [total_number_of_valid_offerers, number_of_offerers_having_created_an_offer,
                    number_of_offerers_with_an_available_offer, number_of_offerers_with_a_booked_offer]},
        columns=["Indicateur", "Valeur"])

    return offerer_indicators


def get_offer_indicators(connection, T):
    bookings = get_real_booking_after_ministerial_decree_table(connection)
    correspondance_table_between_booking_stock_and_offer = get_correspondance_table_between_booking_stock_and_offer(
        connection)
    offers = get_offer_with_stocks_and_valid_venue_table(connection)
    stocks = get_stock_table(connection)

    number_of_booked_offers = _get_number_of_booked_offers(bookings,
                                                           correspondance_table_between_booking_stock_and_offer, offers)

    number_of_available_offers = _get_number_of_available_offers(T, offers, stocks)

    total_number_of_offers = _get_total_number_of_offers(offers)

    offer_indicators = pd.DataFrame(
        {"Indicateur": ["# Offres depuis le début du pass", "# Offres disponibles", "# Offres réservées"],
         "Valeur": [total_number_of_offers, number_of_available_offers, number_of_booked_offers]},
        columns=["Indicateur", "Valeur"])

    return offer_indicators


def get_booking_indicators(connection):
    bookings = get_real_booking_after_ministerial_decree_table(connection)

    total_number_of_not_cancelled_bookings = int(bookings.quantity_net.sum())
    number_of_validated_bookings = int(bookings.quantity_used.sum())

    booking_indicators = pd.DataFrame({"Indicateur": ["# Réservations nettes", "# Réservations validées"],
                                       "Valeur": [total_number_of_not_cancelled_bookings,
                                                  number_of_validated_bookings]},
                                      columns=["Indicateur", "Valeur"])
    return booking_indicators


def get_offer_indicators_by_category_and_digital(connection):
    offers = get_offer_with_stocks_and_valid_venue_table(connection)
    venues = get_valid_venue_table(connection)

    offers_with_category_and_digital = _add_category_and_digital_to_offer(offers, venues)

    offers_by_category_and_digital = _get_number_of_offers_by_category_and_digital(
        offers_with_category_and_digital)
    return offers_by_category_and_digital


def get_booking_indicators_by_category_and_digital(connection):
    bookings = get_real_booking_after_ministerial_decree_table(connection)
    correspondance_table_between_booking_stock_and_offer = get_correspondance_table_between_booking_stock_and_offer(
        connection)
    offers = get_offer_with_stocks_and_valid_venue_table(connection)
    venues = get_valid_venue_table(connection)

    offer_with_type = _add_category_to_offer(offers)
    offer_with_virtual = _add_digital_to_offer(offers, venues)

    booked_id = bookings[bookings['quantity_net'] > 0].bookingId.unique()
    temp = correspondance_table_between_booking_stock_and_offer.loc[
        correspondance_table_between_booking_stock_and_offer['bookingId'].isin(booked_id)]

    booking_offer = temp[['bookingId', 'offerId']]

    booking_with_type = pd.merge(booking_offer, offer_with_type,
                                 how='left', left_on='offerId', right_on='offerId', left_index=True, sort=False)

    booking_with_virtual = pd.merge(booking_offer, offer_with_virtual, how='left', left_on='offerId',
                                    right_on='offerId', left_index=True, sort=False)

    booking_with_type_and_virtual = pd.merge(booking_with_virtual, booking_with_type, how='left', left_on='bookingId',
                                             right_on='bookingId', left_index=True, sort=False)
    booking_with_type_and_virtual = booking_with_type_and_virtual.replace([True, False], ['Numérique', 'Physique'])
    booking_by_type_and_virtual = pd.pivot_table(booking_with_type_and_virtual,
                                                 values=['bookingId', 'categorie', 'isVirtual'],
                                                 index=['categorie', 'isVirtual'],
                                                 aggfunc={'bookingId': pd.Series.nunique})

    booking_by_type_and_virtual.reset_index(inplace=True)
    booking_by_type_and_virtual.rename(columns={'isVirtual': 'Support', 'bookingId': '# réservations totales'},
                                       inplace=True)
    booking_by_type_and_virtual['# réservations totales'] = booking_by_type_and_virtual['# réservations totales'].astype(int)

    return booking_by_type_and_virtual


def get_finance_indicators(connection, date):
    beneficiaries_having_created_an_account = get_beneficiary_users_having_created_an_account_table(connection)
    beneficiaries_having_activated_their_account = beneficiaries_having_created_an_account.loc[
        beneficiaries_having_created_an_account['canBookFreeOffers'] == True]
    bookings = get_real_booking_after_ministerial_decree_table(connection)
    venues_to_repay = get_venues_to_repay_table(connection, date)

    credit_per_beneficiary = 500
    activated_credit = int(beneficiaries_having_activated_their_account['userId'].nunique() * credit_per_beneficiary)
    potentially_used_credit = int(bookings.amount_net.sum())
    to_repay_credit = int(venues_to_repay.amount_really_used_paid.sum())

    finance_indicators = pd.DataFrame({"Indicateur": ["€ Crédit total activé", "€ Crédit total dépensé",
                                                      "€ Dépenses totales à rembourser"],
                                       "Valeur": [activated_credit, potentially_used_credit, to_repay_credit]},
                                      columns=["Indicateur", "Valeur"])
    return finance_indicators


def get_ranking_of_most_booked_offers(connection):
    bookings = get_real_booking_after_ministerial_decree_table(connection)
    correspondance_table_between_booking_stock_and_offer = get_correspondance_table_between_booking_stock_and_offer(
        connection)
    offers = get_offer_with_stocks_and_valid_venue_table(connection)

    booked_id = bookings[bookings['quantity_net'] > 0].bookingId.unique()
    correspondance_table_of_not_cancelled_bookings = correspondance_table_between_booking_stock_and_offer.loc[
        correspondance_table_between_booking_stock_and_offer['bookingId'].isin(booked_id)]
    not_cancelled_bookings = correspondance_table_of_not_cancelled_bookings[['bookingId', 'offerId']]

    not_cancelled_bookings_with_offer_name = pd.merge(not_cancelled_bookings, offers[['offerId', 'name']], how='inner',
                                                      left_on='offerId', right_on='offerId',
                                                      left_index=True, sort=False)
    not_cancelled_bookings_with_name_quantity_and_amount = pd.merge(not_cancelled_bookings_with_offer_name, bookings[
        ['bookingId', 'quantity_net', 'amount_net']], how='inner', left_on='bookingId',
                                                                    right_on='bookingId', left_index=True, sort=False)
    not_cancelled_bookings_with_name_quantity_and_amount = not_cancelled_bookings_with_name_quantity_and_amount.drop_duplicates()

    quantity_and_amount_booked_per_offer = not_cancelled_bookings_with_name_quantity_and_amount.groupby(
        ['name']).sum().reset_index()

    top_20_quantity_and_amount_booked_per_offer = quantity_and_amount_booked_per_offer.nlargest(20, 'quantity_net')
    top_20_quantity_and_amount_booked_per_offer = top_20_quantity_and_amount_booked_per_offer.sort_values(
        'quantity_net', ascending=False)
    top_20_quantity_and_amount_booked_per_offer = top_20_quantity_and_amount_booked_per_offer.reset_index()
    top_20_quantity_and_amount_booked_per_offer.rename(
        columns={'name': 'Offre', 'quantity_net': '# reservations', 'amount_net': '€ depenses'}, inplace=True)
    top_20_quantity_and_amount_booked_per_offer['Offre'] = top_20_quantity_and_amount_booked_per_offer['Offre'].apply(
        lambda x: unidecode.unidecode(x))
    top_20_quantity_and_amount_booked_per_offer[u'€ depenses'] = top_20_quantity_and_amount_booked_per_offer[u'€ depenses'].round(decimals=2)
    return top_20_quantity_and_amount_booked_per_offer


def get_ranking_of_most_booked_offerers_ordered_by_quantity(connection, department=None):
    not_cancelled_bookings_with_name_quantity_amount_and_offerer = _get_not_cancelled_bookings_with_name_quantity_amout_and_offerer(
        connection, department=None)
    top_20_quantity_and_amount_booked_per_offerer = not_cancelled_bookings_with_name_quantity_amount_and_offerer.nlargest(
        20, 'quantity_net')
    top_20_quantity_and_amount_booked_per_offerer_ordered_by_quantity = top_20_quantity_and_amount_booked_per_offerer.sort_values(
        'quantity_net', ascending=False)

    top_20_quantity_and_amount_booked_per_offerer_ordered_by_quantity.rename(
        columns={'offerer_name': 'Acteur culturel', 'quantity_net': '# réservations nettes',
                 'amount_net': '€ dépensés'}, inplace=True)
    top_20_quantity_and_amount_booked_per_offerer_ordered_by_quantity[u'€ dépensés'] = \
    top_20_quantity_and_amount_booked_per_offerer_ordered_by_quantity[u'€ dépensés'].round(decimals=2)
    return top_20_quantity_and_amount_booked_per_offerer_ordered_by_quantity


def get_ranking_of_most_booked_offerers_ordered_by_amount(connection):
    not_cancelled_bookings_with_name_quantity_amount_and_offerer = _get_not_cancelled_bookings_with_name_quantity_amout_and_offerer(
        connection)
    top_20_quantity_and_amount_booked_per_offerer = not_cancelled_bookings_with_name_quantity_amount_and_offerer.nlargest(
        20, 'amount_net')
    top_20_quantity_and_amount_booked_per_offerer_sorted_by_amount = top_20_quantity_and_amount_booked_per_offerer.nlargest(
        20, 'amount_net')
    top_20_quantity_and_amount_booked_per_offerer_sorted_by_amount = top_20_quantity_and_amount_booked_per_offerer_sorted_by_amount.sort_values(
        'amount_net', ascending=False)

    top_20_quantity_and_amount_booked_per_offerer_sorted_by_amount.rename(
        columns={'offerer_name': 'Acteur culturel', 'quantity_net': '# réservations nettes',
                 'amount_net': '€ dépensés'}, inplace=True)
    top_20_quantity_and_amount_booked_per_offerer_sorted_by_amount[u'€ dépensés'] = top_20_quantity_and_amount_booked_per_offerer_sorted_by_amount[
        u'€ dépensés'].round(decimals=2)
    return top_20_quantity_and_amount_booked_per_offerer_sorted_by_amount


def _get_number_of_offers_by_category_and_digital(offers_with_category_and_digital):
    offers_by_category_and_digital = pd.pivot_table(offers_with_category_and_digital,
                                                    values=['offerId', 'categorie', 'isVirtual'],
                                                    index=['categorie', 'isVirtual'],
                                                    aggfunc={'offerId': pd.Series.nunique})
    offers_by_category_and_digital = offers_by_category_and_digital.sort_values('offerId', ascending=False)
    offers_by_category_and_digital.reset_index(inplace=True)
    offers_by_category_and_digital.rename(columns={'isVirtual': 'Support', 'offerId': '# offres totales'}, inplace=True)
    return offers_by_category_and_digital


def _add_category_and_digital_to_offer(offers, venues):
    offers_with_category = _add_category_to_offer(offers)
    offers_with_digital = _add_digital_to_offer(offers, venues)
    offers_with_category_and_digital = pd.merge(offers_with_digital, offers_with_category, how='left',
                                                left_on='offerId',
                                                right_on='offerId', left_index=True, sort=False)
    offers_with_category_and_digital = offers_with_category_and_digital.replace([True, False],
                                                                                ['Numérique', 'Physique'])
    return offers_with_category_and_digital


def _add_digital_to_offer(offers, venues):
    offers_with_digital = pd.merge(offers[['offerId', 'venueId']], venues[['venueId', 'isVirtual']], how='left',
                                   left_on='venueId', right_on='venueId', left_index=True, sort=False)
    del (offers_with_digital['venueId'])
    return offers_with_digital


def _add_category_to_offer(offers):
    offers_with_category = offers[['categorie', 'offerId']]
    offers_with_category = offers_with_category.fillna('Autre')
    return offers_with_category


def _get_total_number_of_offers(offers):
    total_number_of_offers = offers.offerId.nunique()
    return total_number_of_offers


def _get_number_of_available_offers(T, offers, stocks):
    has_some_stock_left = (stocks['stock_available'] != 0.0)
    can_still_be_booked = ((stocks['bookingLimitDatetime'].isnull()) | (stocks['bookingLimitDatetime'] > T))
    is_available = has_some_stock_left & can_still_be_booked
    available_stock = stocks[is_available]
    ids_of_available_offers = available_stock.offerId.unique()
    available_offers = offers.loc[offers['offerId'].isin(ids_of_available_offers)].offerId
    number_of_available_offers = available_offers.nunique()
    return number_of_available_offers


def _get_number_of_booked_offers(bookings, correspondance_table_between_booking_stock_and_offer, offers):
    has_at_least_one_not_cancelled_booking = bookings['quantity_net'] > 0
    ids_of_not_cancelled_bookings = bookings[has_at_least_one_not_cancelled_booking].bookingId.unique()
    correspondance_table_of_not_cancelled_bookings = correspondance_table_between_booking_stock_and_offer.loc[
        correspondance_table_between_booking_stock_and_offer['bookingId'].isin(ids_of_not_cancelled_bookings)]
    booked_offer = correspondance_table_of_not_cancelled_bookings.loc[
        correspondance_table_of_not_cancelled_bookings['offerId'].isin(offers.offerId.unique())].offerId
    number_of_booked_offers = booked_offer.nunique()
    return number_of_booked_offers


def _get_number_of_offerers_with_a_booked_offer(correspondance_table_between_offer_venue_and_offerer, bookings,
                                                correspondance_table_between_booking_stock_and_offer):
    booked_offer_ids = _get_booked_offer_ids(bookings, correspondance_table_between_booking_stock_and_offer)
    has_a_booked_offer = correspondance_table_between_offer_venue_and_offerer['offerId'].isin(booked_offer_ids)
    number_of_offerers_with_a_booked_offer = correspondance_table_between_offer_venue_and_offerer.loc[
        has_a_booked_offer].managingOffererId.nunique()
    return number_of_offerers_with_a_booked_offer


def _get_number_of_offerers_with_an_available_offer(correspondance_table_between_offer_venue_and_offerer, date, offers,
                                                    stocks):
    available_offer_ids = _get_available_offer_ids(date, offers, stocks)
    has_an_available_offer = correspondance_table_between_offer_venue_and_offerer['offerId'].isin(
        available_offer_ids)
    number_of_offerers_with_an_available_offer = correspondance_table_between_offer_venue_and_offerer.loc[
        has_an_available_offer].managingOffererId.nunique()
    return number_of_offerers_with_an_available_offer


def _get_number_of_offerers_having_created_an_offer(correspondance_table_between_offer_venue_and_offerer, offers):
    has_an_offer = correspondance_table_between_offer_venue_and_offerer['offerId'].isin(offers.offerId.unique())
    number_of_offerers_having_created_an_offer = correspondance_table_between_offer_venue_and_offerer.loc[
        has_an_offer].managingOffererId.nunique()
    return number_of_offerers_having_created_an_offer


def _get_total_number_of_valid_offerers(valid_offerers):
    total_number_of_valid_offerers = valid_offerers.offererId.nunique()
    return total_number_of_valid_offerers


def _get_available_offer_ids(date, offers, stocks):
    has_some_stock_left = (stocks['stock_available'] != 0.0)
    can_still_be_booked = (stocks['bookingLimitDatetime'].isnull()) | (stocks['bookingLimitDatetime'] > date)
    is_available = has_some_stock_left & (
        can_still_be_booked)
    available_stock = stocks[is_available]
    ids_of_offers_with_available_stock = available_stock.offerId.unique()
    available_offer_ids = offers.loc[offers['offerId'].isin(ids_of_offers_with_available_stock)].offerId.unique()
    return available_offer_ids


def _get_booked_offer_ids(bookings, correspondance_table_between_booking_stock_and_offer):
    has_at_least_one_not_cancelled_booking = bookings['quantity_net'] > 0
    ids_of_not_cancelled_bookings = bookings[has_at_least_one_not_cancelled_booking].bookingId.unique()
    has_id_in_ids_of_not_cancelled_bookings = correspondance_table_between_booking_stock_and_offer['bookingId'].isin(
        ids_of_not_cancelled_bookings)
    correspondance_table_of_not_cancelled_bookings = correspondance_table_between_booking_stock_and_offer.loc[
        has_id_in_ids_of_not_cancelled_bookings]
    booked_offer_ids = correspondance_table_of_not_cancelled_bookings.offerId.unique()
    return booked_offer_ids


def _get_not_cancelled_bookings_with_name_quantity_amout_and_offerer(connection, department=None):
    bookings = get_real_booking_after_ministerial_decree_table(connection)
    correspondance_table_between_booking_stock_and_offer = get_correspondance_table_between_booking_stock_and_offer(
        connection)
    offers = get_offer_with_stocks_and_valid_venue_table(connection)
    correspondance_table_between_offer_venue_and_offerer = get_correspondance_table_between_offer_venue_and_offerer(
        connection)
    offerers = get_valid_offerer_table(connection)
    not_cancelled_bookings_with_offer_name = _get_not_cancelled_bookings_with_offer_name(bookings,
                                                                                         correspondance_table_between_booking_stock_and_offer,
                                                                                         offers)
    not_cancelled_bookings_with_name_quantity_and_amount = pd.merge(not_cancelled_bookings_with_offer_name, bookings[
        ['bookingId', 'quantity_net', 'amount_net']], how='inner', left_on='bookingId',
                                                                    right_on='bookingId', left_index=True, sort=False)
    not_cancelled_bookings_with_name_quantity_amount_and_offerer_id = pd.merge(
        not_cancelled_bookings_with_name_quantity_and_amount,
        correspondance_table_between_offer_venue_and_offerer[['offerId', 'managingOffererId']],
        how='inner', left_on='offerId', right_on='offerId', left_index=True, sort=False)
    not_cancelled_bookings_with_name_quantity_amount_and_offerer = pd.merge(
        not_cancelled_bookings_with_name_quantity_amount_and_offerer_id,
        offerers[['offererId', 'offerer_name']],
        how='inner', left_on='managingOffererId', right_on='offererId', left_index=True, sort=False)
    del (not_cancelled_bookings_with_name_quantity_amount_and_offerer['bookingId'])
    del (not_cancelled_bookings_with_name_quantity_amount_and_offerer['offerId'])
    del (not_cancelled_bookings_with_name_quantity_amount_and_offerer['name'])
    del (not_cancelled_bookings_with_name_quantity_amount_and_offerer['managingOffererId'])
    del (not_cancelled_bookings_with_name_quantity_amount_and_offerer['offererId'])
    not_cancelled_bookings_with_name_quantity_amount_and_offerer = not_cancelled_bookings_with_name_quantity_amount_and_offerer.groupby(
        ['offerer_name']).sum().reset_index()
    return not_cancelled_bookings_with_name_quantity_amount_and_offerer


def _get_not_cancelled_bookings_with_offer_name(bookings, correspondance_table_between_booking_stock_and_offer, offers):
    booked_id = bookings[bookings['quantity_net'] > 0].bookingId.unique()
    correspondance_table_of_not_cancelled_bookings = correspondance_table_between_booking_stock_and_offer.loc[
        correspondance_table_between_booking_stock_and_offer['bookingId'].isin(booked_id)]
    not_cancelled_bookings = correspondance_table_of_not_cancelled_bookings[['bookingId', 'offerId']]
    not_cancelled_bookings_with_offer_name = pd.merge(not_cancelled_bookings, offers[['offerId', 'name']], how='inner',
                                                      left_on='offerId', right_on='offerId',
                                                      left_index=True, sort=False)
    return not_cancelled_bookings_with_offer_name
