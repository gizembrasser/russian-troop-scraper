# Gather/visualize OSINT on Russian troop locations in Ukraine

This program allows you to retrieve data on Russian troop positions for specific dates and regions. The program will fetch the coordinates for each date and names of the military units provided by the [DeepStateMAP](https://deepstatemap.live/#8/51.1569543/34.6343994) API, and save it to a CSV file for further analysis.

Read about how the program was used in *de Volkskrant* to map troop movements during the Kursk incursion [here](https://www.volkskrant.nl/kijkverder/v/2024/troepenbewegingen-ontleed-russische-troepen-bewegen-nauwelijks-ondanks-de-oekraiense-inval-in-rusland~v1195606/), or click [here](#r-analysis) for more usage examples.

## Requirements

To run this program, you will need:

1. Python: Make sure Python is installed on your computer. You can download it [here](https://www.python.org/downloads/).

2. Command Line Interface (CLI): You will need to use the terminal or command prompt to run the program.

## Installation

Before you start, you'll need to set up your computer to run the program. Follow these steps:

1. Get the program files from the source (e.g., download the zip file from this repository).

2. Open your terminal or command prompt in the folder where the program files are saved.

3. In the terminal, run the following command to install the required Python libraries:

```
pip install -r requirements.txt
```

### Debugging

If the Selenium Chrome WebDriver doesn't work, try one of these fixes:

1. Go to the file `scraper.py` and replace the line:

```python
driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
```

...with this code:

```python
driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
        seleniumwire_options=seleniumwire_options
    )
```

2. You might need to download the [correct version](https://developer.chrome.com/docs/chromedriver/downloads#chromedriver_1140573590) for your Google Chrome. In that case, replace contents of the `driver/` folder in this repo with the right version.
3. Ask ChatGPT 😉

## How to use the program

Open the Command Line in the folder containing the program files, or navigate to it using the `cd` command:

```
cd path/to/program/folder
```

The program supports several subcommands for different operations. The output will be saved to the `/data` folder:

### 1. Collect data from a date range

To collect data on Russian troops from a range of dates, use the `date_range` command. Provide the start date, end date and a name for the output CSV file:

```
python main.py date_range 2024-09-01 2024-09-05 <output_file>
```

- `start_date`: The start date in yyyy-mm-dd format.
- `end_date`: The end date in yyyy-mm-dd format.
- `output_file`: The name of the output CSV file (without extension).

### 2. Collect data from a list of dates

To collect data on Russian troops for specific dates, use the `date_list` command. Provide a name for the output CSV file and a list of dates (separated by spaces):

```
python main.py date_list <output_file> 2024-07-01 2024-08-01 2024-09-01
```

- `output_file`: The name of the output CSV file (without extension).
- `dates`: A list of dates in yyyy-mm-dd format.

> Be sure to manually check if all dates were written to the CSV file, as DeepStateMAP doesn't record data every single day.

### 3. Merge data from two CSV files

To merge two CSV files and add more date columns, use the `merge_data` command:

```
python main.py merge_data <file1> <file2> <output_file>
```

- `file1`: The first CSV file (without extension).
- `file2`: The second CSV file (without extension).
- `output_file`: The name of the merged output CSV file (without extension).

### 4. Clean military unit names

To clean the Ukrainian names from the 'Militaire eenheid' column and keep only the English names, use the `clean_names` command:

```
python main.py clean_names <csv_file> <output_file>
```

- `csv_file`: The input CSV file to clean (without extension).
- `output_file`: The name of the output CSV file (without extension).

### 5. Calculate total movement per troop

To calculate the total movement (in kilometers) for each troop from a CSV file of coordinates, use the `total_movement` command:

```
python main.py total_movement <csv_file> <output_file>
```

- `csv_file`: The input CSV file containing coordinates (without extension) and more than one date column.
- `output_file`: The name of the output CSV file (without extension).

### 6. Collect data per Oblast

To only gather data for one date for a specific Oblast, use the `oblast_data` command. Provide the name of the Oblast, the date and a name for the output CSV file.

```
python main.py oblast_data <oblast_name> <date> <output_file>
```

- `oblast_name`: The name of the Oblast to use as a filter (for example: 'donetsk').
- `date`: A date in yyyy-mm-dd format.
- `output_file`: The name of the output CSV file (without extension).

## R analysis

- The `/project` folder contains R code files used to conduct the analysis. These files will print statistics about the data to the console.

- The `/visuals/maps` folder contains maps of Ukraine and the surrounding area with military units plotted over time, created by R's leaflet library. Right-click on one of the HTML files and select 'Copy Path', paste the URL into a browser in order to view the map.

![](visuals/maps/kursk2024_example.png)

> Movement of Russian troops in Kursk 2024. The hundreds of untrained "Storm-Z" troops (consisting of mostly convicts and volunteers) were excluded from this map for sake of visibility.

- Visuals can be created by uploading datasets collected by the DeepStateMAP scraper to the various `.R` files in the `/project` folder. This folder already includes a few examples for data scraped from 2022, 2023 and 2024.

![](visuals/graphs/2022-2024_aantal_verplaatsingen.png)

> Amount of Russian troops (excluding Storm-Z) that moved more than 10 km per month between 2022 and 2024.