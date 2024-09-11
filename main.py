from scraper import get_geojson_urls, get_troop_data
from utils.dates import get_date_range


if __name__ == "__main__":
    start_date = input("Enter the start date in format yyyy-mm-dd: ")
    end_date = input("Enter the end date in format yyyy-mm-dd: ")

    date_range = get_date_range(start_date, end_date)

    # Retrieve the URL containing the geojson
    geojson_urls = get_geojson_urls(date_range)
    print("API requests made to:", geojson_urls)

    # # Store the necessary data from the JSON into a dataframe and convert to CSV
    # troop_df = get_troop_data(geojson_url, start_date)
    # troop_df.to_csv("data/russische_troepen.csv", index=False)
    # print("CSV succesfully saved to /data folder.")