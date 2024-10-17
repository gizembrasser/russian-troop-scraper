import pandas as pd
from analysis.coordinates import parse_coordinates, calculate_distance, calculate_yearly_distance


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