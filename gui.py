#Code for the gui using tkinter
import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from plotting import generate_selected_chart
from data_handler import  load_csv, format_column_headers, find_missing_tuesdays, detect_request_anomalies, detect_play_anomalies, get_play_date_range, data_analysis
from data_handler import get_tab_df, get_play_df, get_req_df, data_flags


def show_main_screen(root):
    """Displays the main screen with greeting and buttons."""
    for widget in root.winfo_children():
        widget.destroy()
        
    #UI grid configuration
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)

    greet_msg1 = tk.Label(root, text="Data Analysis for Ukulele Tuesday Band", font = ("Arial", 12, "bold"))
    greet_msg1.grid(row=0, column=0, columnspan=3, padx=10, pady=(20, 5), sticky="ew")
    
    greet_msg2 = tk.Label(root, text="Hi, let's start analyzing the data together!")
    greet_msg2.grid(row=1, column=0, columnspan=3, padx=10, pady=(20, 5), sticky="ew")
       
    greet_msg3 = tk.Label(root, text="First, load all the three databases.")
    greet_msg3.grid(row=2, column=0, columnspan=3, padx=10, pady=(3, 5), sticky="ew")

    greet_msg4 = tk.Label(root, text="Enter or select the CSV File Path for each database")
    greet_msg4.grid(row=3, column=0, columnspan=3, padx=10, pady=(25, 10), sticky="w")

    create_db_widgets(root,"Tab Database", 4)
    create_db_widgets(root,"Play Database", 5)
    create_db_widgets(root,"Request Database", 6)

    next_button_1 = tk.Button(root, text="Next", command= lambda: go_to_next_screen(root))
    next_button_1.grid(row=7, column=0, padx=10, pady=(100, 5), sticky="w")

    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.grid(row=7, column=3, padx=10, pady=(100, 5), sticky="e")

def create_db_widgets(root, db_name, row):
    """Create seperate widgets for selecting and loading a database."""
    load_msg = tk.Label(root, text=f"{db_name}:")
    load_msg.grid(row=row, column=0, padx=10, pady=(5, 5), sticky="w")

    filepath = tk.StringVar()  #Calling different variable for each database
    data_entry = tk.Entry(root, textvariable=filepath, width=50)
    data_entry.grid(row=row, column=1, padx=10, pady=(5, 5), sticky="w")

    browse_button = tk.Button(root, text="Browse", command=lambda: browse_file(filepath))
    browse_button.grid(row=row, column=2, padx=5, pady=(5, 5), sticky="w")

    load_button = tk.Button(root, text="Load CSV", command=lambda: load_csv(db_name, filepath))
    load_button.grid(row=row, column=3, padx=5, pady=(5, 5), sticky="w")

def browse_file(filepath):
    """Open a file dialog to browse and select a CSV file."""
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        filepath.set(file_path)

def go_to_next_screen(root):
    """Switch to the next screen if all databases are loaded."""
    if data_flags['tab_data_loaded'] and data_flags['play_data_loaded'] and data_flags['req_data_loaded']:
        second_screen(root)
    else:
        messagebox.showwarning("Warning", "Please load all databases before proceeding.")

def second_screen(root):
    '''Content of second screen'''
    for widget in root.winfo_children():
        widget.destroy()
    
    next_screen_label = tk.Label(root, text="Let's get into Data Analysis", font = ("Arial", 12, "bold"))
    next_screen_label.grid(row=0, column=0, columnspan=3, padx=10, pady=(20, 5), sticky="ew")
    
    decision_label = tk.Label(root, text="Select the task that you would like to perform")
    decision_label.grid(row=1, column=0, columnspan=3, padx=10, pady=(20, 5), sticky="ew")

    data_summary_label = tk.Label(root, text="Data Summary: Summarizes the overall data and peforms the basic checks")
    data_summary_label.grid(row=2, column=0, columnspan=2, padx=10, pady=(20, 5), sticky="w")

    data_summary_button = tk.Button(root, text="Data Summary", command=lambda: data_summary_screen(root))
    data_summary_button.grid(row=2, column=2, pady=(20, 5), sticky="w")

    query_label = tk.Label(root, text="Data Querying: Queries the data based on the user specified date and column ranges")
    query_label.grid(row=3, column=0, columnspan=2, padx=10, pady=(20, 5), sticky="w")   

    query_button = tk.Button(root, text="Data Querying", command= lambda: query_screen(root))
    query_button.grid(row=3, column=2, pady=(20, 5), sticky="w")

    vislz_label = tk.Label(root, text="Data Visualization: Generates plots to understand the data better")
    vislz_label.grid(row=4, column=0, columnspan=2, padx=10, pady=(20, 5), sticky="w")

    vislz_button = tk.Button(root, text="Data Visualization", command= lambda: visualization_screen(root))
    vislz_button.grid(row=4, column=2, pady=(20, 5), sticky="w")

    back_button = tk.Button(root, text="Back", command= lambda: show_main_screen(root))
    back_button.grid(row=5, column=0, padx=10, pady=(70, 5), sticky="w")

    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.grid(row=5, column=3, padx=10, pady=(100, 5), sticky="e")

def data_summary_screen(root):
    """Part 1 of Data summary screen with Data Dictionary, First 10 rows, and data types."""
    tab_df = get_tab_df()
    play_df = get_play_df()
    req_df = get_req_df()
    
    for widget in root.winfo_children():
        widget.destroy()

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)

    main_title = tk.Label(root, text="Data Summary (1/2)", font=("Arial", 12, "bold"))
    main_title.grid(row=0, column=0, columnspan=3, padx=10, pady=(20, 5), sticky="ew")
    
    content_title = tk.Label(root, text="Information on Data Dictionary, First 10 rows and Data Types")
    content_title.grid(row=1, column=0, columnspan=3, padx=10, pady=(10, 5), sticky="ew")

    add_data_dictionary(root,"Tab Database", 0, "Tab_data_dict.txt")
    add_data_dictionary(root,"Play Database", 1, "Play_data_dict.txt")
    add_data_dictionary(root,"Request Database", 2, "Request_data_dict.txt")
    
    table_head_type(root,"Tab Database", tab_df, 0)
    table_head_type(root,"Play Database", play_df, 1, is_melt=True, melt_value_name="play order")
    table_head_type(root,"Request Database", req_df, 2, is_melt=True, melt_value_name="request type")

    insights_button = tk.Button(root, text="More Insights", command=lambda: more_insights_screen(root))
    insights_button.grid(row=5, column=1, padx=5, pady=(10, 5), sticky="ew")

    back_button = tk.Button(root, text="Back", command=lambda: second_screen(root))
    back_button.grid(row=5, column=0, padx=5, pady=(10, 5), sticky="w")

    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.grid(row=5, column=2, padx=5, pady=(10, 5), sticky="e")

def add_data_dictionary(root, db_name, col, file_name):
    """Function to add a data dictionary section for a given database."""
    frame = tk.Frame(root, padx=5, pady=5)
    frame.grid(row=2, column=col, sticky="nsew")

    label = tk.Label(frame, text=f"Data Dictionary for {db_name}", font=("Arial", 9, "bold"))
    label.pack(pady=2)

    text_widget = tk.Text(frame, wrap="word", height=6, width=30)
    text_widget.pack(side="left", fill="both", expand=True)

    vsb = tk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
    text_widget.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")

    # Constructing the file path in the current directory
    file_path = os.path.join(os.path.dirname(__file__), file_name) 
    
    # Trying to open the data dictionary file and displaying it
    try:
        with open(file_path, "r") as file:
            text_widget.insert(tk.END, file.read())
        text_widget.configure(state="disabled")  # Make the text read-only
    except FileNotFoundError:
        text_widget.insert(tk.END, f"Error: {file_name} not found in the current directory.")
        text_widget.configure(state="disabled")
    except Exception as e:
        text_widget.insert(tk.END, f"Error loading data dictionary: {e}")
        text_widget.configure(state="disabled")


def table_head_type(root, db_name, df, col, is_melt=False, melt_value_name="value"):
    '''Function for displaying first 10 rows and data types of each database'''
    if not isinstance(df, pd.DataFrame) or df.empty:
        error_label = tk.Label(root, text=f"{db_name} not loaded or empty.", fg="red", font=("Arial", 8))
        error_label.grid(row=col, column=0, columnspan=3, pady=5, sticky="ew")
        return  # Exit if DataFrame is invalid
    
    frame = tk.Frame(root, padx=5, pady=5)
    frame.grid(row=3, column=col, sticky="nsew")

    db_label = tk.Label(frame, text=f"First 10 rows of {db_name}", font=("Arial", 9, "bold"))
    db_label.pack(pady=2)

    #Removing tabber column for data privacy protection and formatting the date columns
    if db_name == "Tab Database":
        if "tabber" in df.columns:
            df = df.drop(columns=["tabber"])
        if "date" in df.columns:
            df["date"] = df["date"].apply(lambda x: str(int(x)) if not pd.isnull(x) else x)

    #Reshaping the play and request dataframe for easier data handling
    if is_melt and isinstance(df, pd.DataFrame) and not df.empty:
        id_vars = ['song', 'artist'] if 'song' in df.columns and 'artist' in df.columns else df.columns[:2].tolist()
        df = pd.melt(df, id_vars=id_vars, var_name='date', value_name=melt_value_name)
        df = df.dropna(subset=[melt_value_name])

    #data head display
    if isinstance(df, pd.DataFrame) and not df.empty:
        tree_frame = tk.Frame(frame, width=300, height=150)
        tree_frame.pack_propagate(False)
        tree_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(tree_frame, columns=list(df.columns), show='headings', height=6)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=hsb.set)
        hsb.pack(side="bottom", fill="x")
        tree.pack(fill="both", expand=True)

        for col_name in df.columns:
            tree.heading(col_name, text=col_name)
            tree.column(col_name, width=80, anchor='center')

        for index, row in df.head(10).iterrows():
            tree.insert("", tk.END, values=list(row))
    else:
        error_label = tk.Label(frame, text=f"{db_name} not loaded or empty.", fg="red", font=("Arial", 8))
        error_label.pack(pady=2)
    
    #data types display
    dtype_frame = tk.Frame(frame, padx=2, pady=2)
    dtype_frame.pack(fill="both", expand=True)

    dtype_label = tk.Label(dtype_frame, text=f"Data Types of {db_name}", font=("Arial", 9, "bold"))
    dtype_label.pack(pady=2)

    dtype_text = tk.Text(dtype_frame, wrap="none", width=30, height=6)
    dtype_text.pack(side="left", fill="both", expand=True)

    vsb = ttk.Scrollbar(dtype_frame, orient="vertical", command=dtype_text.yview)
    dtype_text.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")

    #displaying data types
    if isinstance(df, pd.DataFrame) and not df.empty:
        dtype_text.insert(tk.END, df.dtypes.to_string())
    else:
        dtype_text.insert(tk.END, f"{db_name} not loaded.")

def more_insights_screen(root):
    """Display Missing Values and Anomalies in the More Insights screen."""
    for widget in root.winfo_children():
        widget.destroy()

    main_title = tk.Label(root, text="Data Summary (2/2)", font=("Arial", 12, "bold"))
    main_title.grid(row=0, column=0, columnspan=3, padx=10, pady=(20, 5), sticky="ew")
    
    content_title = tk.Label(root, text="Information on Missing Data, Data Anomalies and Date Range")
    content_title.grid(row=1, column=0, columnspan=3, padx=10, pady=(10, 5), sticky="ew")

    display_tab_missing_values_and_missing_tuesdays(root)

    anomalies_title = tk.Label(root, text="Anomalies in the Data", font=("Arial", 10, "bold"))
    anomalies_title.grid(row=3, column=0, columnspan=3, pady=5)

    display_anomalies_side_by_side(root)

    display_play_date_range(root)

    back_button = tk.Button(root, text="Back", command=lambda: data_summary_screen(root))
    back_button.grid(row=7, column=0, padx=5, pady=5, sticky="w")

    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.grid(row=7, column=2, padx=5, pady=5, sticky="e")

def display_tab_missing_values_and_missing_tuesdays(root):
    """Display missing values of Tab Database and missing Tuesdays side by side."""
    tab_df = get_tab_df()
    play_df = get_play_df()
    parent_frame = tk.Frame(root, padx=5, pady=5)
    parent_frame.grid(row=2, column=0, columnspan=3, sticky="ew")

    parent_frame.grid_columnconfigure(0, weight=1)
    parent_frame.grid_columnconfigure(1, weight=1)

    #Missing Values of Tab Database in Left frame: 
    left_frame = tk.Frame(parent_frame, padx=5, pady=5)
    left_frame.grid(row=0, column=0, sticky="nsew")

    missing_label = tk.Label(left_frame, text="Count of missing values per column of Tab Database", font=("Arial", 9, "bold"))
    missing_label.pack(pady=2)

    #displaying the missing values for each column of tab database
    if isinstance(tab_df, pd.DataFrame) and not tab_df.empty:
        missing_values = tab_df.isnull().sum()
        missing_df = pd.DataFrame(missing_values, columns=['Missing Values']).reset_index()
        missing_df.columns = ['Column', 'Missing Values']

        tree = ttk.Treeview(left_frame, columns=list(missing_df.columns), show='headings', height=6)
        for col_name in missing_df.columns:
            tree.heading(col_name, text=col_name)
            tree.column(col_name, width=120, anchor='center')
        for _, row in missing_df.iterrows():
            tree.insert("", tk.END, values=list(row))
        tree.pack(fill="both", expand=True)
    else:
        empty_label = tk.Label(left_frame, text="No missing values or Tab Database not loaded", fg="gray", font=("Arial", 9))
        empty_label.pack()

    #Missing Tuesdays in Right frame
    right_frame = tk.Frame(parent_frame, padx=5, pady=5)
    right_frame.grid(row=0, column=1, sticky="nsew")

    missing_tuesdays_label = tk.Label(right_frame, text="Tuesdays for which we don't have data!", font=("Arial", 9, "bold"))
    missing_tuesdays_label.pack(pady=2)

    tuesdays_textbox = tk.Text(right_frame, wrap="word", height=6, width=40)
    tuesdays_textbox.pack(fill="both", expand=True)

    missing_tuesdays_message = find_missing_tuesdays(play_df)
    
    tuesdays_textbox.insert(tk.END, missing_tuesdays_message)
    tuesdays_textbox.configure(state="disabled")

def display_anomalies_side_by_side(root):
    """Display anomalies for both Request and Play Databases side by side."""
    play_df = get_play_df()
    req_df = get_req_df()
    parent_frame = tk.Frame(root, padx=5, pady=5)
    parent_frame.grid(row=4, column=0, columnspan=3, sticky="ew")

    parent_frame.grid_columnconfigure(0, weight=1)
    parent_frame.grid_columnconfigure(1, weight=1)

    #Request Database anomalies in Left frame
    left_frame = tk.Frame(parent_frame, padx=5, pady=5)
    left_frame.grid(row=0, column=0, sticky="nsew")

    request_label = tk.Label(left_frame, text="Anomalies in Request Database", font=("Arial", 9, "bold"))
    request_label.pack(pady=2)

    request_text = tk.Text(left_frame, wrap="word", height=6, width=40)
    request_text.pack(fill="both", expand=True)

    #calling the function and displaying the data anomalies
    request_anomalies = detect_request_anomalies(req_df)
    if request_anomalies:
        request_text.insert(tk.END, "\n".join(request_anomalies))
    else:
        request_text.insert(tk.END, "No anomalies found in Request Database.")
    request_text.configure(state="disabled")

    #Play Database anomalies in Right frame: 
    right_frame = tk.Frame(parent_frame, padx=5, pady=5)
    right_frame.grid(row=0, column=1, sticky="nsew")

    play_label = tk.Label(right_frame, text="Anomalies in Play Database", font=("Arial", 9, "bold"))
    play_label.pack(pady=2)

    play_text = tk.Text(right_frame, wrap="word", height=6, width=40)
    play_text.pack(fill="both", expand=True)

    #calling the function and displaying the data anomalies
    play_anomalies = detect_play_anomalies(play_df)
    if play_anomalies:
        play_text.insert(tk.END, "\n".join(play_anomalies))
    else:
        play_text.insert(tk.END, "No anomalies found in Play Database.")
    play_text.configure(state="disabled")

def display_play_date_range(root):
    """Display the date range dynamically in the More Insights screen."""
    play_df = get_play_df()
    range_message = get_play_date_range(format_column_headers(play_df.copy()))

    date_range_heading = tk.Label(root, text="Range of Dates Where Songs Were Played", font=("Arial", 10, "bold"))
    date_range_heading.grid(row=5, column=0, columnspan=3, pady=5, sticky="ew")

    date_range_label = tk.Label(root, text=range_message, font=("Arial", 9))
    date_range_label.grid(row=6, column=0, columnspan=3, pady=5, sticky="ew")

def query_screen(root):
    '''Content of data querying screen'''
    tab_df = get_tab_df()
    for widget in root.winfo_children():
        widget.destroy()

    query_label = tk.Label(root, text="Data Querying", font=("Arial", 12, "bold"))
    query_label.grid(row=0, column=0, columnspan=3, padx=10, pady=(20, 5), sticky="ew")

    datefilter_label = tk.Label(root, text="Enter the range of dates('dd-mm-yyyy') where the songs were played(By default, entire range is selected):")
    datefilter_label.grid(row=1, column=0, columnspan=2, padx=10, pady=(20, 5), sticky="w")

    start_date_entry = tk.Entry(root)
    start_date_entry.grid(row=1, column=2, columnspan=1, padx=10, pady=(20, 5), sticky="w")

    end_date_entry = tk.Entry(root)
    end_date_entry.grid(row=1, column=4, columnspan=1, padx=10, pady=(20, 5), sticky="w")

    columnfilter_label = tk.Label(root, text="Select the columns to filter the result by (can select multiple columns):")
    columnfilter_label.grid(row=3, column=0, columnspan=2, padx=10, pady=(50, 5), sticky="w")
       
    # Create a Listbox for selecting multiple columns
    tabdf_columns = [col for col in tab_df.columns if col != 'tabber']
    columns_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=5, width=20)
    for column in tabdf_columns:
        columns_listbox.insert(tk.END, column)
    columns_listbox.grid(row=3, column=2, columnspan=5, padx=10, pady=5, sticky="w")

    apply_button = tk.Button(root, text="Apply the filters and display the data", 
                             command=lambda: data_analysis(root,start_date_entry, end_date_entry, columns_listbox))
    apply_button.grid(row=4, column=1, columnspan=2, padx=10, pady=(40, 5), sticky="ew")

    back_button = tk.Button(root, text="Back", command=lambda: second_screen(root))
    back_button.grid(row=5, column=0, padx=10, pady=(70, 5), sticky="w")

    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.grid(row=5, column=6, padx=10, pady=(100, 5), sticky="e")

def visualization_screen(root):
    """Screen for selecting a single chart to display with category options."""
    for widget in root.winfo_children():
        widget.destroy()
    
    greet_msg = tk.Label(root, text="Data Visualizations", font=("Arial", 12, "bold"))
    greet_msg.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

    # Chart selection radio buttons
    chart_var = tk.StringVar(value= "Histogram of Songs by Difficulty")
    chart_options = [
        "Histogram of Songs by Difficulty",
        "Histogram of Songs by Duration",
        "Bar Chart of Songs by Language",
        "Bar Chart of Songs by Source",
        "Bar Chart of Songs by Decades",
        "Cumulative Line Chart of Songs Played",
        "Donut Chart of Songs by Categorical Columns"
        ]
    for i, chart_name in enumerate(chart_options, start=1):
        chart_radiobutton= tk.Radiobutton(root, text=chart_name, variable=chart_var, value=chart_name)
        chart_radiobutton.grid(row=i, column=1, columnspan=3, padx=10, pady=5, sticky="w")

    # Category selection for charts
    generate_lable = tk.Label(root, text="Select Categorical Filter for the Charts")
    generate_lable.grid(row=9, column=0, padx=10, pady=10, sticky="w")
    
    category_var = tk.StringVar(value="gender")
    generate_menu = tk.OptionMenu(root, category_var,"no category", "gender", "language", "type", "source")
    generate_menu.grid(row=9, column=1, padx=10, pady=5, sticky="w")

    generate_button= tk.Button(root, text="Generate Chart", command=lambda: generate_selected_chart(root,chart_var.get(), category_var.get()))
    generate_button.grid(row=9, column=2, padx=10, pady=20, sticky="e")

    back_button = tk.Button(root, text="Back", command=lambda: second_screen(root))
    back_button.grid(row=11, column=0, padx=10, pady=(70, 5), sticky="w")
    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.grid(row=11, column=2, padx=10, pady=(70, 5), sticky="e")


