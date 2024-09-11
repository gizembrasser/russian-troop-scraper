# Retrieve data from DeepStateMAP

This program allows you to retrieve data on Russian troop positions for a specific date or range of dates. The program will fetch the coordinates for each date and names of the military units provided by the [DeepStateMAP](https://deepstatemap.live/#8/51.1569543/34.6343994) API, and save it to a CSV file for further analysis.

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

1. Open the Command Line in the folder containing the program files. Or navigate to it using the `cd` command:

```
cd path/to/program/folder
```

2. Run the program using the following command. You will be prompted to provide a range of dates and a name for the CSV file.

```
python main.py
```

3. After running the program, the troop data will be written to a CSV file in the `/data` folder.
