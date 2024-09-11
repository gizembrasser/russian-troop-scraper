import pandas as pd


def add_date_column(file1, file2, output_file):
    """
    Merges two CSV files based on the 'Militaire eenheid' column and sorts the date columns from earliest to latest.
    Saves the result to a new CSV file.
    """
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    merged_df = pd.merge(df1, df2, on='Militaire eenheid', how='outer')

    # Identify date columns and sort them in ascending order
    date_columns = [col for col in merged_df.columns if col != 'Militaire eenheid' and pd.to_datetime(col, format='%Y-%m-%d', errors='coerce') is not pd.NaT]
    sorted_columns = ['Militaire eenheid'] + sorted(date_columns, key=lambda x: pd.to_datetime(x))

    sorted_df = merged_df[sorted_columns]

    sorted_df.to_csv(output_file, index=False)


def clean_unit_names(csv_file, output_file):
    """
    Reads a CSV file, keeps only the English name in the 'Militaire eenheid' column, and saves the result to a new CSV file.
    """
    df = pd.read_csv(csv_file)

    df['Militaire eenheid'] = df['Militaire eenheid'].apply(lambda x: x.split('///')[-1].strip() if '///' in x else x.strip())

    df.to_csv(output_file, index=False)

