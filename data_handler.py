#Code for all the functions in Data Summary and Data Querying Screen
import pandas as pd
import numpy as np
from utils import data_display
from collections import defaultdict
from tkinter import messagebox

# Global DataFrames for storing loaded data
tab_df = None  # DataFrame for Tab Database
play_df = None  # DataFrame for Play Database
req_df = None  # DataFrame for Request Database

# Mutable dictionary to store database load flags
data_flags = {
    "tab_data_loaded": False,
    "play_data_loaded": False,
    "req_data_loaded": False,
}

def load_csv(db_name, filepath):
    """Load the CSV file and show a pop-up window with success or error message."""
    global tab_df, play_df, req_df
    try:
        file_path = filepath.get()
        df = pd.read_csv(file_path)
        if db_name == "Tab Database":
            tab_df = df
            update_data_loaded_flag(db_name)
        elif db_name == "Play Database":
            play_df = df
            update_data_loaded_flag(db_name)
        elif db_name == "Request Database":
            req_df = df
            update_data_loaded_flag(db_name)
        messagebox.showinfo("Success", f"{db_name} loaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Unable to load {db_name}: {e}")


def update_data_loaded_flag(db_name):
    """Update the data loaded flags based on database name."""
    global data_flags
    if db_name == "Tab Database":
        data_flags['tab_data_loaded'] = True
    elif db_name == "Play Database":
        data_flags['play_data_loaded'] = True
    elif db_name == "Request Database":
        data_flags['req_data_loaded'] = True

def correct_language(data):
    """Correct and explode the language column in Tab Database."""
    data['language'] = data['language'].str.split(',')  # Split languages into lists
    data = data.explode('language')  # Flatten the DataFrame
    data['language'] = data['language'].str.strip()
    data.dropna(subset=['language'], inplace=True)
    return data

def format_column_headers(df):
    """Format date column headers from yyyymmdd to yyyy/mm/dd."""
    formatted_columns = {}
    for col in df.columns:
        try:
            if col.isdigit() and len(col) == 8:  #Ensuring header is a numeric with 8 digits
                formatted_columns[col] = f"{col[:4]}/{col[4:6]}/{col[6:]}"  #Formating as yyyy/mm/dd
            else:
                formatted_columns[col] = col
        except Exception as e:
            formatted_columns[col] = col

    return df.rename(columns=formatted_columns, inplace=False)

def find_missing_tuesdays(play_df):
    """Find Tuesdays where no songs were played using a formatted dateframe."""
    formatted_play_df = format_column_headers(play_df.copy())  # Use a formatted copy
    date_columns = [
        col for col in formatted_play_df.columns if len(col) == 10 and col.count("/") == 2
    ]
    if not date_columns:
        return "No valid date columns found in the Play Database."

    min_date = min(date_columns)
    max_date = max(date_columns)
    all_dates = pd.date_range(start=min_date, end=max_date, freq='W-TUE')
    formatted_tuesdays = all_dates.strftime("%Y/%m/%d").tolist()

    #Displying missing tuesdays
    missing_tuesdays = [date for date in formatted_tuesdays if date not in date_columns]
    if missing_tuesdays:
        return f"Tuesdays with no songs played:\n{', '.join(missing_tuesdays)}"
    return "All Tuesdays in the range had songs played."

def detect_request_anomalies(req_df):
    """Detect anomalies in the Request Database and group them."""
    grouped_anomalies = defaultdict(list)  # Group dates by invalid requester values using inbuilt defaultdict()

    #getting all values that are not "A" or "G" from Request database along with thier respective requested_date
    if isinstance(req_df, pd.DataFrame) and not req_df.empty:
        req_df = format_column_headers(req_df)  # Format dates
        # Identify date columns
        date_columns = [
            col for col in req_df.columns if (col.isdigit() and len(col) == 8) or (len(col) == 10 and col.count("/") == 2)
        ]
        # Check for invalid requester values
        for col in date_columns:
            invalid_values = req_df[col].dropna().apply(lambda x: str(x).strip()).unique()

            for value in invalid_values:
                if value not in ['A', 'G']:
                    grouped_anomalies[value].append(col)

    # Group anomalies for display
    anomalies = [
        f"[{', '.join(dates)}] have the invalid requester value: {value}.\n"
        for value, dates in grouped_anomalies.items()
    ]

    return anomalies

def detect_play_anomalies(play_df):
    """Detect anomalies in the Play Database and group them."""
    anomalies = []

    #getting all dates from Play database that had incorrect song order 
    if isinstance(play_df, pd.DataFrame) and not play_df.empty:
        play_df = format_column_headers(play_df)  # Format dates

        decimal_anomalies = []
        same_order_anomalies = []

        for col in play_df.columns:
            # Check for decimal values in play order
            decimal_values = play_df[col].dropna().apply(lambda x: isinstance(x, float) and not x.is_integer())
            if decimal_values.any():
                decimal_anomalies.append(col)

            # Check for same play order across all rows for a date
            unique_values = play_df[col].dropna().nunique()
            if unique_values == 1:
                same_order_anomalies.append(col)

        # Group anomalies for display
        if decimal_anomalies:
            anomalies.append(f"[{', '.join(decimal_anomalies)}] \n The above dates contain decimal values as play orders.")
        if same_order_anomalies:
            anomalies.append(f"\n[{', '.join(same_order_anomalies)}] \n The above dates have the same play order for all the songs played that day.")
    
    return anomalies

def get_play_date_range(play_df):
    """Return the range of dates (yyyy/mm/dd) based on the column headers of the Play Database."""

    # Identify columns with the format yyyy/mm/dd
    play_dates = [
        col.strip() for col in play_df.columns
        if len(col.strip()) == 10 and col.strip().count("/") == 2
    ]

    if play_dates:
        # Find the maximum and minimum dates
        min_date = min(play_dates)
        max_date = max(play_dates)
        return f"Database has songs that were played between {min_date} and {max_date}."
    else:
        return "No valid date columns found in the Play Database."
    
def data_analysis(root,start_date_entry, end_date_entry, columns_listbox):
    global tab_df, play_df, req_df

    #Formatting the databases for easier data handling
    melted_play_df = play_df.melt(id_vars=['song', 'artist'], var_name='played_date', value_name='song_order')
    melted_req_df = req_df.melt(id_vars=['song', 'artist'], var_name='request_date', value_name='requester')
    merged_df = pd.merge(melted_play_df, melted_req_df, left_on=['song', 'artist', 'played_date'], right_on=['song', 'artist', 'request_date'], how='inner')
    tab_df_v1 = tab_df.copy() #creating a version to not make issues in other screen

    #deleting null value rows from merged_df to keep the data small and easier to work with
    merged_df = merged_df[(merged_df['song_order'].notna()) & (merged_df['requester'].notna())]

    merged_df['requester'] = np.where(
        merged_df['requester'].str.contains('A', case=False), 'audience',
        np.where(merged_df['requester'].str.contains('G', case=False), 'group', 'unknown')
    )
    merged_df['played_date'] = pd.to_datetime(merged_df['played_date'], format='%Y%m%d', errors='coerce')
    merged_df['request_date'] = pd.to_datetime(merged_df['request_date'], format='%Y%m%d', errors='coerce')
    tab_df_v1['date'] = pd.to_datetime(tab_df_v1['date'], format='%Y%m%d', errors='coerce').dt.date
    #dropping tabber column to protect privacy
    if 'tabber' in tab_df_v1.columns:
        tab_df_v1.drop('tabber', axis=1, inplace=True)

    for column in tab_df_v1.columns:
        if tab_df_v1[column].dtype in ['int64', 'float64']:
            tab_df_v1[column] = tab_df_v1[column].fillna(0)
        else:
            tab_df_v1[column] = tab_df_v1[column].fillna("NA")
       
    #Get start and end dates from the user input
    try:
        start_date_input = start_date_entry.get().strip()
        end_date_input = end_date_entry.get().strip()
        start_date = pd.to_datetime(start_date_input, format='%d-%m-%Y', errors='coerce')
        end_date = pd.to_datetime(end_date_input, format='%d-%m-%Y', errors='coerce')

        #If user date input is in incorrect format, open error box
        if start_date_input and pd.isna(start_date):
            raise ValueError(f"Invalid start date: {start_date_input}. Please enter the date in dd-mm-yyyy format.")
        if end_date_input and pd.isna(end_date):
            raise ValueError(f"Invalid end date: {end_date_input}. Please enter the date in dd-mm-yyyy format.")

        #Select entire range if start or end date is not given (If only start is given last date is considered as end date and vice versa for end date)
        start_date = start_date if start_date_input else merged_df['played_date'].min()
        end_date = end_date if end_date_input else merged_df['played_date'].max()

    except ValueError as e:
        messagebox.showwarning("Invalid Date Format", str(e))
        return
 
    #Filter database based on user selected dates and columns and performing count()
    filtered_merged_df = merged_df[(merged_df['played_date'] >= start_date) & (merged_df['played_date'] <= end_date)]
    
    selected_columns = [columns_listbox.get(i) for i in columns_listbox.curselection()]
    if not selected_columns:  #if no columns are selected, show all columns of tab_df as default
        selected_columns = tab_df_v1.columns.tolist()
    
    base_df = pd.merge(tab_df_v1, filtered_merged_df, on=['song', 'artist'], how='left')
    grouped_df = base_df.groupby(selected_columns).agg(
        count_song_played=('played_date', 'count'),
        count_requested_audience=('requester', lambda x: (x == 'audience').sum()),
        count_requested_group=('requester', lambda x: (x == 'group').sum()),
        count_requested_unknown=('requester', lambda x: (x == 'unknown').sum())
    ).reset_index()
    grouped_df.fillna(0, inplace=True)

    #arguments that are passed to data_display()
    display_columns = grouped_df.columns.tolist()
    data_display(root,grouped_df, display_columns)

def get_tab_df():
    global tab_df
    return tab_df

def get_play_df():
    global play_df
    return play_df

def get_req_df():
    global req_df
    return req_df
