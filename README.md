# Retrieve data from DeepStateMAP

This program allows you to retrieve data on Russian troop positions for a specific date by providing the year, month, and day. The program will fetch the data and save it as a CSV file. The data is provided by [DeepStateMAP](https://deepstatemap.live/#8/51.1569543/34.6343994).

## Requirements

To run this program, you will need:

1. Python: Make sure Python is installed on your computer. You can download it [here](https://www.python.org/downloads/).

2. Command Line Interface (CLI): You will need to use the terminal or command prompt to run the program.

## Installation

Before you start, you'll need to set up your computer to run the program. Follow these steps:

1. Get the program files from the source (e.g., download from a shared link or repository).

2. Open your terminal or command prompt in the folder where the program files are saved..

3. In the terminal, run the following command to install the required Python libraries:

```
pip install - requirements.txt
```

## How to use the program

1. Open the Command Line in the folder containing the program files. Or navigate to it using the `cd` command:

```
cd path/to/program/folder
```

2. Run the program using the following command. You will be prompted to provide a date.

```
python main.py
```

3. After running the program, it will save the troop data in a CSV file in the `/data` folder.