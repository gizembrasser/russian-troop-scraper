from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from coordinates import parse_coordinates


def get_oblast(lat, lon):
    """
    Function to return the name of the Russian or Ukrainian oblast (region) fro a given coordinate.
    """
    try:
        # Use Nominatim geocoder
        geolocator = Nominatim(user_agent="geo_oblast_locator")
        location = geolocator.reverse((lat, lon), language="en", timeout=10)

        # Check if a valid location is returned
        if location and "address" in location.raw:
            address = location.raw["address"]

            # Check for 'state' or 'region' in the address to find the oblast
            oblast = address.get("state", None) or address.get("region", None)
            return oblast if oblast else None
        return None
        
    except GeocoderTimedOut:
        print("Geocoder service timed out.")


def filter_oblast(df, oblast_name):
    """
    Function to filter rows of a DataFrame where the coordinate's oblast doesn't match the provided oblast name.
    """
    coord_column = df.loc[:, 1] # Second column contains the coordinates

    def is_in_oblast(coord_str):
        # Parse the coordinates
        coordinates = parse_coordinates(coord_str)
        if coordinates is None:
            return False
        
        lat, lon = coordinates

        # Get the oblast from the coordinates
        oblast = get_oblast(lat, lon)

        # Check if the oblast matches the provided one
        return oblast_name.lower() in oblast.lower() if oblast != None else False

    # Filter the DataFrame
    mask = coord_column.apply(is_in_oblast)
    
    filtered_df = df[mask].copy()
    return filtered_df

    
