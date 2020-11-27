def clean_data(data):
    # Eliminating rows with NaN and null values
    if data.isnull().values.any():
        data.dropna(subset=["win", "firstBlood", "firstTower", "firstInhibitor",
                            "firstBaron", "firstDragon", "firstRiftHerald"], inplace=True)
    return data
