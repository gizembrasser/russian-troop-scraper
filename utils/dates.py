import calendar
from datetime import datetime, timedelta


def parse_date(date_str):
    try:
        # Check if the input is a valid date
        valid_date = datetime.strptime(date_str, "%Y-%m-%d")

        year = valid_date.strftime("%Y")
        month_number = int(valid_date.strftime("%m"))
        day = str(int(valid_date.strftime("%d")))

        month_name = calendar.month_name[month_number] # Get the month name

        return year, month_name, day
    
    except ValueError:
        print("Invalid date format.")


def get_date_range(start_date_str, end_date_str):
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        # Check if the start date is earlier than the end date
        if start_date > end_date:
            print("Start date must be earlier than the end date.")
            return []
        
        # Generate all the dates between start and end date
        current_date = start_date
        date_list = []
        while current_date <= end_date:
            formatted_date = parse_date(current_date.strftime("%Y-%m-%d"))
            date_list.append(formatted_date)
            current_date += timedelta(days=1)
        
        return date_list
    
    except ValueError:
        print("Invalid date format. Please use yyyy-mm-dd.")
        return []


def get_column_names(date_list):
    month_mapping = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04',
        'May': '05', 'June': '06', 'July': '07', 'August': '08',
        'September': '09', 'October': '10', 'November': '11', 'December': '12'
    }

    formatted_dates = []

    for year, month, day in date_list:
        # Convert the month name to the corresponding number
        month_num = month_mapping[month]

        # Format the date as yyyy-mm-dd
        formatted_date = f"{year}-{month_num}-{day.zfill(2)}"
        formatted_dates.append(formatted_date)
    
    return formatted_dates
        