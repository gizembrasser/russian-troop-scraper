import pandas as pd


def add_date_column(file1, file2, output_file):
    """
    Merges two CSV files based on the 'Militaire eenheid' column and sorts the date columns from earliest to latest.
    Saves the result to a new CSV file.
    """
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    merged_df = pd.merge(df1, df2, on='Militaire eenheid', how='outer')

    # For columns common to both, use the values from df1
    for col in df1.columns:
        if col in df2.columns and col != 'Militaire eenheid':
            merged_df[col] = merged_df[col + '_x'].combine_first(merged_df[col + '_y'])
            merged_df.drop(columns=[col + '_x', col + '_y'], inplace=True)

    # Identify date columns and sort them in ascending order
    date_columns = [col for col in merged_df.columns if col != 'Militaire eenheid' and pd.to_datetime(col, format='%Y-%m-%d', errors='coerce') is not pd.NaT]
    sorted_columns = ['Militaire eenheid'] + sorted(date_columns, key=lambda x: pd.to_datetime(x))

    sorted_df = merged_df[sorted_columns + [col for col in merged_df.columns if col not in sorted_columns]]

    sorted_df.to_csv(output_file, index=False)
    return sorted_df


def clean_unit_names(csv_file, output_file):
    """
    Reads a CSV file, keeps only the English name in the 'Militaire eenheid' column, and saves the result to a new CSV file.
    """
    df = pd.read_csv(csv_file)

    df['Militaire eenheid'] = df['Militaire eenheid'].apply(lambda x: x.split('///')[-1].strip() if '///' in x else x.strip())

    df.to_csv(output_file, index=False)
    return df


def match_units(df):
    """
    Reads a CSV file, finds duplicate rows in the 'Militaire eenheid' column, and fills missing values 
    in one row with values from another row where data is available.
    """
    grouped = df.groupby("Militaire eenheid")

    # Iterate through each group and fill missing values in-place
    for _, group in grouped:
        if len(group) > 1:
            # Forward and backward fill the msising values in each group
            filled_group = group.ffill().bfill()

            # Update only missing values in the original dataframe
            for idx in group.index:
                for col in group.columns:
                    if pd.isna(df.loc[idx, col]):
                        df.loc[idx, col] = filled_group.loc[idx, col]
    
    # Remove duplicate rows based on 'Militaire eenheid'
    df = df.drop_duplicates(subset="Militaire eenheid", keep="first")             
    return df

