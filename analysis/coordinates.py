import pandas as pd
from geopy.distance import geodesic


def parse_coordinates(coord_str):
    """
    Function to parse the coordinate string into a tuple of floats (lat, lon).
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
    Function to calculate distance in km between two sets of coordinates.
    """
    if coord1 is None or coord2 is None:
        return 0
    return geodesic(coord1, coord2).kilometers


def count_movements(row, date_columns):
    """
    Function to count how many times a military unit moved based on changes in coordinates.
    """
    coords = [parse_coordinates(row[date]) for date in date_columns]
    movement_count = 0

    # Count the number of times the coordinates change (i.e., location changes)
    for i in range(1, len(coords)):
        if coords[i] is not None and coords[i] != coords[i - 1]:
            movement_count += 1

    return movement_count


def calculate_yearly_distance(row, date_columns):
    """
    Function to calculate the distance between the first and last valid (non-empty) coordinates in a row, being the yearly distance.
    """
    coords = [parse_coordinates(row[date]) for date in date_columns]

    # Find the first and last non-empty coordinate
    first_coord = next((coord for coord in coords if coord is not None), None)
    last_coord = next((coord for coord in reversed(coords) if coord is not None), None)

    # Calculate the yearly distance
    if first_coord and last_coord:
        return calculate_distance(first_coord, last_coord)
    return 0


def calculate_total_movement(csv_file, output_file):
    """
    Calculate total movement (in km) and number of movements for each row in the dataframe.
    Adds two columns: 'Totale beweging (km)' and 'Aantal bewegingen'.
    """
    df = pd.read_csv(csv_file)
    date_columns = [col for col in df.columns if col != 'Militaire eenheid']

    df["Totale beweging (km)"] = 0.0
    df["Aantal bewegingen"] = 0
    df["Jaarlijkse beweging (km)"] = 0.0

    # Iterate over each row and calculate total movement
    for idx, row in df.iterrows():
        total_distance = 0

        coords = [parse_coordinates(row[date]) for date in date_columns]

        # Calculate the distance between consecutive coordinates
        for i in range(1, len(coords)):
            dist = calculate_distance(coords[i-1], coords[i])
            if dist > 0: # Ignore pairs where distance couldn't be calculated
                total_distance += dist
        
        # Set the total movement for the current row
        df.at[idx, "Totale beweging (km)"] = total_distance

        # Calculate and set the number of movements (coordinate changes)
        df.at[idx, "Aantal bewegingen"] = count_movements(row, date_columns)

        # Calculate and set the yearly distance
        df.at[idx, "Jaarlijkse beweging (km)"] = calculate_yearly_distance(row, date_columns)
    
    # Sort the DataFrame based on the average movement
    df_sorted = df.sort_values(by="Totale beweging (km)", ascending=False)
    df_sorted.to_csv(output_file, index=False)
