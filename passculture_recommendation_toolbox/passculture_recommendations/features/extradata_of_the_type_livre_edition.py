def get_feature_of_the_book(extradata_livres):
    feature_of_the_book = []
    for data in extradata_livres['extraData']:
        if data is None:
            continue
        for key in data.keys():
            if key not in feature_of_the_book:
                feature_of_the_book.append(key)

    print("The characteristics that can be recovered from the Extradata column are: ")
    return feature_of_the_book


def add_columns_of_the_features_in_df_extradata_livre(extradata_livres, feature_of_the_book):
    for feature in feature_of_the_book:
        extradata_livres[feature] = extradata_livres['extraData'].apply(lambda x: x.get(feature) if x != None else None)
    return extradata_livres
