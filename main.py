import argparse
from scraper import get_geojson_urls, get_troop_data
from utils.dates import get_date_range, get_column_names, parse_date
from utils.merge import add_date_column, clean_unit_names
from analysis.coordinates import calculate_total_movement


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="python main.py")
    subparsers = parser.add_subparsers(dest="command")

    date_range = subparsers.add_parser("date_range", help="Collect GeoJSON data based on a range of dates")
    date_range.add_argument("start_date", help="Start date in format yyyy-mm-dd")
    date_range.add_argument("end_date", help="End date in format yyyy-mm-dd")
    date_range.add_argument("output_file", help="Provide the name for the output CSV file (without extension)")

    date_list = subparsers.add_parser("date_list", help="Collect GeoJSON data based a list of dates")
    date_list.add_argument("output_file", help="Provide the name for the output CSV file (without extension)")
    date_list.add_argument("dates", nargs="+", help="List of dates (separated by a space) in format yyyy-mm-dd")

    merge_data = subparsers.add_parser("merge_data", help="Merge two DataFrames in order to add more date columns")
    merge_data.add_argument("file1", help="Provide the name of the first input CSV file to merge (without extension)")
    merge_data.add_argument("file2", help="Provide the name of the second input CSV file to merge (without extension)")
    date_range.add_argument("output_file", help="Provide the name for the output CSV file (without extension)")

    clean_names = subparsers.add_parser("clean_names", help="Remove the Ukrainian name from the column 'Militaire eenheid' and only keep the English name")
    clean_names.add_argument("csv_file", help="Provide the name of the input CSV file to clean (without extension)")
    clean_names.add_argument("output_file", help="Provide the name for the output CSV file (without extension)")

    total_movement = subparsers.add_parser("total_movement", help="Calculate the total movement for each troop in km from a CSV file of coordinates")
    total_movement.add_argument("csv_file", help="Provide the name of the input CSV file to clean (without extension)")
    total_movement.add_argument("output_file", help="Provide the name for the output CSV file (without extension)")

    args = parser.parse_args()

    # Command for providing a date range from which to collect GeoJSON URLs
    if args.command == "date_range":
        start_date = args.start_date
        end_date = args.end_date
        output_file = args.output_file

        date_range = get_date_range(start_date, end_date)

        geojson_urls = get_geojson_urls(date_range)

        troop_df = get_troop_data(geojson_urls, get_column_names(date_range))
        troop_df.to_csv(f"data/{output_file}.csv", index=False)
        print(f"{args.output_file}.csv successfully saved to the /data folder!")
    
    # Command for manually providing a list of dates from which to collect GeoJSON URLs
    if args.command == "date_list":
        output_file = args.output_file
        dates = args.dates
        
        parsed_dates = [parse_date(date) for date in dates]
        
        geojson_urls = get_geojson_urls(parsed_dates)

        troop_df = get_troop_data(geojson_urls, get_column_names(dates))
        troop_df.to_csv(f"data/{output_file}.csv", index=False)
        print(f"{args.output_file}.csv successfully saved to the /data folder!")
    
    # Command to merge two DataFrames in order to add more dates
    if args.command == "merge_data":
        file1 = f"data/{args.file1}.csv"
        file2 = f"data/{args.file2}.csv"
        output_file = f"data/merged/{args.output_file}.csv"

        add_date_column(file1, file2, output_file)
        print(f"{args.output_file}.csv successfully saved to the /data/merged folder!")
    
    # Command to only keep the English names in the column 'Militaire eenheid'
    if args.command == "clean_names":
        csv_file = f"data/{args.csv_file}.csv"
        output_file = f"data/clean/{args.output_file}.csv"

        clean_unit_names(csv_file, output_file)
        print(f"{args.output_file}.csv successfully saved to the /data/clean folder!")
    
    # Command to calculate the average movement between coordinates for the Russian troops
    if args.command == "total_movement":
        csv_file = f"data/{args.csv_file}.csv"
        output_file = f"data/{args.output_file}.csv"

        calculate_total_movement(csv_file, output_file)
        print(f"{args.output_file}.csv successfully saved to the /data folder!")
