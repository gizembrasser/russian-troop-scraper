# Retrieve data from DeepStateMAP

This program allows you to retrieve data on Russian troop positions for specific dates or range of dates. The program will fetch the coordinates for each date and names of the military units provided by the [DeepStateMAP](https://deepstatemap.live/#8/51.1569543/34.6343994) API, and save it to a CSV file for further analysis.

## Requirements

To run this program, you will need:

1. Python: Make sure Python is installed on your computer. You can download it [here](https://www.python.org/downloads/).

2. Command Line Interface (CLI): You will need to use the terminal or command prompt to run the program.

## Installation

Before you start, you'll need to set up your computer to run the program. Follow these steps:

1. Get the program files from the source (e.g., download from this repository).

2. Open your terminal or command prompt in the folder where the program files are saved.

3. In the terminal, run the following command to install the required Python libraries:

```
pip install -r requirements.txt
```

## How to use the program

Open the Command Line in the folder containing the program files, or navigate to it using the `cd` command:

```
cd path/to/program/folder
```

The program support several subcommands for different operations. The output will be saved to the `/data` folder:

### 1. Collect data from a date range

To collect data on Russian troops from a range of dates, use the following commmand. Provide the start date, end date and a name for the output CSV file:

```
python main.py date_range 2024-09-01 2024-09-05 <output_file>
```

- `start_date`: The start date in yyyy-mm-dd format.
- `end_date`: The end date in yyyy-mm-dd format.
- `output_file`: The name of the output CSV file (without extension).

### 2. Collect data from a list of dates

To collect data on Russian troops for specific dates, use the following command. Provide a name for the output CSV file and a list of dates (separated by spaces):

```
python main.py date_list <output_file> 2024-07-01 2024-08-01 2024-09-01
```

- `output_file`: The name of the output CSV file (without extension).
- `dates`: A list of dates in yyyy-mm-dd format.

*Note: be sure to manually check if all dates were written to the CSV file, as DeepStateMAP doesn't record data every single day.* 

### 3. Merge data from two CSV files

To merge two CSV files and add more date columns, use the following command:

```
python main.py merge_data <file1> <file2> <output_file>
```

- `file1`: The first CSV file (without extension).
- `file2`: The second CSV file (without extension).
- `output_file`: The name of the merged output CSV file (without extension).

### 4. Clean military unit names

To clean the Ukrainian names from the 'Militaire eenheid' column and keep only the English names, use this command:

```
python main.py clean_names <csv_file> <output_file>
```

- `csv_file`: The input CSV file to clean (without extension).
- `output_file`: The name of the output CSV file (without extension).

### 5. Calculate total movement per troop

To calculate the total movement (in kilometers) for each troop from a CSV file of coordinates, use the following command:

```
python main.py total_movement <csv_file> <output_file>
```

- `csv_file`: The input CSV file containing coordinates (without extension) and more than one date column.
- `output_file`: The name of the output CSV file (without extension).

## R analysis

The `/project` folder contains R code files used to conduct the analysis. These files will print some handy statistics about the data to the console.

The `/visuals/maps` folder contains maps of Ukraine and the surrounding area with military units plotted over time, created by R's leaflet library. Right-click on one of the HTML files and select 'Copy Path', paste the URL into a browser in order to view the map.

The `/visuals/graphs` folder