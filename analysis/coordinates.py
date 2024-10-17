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
