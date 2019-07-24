# coding: utf-8
from datetime import datetime
from functools import partial

from apscheduler.schedulers.blocking import BlockingScheduler

from connectors import get_worksheet, connect_to_postgres
from statistics_dashboard import get_usage_indicators, get_departments_ranked_by_number_of_bookings, \
    get_offerer_indicators, get_offer_indicators, get_booking_indicators, get_offer_indicators_by_category_and_digital, \
    get_booking_indicators_by_category_and_digital, get_finance_indicators, get_ranking_of_most_booked_offers, \
    get_ranking_of_most_booked_offerers_ordered_by_quantity, get_ranking_of_most_booked_offerers_ordered_by_amount

SHEET_NAME = 'Test Tableau de bord pass Culture'
TAB_NAME = "Global"
DEPARTMENT_CODE = ['29','22','35','56','34','84','67','08','93','94','973','58','71','25']


def update_global_dashboard(date, get_global_dashboard=get_worksheet,
                            connect_to_database=connect_to_postgres):
    global_dashboard = get_global_dashboard(SHEET_NAME, TAB_NAME)
    connection = connect_to_database()

    usage_indicators = get_usage_indicators(connection)
    departments_ranked_by_number_of_bookings = get_departments_ranked_by_number_of_bookings(connection, DEPARTMENT_CODE)
    offerer_indicators = get_offerer_indicators(connection, date)
    offer_indicators = get_offer_indicators(connection, date)
    booking_indicators = get_booking_indicators(connection)
    offer_indicators_by_category_and_digital = get_offer_indicators_by_category_and_digital(connection)
    booking_indicators_by_category_and_digital_table = get_booking_indicators_by_category_and_digital(connection)
    finance_indicators = get_finance_indicators(connection, date)
    ranking_of_most_booked_offers = get_ranking_of_most_booked_offers(connection)
    ranking_of_most_booked_offerers_sorted_by_quantity = get_ranking_of_most_booked_offerers_ordered_by_quantity(
        connection)
    ranking_of_most_booked_offerers_sorted_by_amount = get_ranking_of_most_booked_offerers_ordered_by_amount(
        connection)

    usage_indicators_spreadsheet_location = 'A8'
    departments_ranked_by_number_of_bookings_spreadsheet_location = 'A15'
    offerer_indicators_spreadsheet_location = 'A33'
    offer_indicators_spreadsheet_location = 'E33'
    booking_indicators_spreadsheet_location = 'I33'
    offer_indicators_by_category_and_digital_spreadsheet_location = 'A40'
    booking_indicators_by_category_and_digital_table_spreadsheet_location = 'E40'
    finance_indicators_spreadsheet_location = 'A63'
    ranking_of_most_booked_offers_spreadsheet_location = 'A70'
    ranking_of_most_booked_offerers_sorted_by_quantity_spreadsheet_location = 'A94'
    ranking_of_most_booked_offerers_sorted_by_amount_spreadsheet_location = 'A117'

    global_dashboard.set_dataframe(usage_indicators, usage_indicators_spreadsheet_location)
    global_dashboard.set_dataframe(departments_ranked_by_number_of_bookings,
                                   departments_ranked_by_number_of_bookings_spreadsheet_location)
    global_dashboard.set_dataframe(offerer_indicators, offerer_indicators_spreadsheet_location)
    global_dashboard.set_dataframe(offer_indicators, offer_indicators_spreadsheet_location)
    global_dashboard.set_dataframe(booking_indicators, booking_indicators_spreadsheet_location)
    global_dashboard.set_dataframe(offer_indicators_by_category_and_digital,
                                   offer_indicators_by_category_and_digital_spreadsheet_location)
    global_dashboard.set_dataframe(booking_indicators_by_category_and_digital_table,
                                   booking_indicators_by_category_and_digital_table_spreadsheet_location)

    global_dashboard.set_dataframe(finance_indicators, finance_indicators_spreadsheet_location)

    global_dashboard.set_dataframe(ranking_of_most_booked_offers[['Offre', '# reservations', '€ depenses']],
                                   ranking_of_most_booked_offers_spreadsheet_location)
    global_dashboard.set_dataframe(
        ranking_of_most_booked_offerers_sorted_by_quantity[['Acteur culturel', '# réservations nettes', '€ dépensés']],
        ranking_of_most_booked_offerers_sorted_by_quantity_spreadsheet_location)
    global_dashboard.set_dataframe(
        ranking_of_most_booked_offerers_sorted_by_amount[['Acteur culturel', '# réservations nettes', '€ dépensés']],
        ranking_of_most_booked_offerers_sorted_by_amount_spreadsheet_location)


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    today = datetime.utcnow()
    update_global_dashboard_today = partial(update_global_dashboard, date=today)

    scheduler.add_job(update_global_dashboard_today, 'cron', id='send_final_booking_recaps', month='*', day=24, hour=16, minute=15)
