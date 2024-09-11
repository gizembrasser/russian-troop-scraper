import argparse
from scraper import get_geojson_urls, get_troop_data
from utils.dates import get_date_range, get_column_names
from utils.merge import add_date_column, clean_unit_names
from analysis.coordinates import calculate_total_movement


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="python main.py")
    subparsers = parser.add_subparsers(dest="command")

    date_range = subparsers.add_parser("date_range", help="Collect GeoJSON data based on a range of dates")
    date_range.add_argument("start_date", help="Start date in format yyyy-mm-dd")
    date_range.add_argument("end_date", help="End date in format yyyy-mm-dd")
    date_range.add_argument("csv_name", help="Name for the CSV file (without extension)")

    date_list = subparsers.add_parser("date_list", help="Collect GeoJSON data based a list of dates")
    date_list.add_argument("csv_name", help="Name for the CSV file (without extension)")
    # Unfinished...

    merge_data = subparsers.add_parser("merge_data", help="Merge two DataFrames in order to add more date columns")

    clean_names = subparsers.add_parser("clean_names", help="Remove the Ukrainian name from the column 'Militaire eenheid' and only keep the English name")

    total_movement = subparsers.add_parser("total_movement", help="Calculate the total movement for each troop in km from a CSV file of coordinates")
    total_movement.add_argument("csv_file", help="Provide the path to the CSV file (with extension)")
    total_movement.add_argument("output_file", help="Provide the path to the output CSV file (with extension)")

    args = parser.parse_args()

    # Command for providing a date range from which to collect GeoJSON URLs
    if args.command == "date_range":
        start_date = args.start_date
        end_date = args.end_date
        csv_name = args.csv_name

        date_range = get_date_range(start_date, end_date)

        geojson_urls = get_geojson_urls(date_range)

        troop_df = get_troop_data(geojson_urls, get_column_names(date_range))
        troop_df.to_csv(f"data/{csv_name}.csv", index=False)
    
    # Command for manually providing a list of dates from which to collect GeoJSON URLs
    if args.command == "date_list":
        # csv_name = args.csv_name
        # date_list = [('2024', 'April', '2'), ('2024', 'May', '2')]
        
        # geojson_urls = get_geojson_urls(date_list)

        # troop_df = get_troop_data(geojson_urls, get_column_names(date_list))
        # troop_df.to_csv(f"data/{csv_name}.csv", index=False)
        print("Unfinished")
    
    # Command to merge two DataFrames in order to add more dates
    if args.command == "merge_data":
        # add_date_column("data/clean/2022-2023_troepen.csv", "data/clean/2024_troepen_clean.csv", "data/clean/2022-2024_troepen.csv")
        print("Unfinished")
    
    # Command to only keep the English names in the column 'Militaire eenheid'
    if args.command == "clean_names":
        # clean_unit_names("data/2024_troepen.csv", "data/2024_troepen_clean.csv")
        print("Unfinished")
    
    # Command to calculate the average movement between coordinates for the Russian troops
    if args.command == "total_movement":
        csv_file = args.csv_file
        output_file = args.output_file

        df_total_movement = calculate_total_movement(csv_file, output_file)
