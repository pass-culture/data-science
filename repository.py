import pandas as pd


def get_activation_stock_id(connection):
    result = connection.execute("""
    SELECT stock.id 
    FROM stock 
    JOIN offer ON 
     offer.id = stock."offerId" 
     AND offer.type = 'ThingType.ACTIVATION'
    JOIN venue ON 
     venue.id = offer."venueId"
     AND venue."isVirtual" = true;""")
    return result.fetchone()[0]


def get_users(connection):
    return pd.read_sql_query('select * FROM "user";', connection)


def get_bookings(connection):
    return pd.read_sql_query('select * FROM booking;', connection)


def get_user_offerers(connection):
    return pd.read_sql_query('select * FROM user_offerer;', connection)


def get_offerers(connection):
    return pd.read_sql_query('select * FROM offerer;', connection)


def get_venues(connection):
    return pd.read_sql_query('select * FROM venue;', connection)


def get_stocks(connection):
    return pd.read_sql_query('select * FROM stock;', connection)


def get_offers(connection):
    return pd.read_sql_query('select * FROM offer;', connection)
