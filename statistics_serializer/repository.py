def get_activation_stock_id(connection):
    result = connection.execute("""
    SELECT stock.id 
    FROM stock 
    JOIN offer on offer.id=stock."offerId" 
    JOIN venue ON venue.id = offer."venueId" 
    WHERE venue."isVirtual" 
    AND offer.type = 'ThingType.ACTIVATION';""")
    return result.fetchone()[0]
