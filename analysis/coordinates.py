import pandas as pd
from geopy.distance import geodesic


def parse_coordinates(coord_str):
    """
    Function to parse the coordinate string into a tuple of floats (lat, lon)
    """
    if isinstance(coord_str, str):
        try:
            lat, lon = map(float, coord_str.split(","))
            return lat, lon
        except ValueError:
            return None  # Return None if parsing fails (handle missing or malformed values)
    return None  # Return None if coord_str is not a string


def calculate_distance(coord1, coord2):
    """
    Function to calculate distance in km between two sets of coordinates
    """
    if coord1 is None or coord2 is None:
        return 0
    return geodesic(coord1, coord2).kilometers


def calculate_avg_movement(df):
    date_columns = [col for col in df.columns if col != 'Militaire eenheid']

    df["Gemiddelde beweging (km)"] = 0.0

    # Iterate over each row and calculate average movement
    for idx, row in df.iterrows():
        total_distance = 0
        valid_pairs = 0

        coords = [parse_coordinates(row[date]) for date in date_columns]

        # Calculate the distance between consecutive coordinates
        for i in range(1, len(coords)):
            dist = calculate_distance(coords[i-1], coords[i])
            if dist > 0: # Ignore pairs where distance couldn't be calculated
                total_distance += dist
                valid_pairs += 1
        
        # Calculate the average movement
        if valid_pairs > 0:
            df.at[idx, "Gemiddelde beweging (km)"] = total_distance / valid_pairs
        else:
            df.at[idx, "Gemiddelde beweging (km)"] = 0
    
    # Sort the DataFrame by the 'movement' column in descending order
    df_sorted = df.sort_values(by="Gemiddelde beweging (km)", ascending=False)
    return df_sorted
    
