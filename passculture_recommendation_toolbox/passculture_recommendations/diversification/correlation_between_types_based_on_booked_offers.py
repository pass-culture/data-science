import pandas as pd

def get_correlation_between_types_based_on_booked_offers(connection):
    booked_offers = pd.read_sql_query("""SELECT "user".id, offer.type 
                           FROM "booking" 
                           INNER JOIN "user" ON "user".id=booking."userId" 
                           INNER JOIN stock ON booking."stockId"=stock.id 
                           INNER JOIN offer ON offer.id=stock."offerId" 
                           WHERE offer.type!='ThingType.ACTIVATION'
                           ORDER BY "user".id """, connection)

    matrix_user_type = pd.DataFrame(index=booked_offers['id'].unique(),
                                    columns=booked_offers['type'].unique())

    is_EventType_SPECTACLE_VIVANT = (booked_offers['type'] == 'EventType.SPECTACLE_VIVANT')
    is_EventType_MUSEES_PATRIMOINE = (booked_offers['type'] == 'EventType.MUSEES_PATRIMOINE')
    is_ThingType_LIVRE_EDITION = (booked_offers['type'] == 'ThingType.LIVRE_EDITION')
    is_ThingType_AUDIOVISUEL = (booked_offers['type'] == 'ThingType.AUDIOVISUEL')
    is_EventType_MUSIQUE = (booked_offers['type'] == 'EventType.MUSIQUE')
    is_EventType_CINEMA = (booked_offers['type'] == 'EventType.CINEMA')
    is_ThingType_CINEMA_ABO = (booked_offers['type'] == 'ThingType.CINEMA_ABO')
    is_EventType_CONFERENCE_DEBAT_DEDICACE = (
                booked_offers['type'] == 'EventType.CONFERENCE_DEBAT_DEDICACE')
    is_ThingType_INSTRUMENT = (booked_offers['type'] == 'ThingType.INSTRUMENT')
    is_EventType_PRATIQUE_ARTISTIQUE = (booked_offers['type'] == 'EventType.PRATIQUE_ARTISTIQUE')
    is_ThingType_MUSIQUE = (booked_offers['type'] == 'ThingType.MUSIQUE')
    is_ThingType_JEUX_VIDEO = (booked_offers['type'] == 'ThingType.JEUX_VIDEO')
    is_ThingType_MUSEES_PATRIMOINE_ABO = (booked_offers['type'] == 'ThingType.JEUX_VIDEO')
    is_ThingType_PRATIQUE_ARTISTIQUE_ABO = (
                booked_offers['type'] == 'ThingType.PRATIQUE_ARTISTIQUE_ABO')
    is_EventType_JEUX = (booked_offers['type'] == 'EventType.JEUX')
    is_ThingType_MUSIQUE_ABO = (booked_offers['type'] == 'ThingType.MUSIQUE_ABO')
    is_ThingType_SPECTACLE_VIVANT_ABO = (booked_offers['type'] == 'ThingType.SPECTACLE_VIVANT_ABO')
    is_ThingType_CINEMA_CARD = (booked_offers['type'] == 'ThingType.CINEMA_CARD')
    is_ThingType_OEUVRE_ART = (booked_offers['type'] == 'ThingType.OEUVRE_ART')
    is_ThingType_JEUX_VIDEO_ABO = (booked_offers['type'] == 'ThingType.JEUX_VIDEO_ABO')
    is_ThingType_PRESSE_ABO = (booked_offers['type'] == 'ThingType.PRESSE_ABO')
    is_ThingType_LIVRE_AUDIO = (booked_offers['type'] == 'ThingType.LIVRE_AUDIO')

    df = booked_offers[is_EventType_SPECTACLE_VIVANT]
    matrix_user_type['EventType.SPECTACLE_VIVANT'] = booked_offers['id'].apply(
        lambda x: 1 if x in df['id'].values else 0)

    df = booked_offers[is_EventType_MUSEES_PATRIMOINE]
    matrix_user_type['EventType.MUSEES_PATRIMOINE'] = booked_offers['id'].apply(
        lambda x: 1 if x in df['id'].values else 0)

    df = booked_offers[is_ThingType_LIVRE_EDITION]
    matrix_user_type['ThingType.LIVRE_EDITION'] = booked_offers['id'].apply(
        lambda x: 1 if x in df['id'].values else 0)

    df = booked_offers[is_ThingType_AUDIOVISUEL]
    matrix_user_type['ThingType.AUDIOVISUEL'] = booked_offers['id'].apply(
        lambda x: 1 if x in df['id'].values else 0)

    df = booked_offers[is_EventType_MUSIQUE]
    matrix_user_type['EventType.MUSIQUE'] = booked_offers['id'].apply(
        lambda x: 1 if x in df['id'].values else 0)

    df = booked_offers[is_EventType_CINEMA]
    matrix_user_type['EventType.CINEMA'] = booked_offers['id'].apply(
        lambda x: 1 if x in df['id'].values else 0)

    df = booked_offers[is_ThingType_CINEMA_ABO]
    matrix_user_type['ThingType.CINEMA_ABO'] = booked_offers['id'].apply(
        lambda x: 1 if x in df['id'].values else 0)

    df = booked_offers[is_EventType_CONFERENCE_DEBAT_DEDICACE]
    matrix_user_type['EventType.CONFERENCE_DEBAT_DEDICACE'] = booked_offers['id'].apply(
        lambda x: 1 if x in df['id'].values else 0)

    df = booked_offers[is_ThingType_INSTRUMENT]
    matrix_user_type['ThingType.INSTRUMENT'] = booked_offers['id'].apply(
        lambda x: 1 if x in df['id'].values else 0)

    df = booked_offers[is_EventType_PRATIQUE_ARTISTIQUE]
    matrix_user_type['EventType.PRATIQUE_ARTISTIQUE'] = booked_offers['id'].apply(
        lambda x: 1 if x in df['id'].values else 0)

    df = booked_offers[is_ThingType_MUSIQUE]
    matrix_user_type['ThingType.MUSIQUE'] = booked_offers['id'].apply(
        lambda x: 1 if x in df['id'].values else 0)

    df = booked_offers[is_ThingType_JEUX_VIDEO]
    matrix_user_type['ThingType.JEUX_VIDEO'] = booked_offers['id'].apply(
        lambda x: 1 if x in df['id'].values else 0)

    df = booked_offers[is_ThingType_MUSEES_PATRIMOINE_ABO]
    matrix_user_type['ThingType.MUSEES_PATRIMOINE_ABO'] = booked_offers['id'].apply(
        lambda x: 1 if x in df['id'].values else 0)

    df = booked_offers[is_ThingType_PRATIQUE_ARTISTIQUE_ABO]
    matrix_user_type['ThingType.PRATIQUE_ARTISTIQUE_ABO'] = booked_offers['id'].apply(
        lambda x: 1 if x in df['id'].values else 0)

    df = booked_offers[is_EventType_JEUX]
    matrix_user_type['EventType.JEUX'] = booked_offers['id'].apply(
        lambda x: 1 if x in df['id'].values else 0)

    df = booked_offers[is_ThingType_MUSIQUE_ABO]
    matrix_user_type['ThingType.MUSIQUE_ABO'] = booked_offers['id'].apply(
        lambda x: 1 if x in df['id'].values else 0)

    df = booked_offers[is_ThingType_SPECTACLE_VIVANT_ABO]
    matrix_user_type['ThingType.SPECTACLE_VIVANT_ABO'] = booked_offers['id'].apply(
        lambda x: 1 if x in df['id'].values else 0)

    df = booked_offers[is_ThingType_CINEMA_CARD]
    matrix_user_type['ThingType.CINEMA_CARD'] = booked_offers['id'].apply(
        lambda x: 1 if x in df['id'].values else 0)

    df = booked_offers[is_ThingType_OEUVRE_ART]
    matrix_user_type['ThingType.OEUVRE_ART'] = booked_offers['id'].apply(
        lambda x: 1 if x in df['id'].values else 0)

    df = booked_offers[is_ThingType_JEUX_VIDEO_ABO]
    matrix_user_type['ThingType.JEUX_VIDEO_ABO'] = booked_offers['id'].apply(
        lambda x: 1 if x in df['id'].values else 0)

    df = booked_offers[is_ThingType_PRESSE_ABO]
    matrix_user_type['ThingType.PRESSE_ABO'] = booked_offers['id'].apply(
        lambda x: 1 if x in df['id'].values else 0)

    df = booked_offers[is_ThingType_LIVRE_AUDIO]
    matrix_user_type['ThingType.LIVRE_AUDIO'] = booked_offers['id'].apply(
        lambda x: 1 if x in df['id'].values else 0)

    matrix_type_type_corr = matrix_user_type.corr()

    return matrix_type_type_corr