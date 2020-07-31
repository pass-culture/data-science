import numpy as np

def add_support_in_type(df_of_offers_with_column_type_to_add_support):
    for i, row in df_of_offers_with_column_type_to_add_support.iterrows():
        df_of_offers_with_column_type_to_add_support.loc[i, 'type'] = np.where(row.url is None, row['type'] + '_physique',
                                                               row['type'] + '_numerique')

    return df_of_offers_with_column_type_to_add_support


