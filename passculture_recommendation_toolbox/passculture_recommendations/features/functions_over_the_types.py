import pandas as pd


def create_dataframe_of_the_name_of_all_the_types(df):
    name_of_all_the_types = pd.DataFrame()
    name_of_all_the_types['type'] = df['type'].value_counts().index
    return name_of_all_the_types


def replace_dot_with_a_dash_in_the_column_type(df):
    list_of_types = []
    for types in df['type']:
        list_of_types.append(str(types).replace(".", "_"))
    df['type'] = list_of_types
    return df

