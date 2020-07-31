import pandas as pd

def compute_number_of_offer_per_category(dataframe_of_offers, category, total) -> pd.DataFrame:
    number_of_offers_per_category = pd.DataFrame(columns = [category, total])
    number_of_offers_per_category[category] = dataframe_of_offers[category].value_counts().index
    number_of_offers_per_category[total] = dataframe_of_offers[category].value_counts().array

    return number_of_offers_per_category


