#Code for all the functions in Data Visualisation Screen
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.dates as mdates
from data_handler import get_tab_df,get_play_df, correct_language
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

def validate_category_selection(selected_chart, category):
    '''Defining the categorical varaibales to group the charts'''
    # Define the chart types and the categories they use as primary axes
    chart_axes = {
        "Bar Chart of Songs by Decades": ["decade"],
        "Cumulative Line Chart of Songs Played": ["date"],
        "Donut Chart of Songs by Categorical Columns": [],  
        "Histogram of Songs by Difficulty": ["difficulty"],
        "Histogram of Songs by Duration": ["duration_binned"],
        "Bar Chart of Songs by Language": ["language"],
        "Bar Chart of Songs by Source": ["source"]
    }
    
    # Checking if the selected category is already an axis in the chosen chart and then show an error message
    if category in chart_axes.get(selected_chart, []):
        messagebox.showwarning("Invalid Category Selection", 
                               f"The category '{category}' is already an axis in the '{selected_chart}' chart. "
                               "Please choose a different category.")
        return False  
    return True  

def generate_selected_chart(root,selected_chart, category):
    """Generate a chart based on the selected option and category filter."""
    # Checking if the category is already used as an axis in the selected chart
    if not validate_category_selection(selected_chart, category):
        return  
    
    fig, ax = plt.subplots(figsize=(8,6))
    fig.subplots_adjust(right=0.70)     
    
    #Radio Buttons to call the appropriate plotting function based on the selected chart
    chart_var = tk.StringVar(value="Histogram of Songs by Difficulty")  
    
    if selected_chart == "Histogram of Songs by Difficulty":
        plot_difficulty_histogram(ax, category)
    elif selected_chart == "Histogram of Songs by Duration":
        plot_duration_histogram(ax, category)
    elif selected_chart == "Bar Chart of Songs by Language":
        plot_language_bar_chart(ax, category)
    elif selected_chart == "Bar Chart of Songs by Source":
        plot_source_bar_chart(ax, category)
    elif selected_chart == "Bar Chart of Songs by Decades":
        plot_stacked_bar(ax, category)
    elif selected_chart == "Cumulative Line Chart of Songs Played":
        plot_cumulative_line(ax, category)
    elif selected_chart == "Donut Chart of Songs by Categorical Columns":
        plot_donut_chart(ax, category)   

    display_chart(root,fig)

def plot_difficulty_histogram(ax, category):
    """Plot a histogram of songs by difficulty with optional stacking by category."""
    df = get_tab_df().copy()

    # Handle missing values
    df['language'] = df['language'].fillna('Unknown')

    df = correct_language(df)

    ax.clear()    # Clear any existing plot
    
    min_val = np.floor(df["difficulty"].min()) 
    max_val = np.ceil(df["difficulty"].max())
    bins = list(range(int(min_val), int(max_val) + 1))
    if category in df.columns:
        groups = df[category].unique()
        data = [df[df[category] == group]['difficulty'] for group in groups]
        ax.hist(data, bins=bins, stacked=True, label=groups)

    ax.set_xlabel('Difficulty Level')
    ax.set_ylabel('Number of Songs')
    ax.set_title(f'Songs by Difficulty Level' + (f' by {category.capitalize()}' if category else ''))
    ax.legend(title=category.capitalize(), bbox_to_anchor=(1.05, 1), loc='upper left')
    
    if category == "no category":
        ax.hist(df['difficulty'], bins=bins,color="#0000FF")
        # Set labels and title
        ax.set_xlabel('Difficulty Level')
        ax.set_ylabel('Number of Songs')
        ax.set_title(f'Songs by Difficulty Level' + (f' by {category.capitalize()}' if category and category != "no category" else ''))
      
def plot_duration_histogram(ax, category):
    """Plot a histogram of songs by duration (in minutes) with optional stacking by category."""
    df = get_tab_df().copy()

    # Handle missing values
    df['language'] = df['language'].fillna('Unknown')

    df = correct_language(df)

    ax.clear()
    df['Duration_in_minutes'] = df['duration'].apply(convert_to_minutes)
    df = df.dropna(subset=['Duration_in_minutes'])
    min_val = np.floor(df["Duration_in_minutes"].min()) 
    max_val = np.ceil(df["Duration_in_minutes"].max())
    bins = list(range(int(min_val), int(max_val) + 1))

    if category in df.columns:                           
        groups = df[category].unique()
        data = [df[df[category] == group]['Duration_in_minutes'] for group in groups]
        ax.hist(data, bins=bins, stacked=True, label=groups)
   
    ax.set_xlabel('Duration (minutes)')
    ax.set_ylabel('Number of Songs')
    ax.set_title(f'Songs by Duration' + (f' by {category.capitalize()}' if category else ''))
    ax.legend(title=category.capitalize(), bbox_to_anchor=(1.05, 1), loc='upper left')

    if category == "no category":
        ax.hist(df['Duration_in_minutes'], bins=bins,color="#0000FF")
        # Set labels and title
        ax.set_xlabel('Duration (minutes)')
        ax.set_ylabel('Number of Songs')
        ax.set_title(f'Histogram of Songs by Duration' + (f' by {category.capitalize()}' if category and category != "no category" else ''))

def plot_language_bar_chart(ax, category):
    """Plot a bar chart of songs by language with optional categorization."""
    df = get_tab_df().copy()
    
    # Handle missing values
    df['language'] = df['language'].fillna('Unknown')

    df = correct_language(df)
  
    ax.clear()

    if category in df.columns and category != 'language':
        # Group by language and the selected category, then stack
        data_counts = df.groupby(['language', category]).size().unstack(fill_value=0)
        data_counts.plot(kind='bar', stacked=True, ax=ax)

    else:
        language_counts = df['language'].value_counts()
        ax.bar(language_counts.index, language_counts)
    
    ax.set_xlabel('Language')
    ax.set_ylabel('Number of Songs')
    ax.set_title(f'Bar Chart of Songs by Language' + (f' by {category.capitalize()}' if category else ''))
    ax.legend(title=category.capitalize(), bbox_to_anchor=(1.05, 1), loc='upper left')

    if category == "no category":
        ax.bar(language_counts.index, language_counts.values,color="#0000FF")
        # Set labels and title
        ax.set_xlabel('Language')
        ax.set_ylabel('Number of Songs')
        ax.set_title(f'Bar Chart of Songs by Language' + (f' by {category.capitalize()}' if category and category != "no category" else ''))
        ax.tick_params(axis='x', rotation=90)

def plot_source_bar_chart(ax, category):
    """Plot a bar chart of songs by source with optional categorization."""
    df = get_tab_df().copy()
    
    # Handle missing values
    df['language'] = df['language'].fillna('Unknown')

    df = correct_language(df)

    ax.clear()    # Clear any existing plot

    if category in df.columns and category != 'source':
        data_counts = df.groupby(['source', category]).size().unstack(fill_value=0)
        data_counts.plot(kind='bar', stacked=True, ax=ax)
    else:
        source_counts = df['source'].value_counts()
        ax.bar(source_counts.index, source_counts)

    ax.set_xlabel('Source')
    ax.set_ylabel('Number of Songs')
    ax.set_title(f'Bar Chart of Songs by Source' + (f' by {category.capitalize()}' if category else ''))
    ax.legend(title=category.capitalize(), bbox_to_anchor=(1.05, 1), loc='upper left')

    if category == "no category":
        ax.bar(source_counts.index, source_counts.values,color="#0000FF")
        # Set labels and title
        ax.set_xlabel('Source')
        ax.set_ylabel('Number of Songs')
        ax.set_title(f'Bar Chart of Songs by Source' + (f' by {category.capitalize()}' if category and category != "no category" else ''))

def plot_stacked_bar(ax, category):
    """Plot a bar chart of songs by decade with optional stacking by category."""
    df = get_tab_df().copy()
    
    # Handle missing values
    df['language'] = df['language'].fillna('Unknown')
    
    df = correct_language(df)

  
    ax.clear()  
    # Convert the 'Year' column to decades and remove missing decades
    df['Decade'] = (df['year'] // 10) * 10
    df = df.dropna(subset=['Decade'])

    if category in df.columns:  
        grouped_data = df.groupby(['Decade', category]).size().unstack(fill_value=0)
        grouped_data.plot(kind='bar', stacked=True, ax=ax, width=0.8)

        ax.set_xlabel('Decade')
        ax.set_ylabel('Number of Songs')
        ax.set_title(f'Songs by Decade' + (f' by {category.capitalize()}' if category else ''))
        ax.legend(title=category.capitalize(), bbox_to_anchor=(1.05, 1), loc='upper left')

    if category == "no category":
        grouped_data = df.groupby('Decade').size()
        grouped_data.plot(kind='bar',ax=ax, width=0.8,color="#0000FF")
        ax.bar(grouped_data.index, grouped_data.values)        
        ax.set_xlabel('Decade')
        ax.set_ylabel('Number of Songs')
        ax.set_title('Bar Chart of Songs by Decade')

def plot_cumulative_line(ax, category):
    """Plot the cumulative line chart based on the specified category."""
    df = get_tab_df().copy()
    
    # Handle missing values
    df['language'] = df['language'].fillna('Unknown')
    
    df = correct_language(df)

    play_df=get_play_df()
    play_melted = play_df.melt(
        id_vars=['song', 'artist'], var_name='date', value_name='play_order'
    ).dropna(subset=['play_order'])
    play_melted['date'] = pd.to_datetime(play_melted['date'], errors='coerce')
    data = pd.merge(play_melted,df[['song', 'gender', 'language', 'type', 'source']],on='song')
    
    if category in df.columns:
        data_counts = data.groupby(['date', category]).size().unstack(fill_value=0).cumsum()

        for cat_value in data_counts.columns:
            ax.plot(data_counts.index, data_counts[cat_value], label=cat_value)

        last_totals = data_counts.iloc[-1]
        legend_labels = [f"{label} - {count} (Total)" for label, count in zip(last_totals.index, last_totals.values)]
        ax.legend(legend_labels, title=category.capitalize(), bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax.set_xlabel('Date')
        ax.set_ylabel('Cumulative Number of Songs Played')
        ax.set_title(f'Cumulative Songs Played by {category.capitalize()}')

    if category == "no category":
        data_counts = data.groupby('date').size().cumsum()
        ax.plot(data_counts.index, data_counts.values, label='Total',color="#0000FF")
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Songs Played')
        ax.set_title('Cumulative Chart of Songs Played')

def plot_donut_chart(ax, category):
    """Plot the donut chart based on the specified category."""
    df = get_tab_df().copy()
    # Handle missing values
    df['language'] = df['language'].fillna('Unknown')

    df = correct_language(df)

    # Handle missing values
    df['language'] = df['language'].fillna('Unknown')

    if category in df.columns:
     category_counts = df[category].value_counts()
     wedges, _ = ax.pie(category_counts, startangle=90, wedgeprops=dict(width=0.3))
     ax.legend(wedges, [f"{label} - {percent:.1f}%" for label, percent in zip(category_counts.index, (category_counts / category_counts.sum()) * 100)],
              title=category.capitalize(), loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
     ax.set_title(f'Songs by {category.capitalize()}')

    #Pie chart by gender
    if category == "no category":
        gender_counts = df['gender'].value_counts()
        wedges, _ = ax.pie(gender_counts,startangle=90)
        ax.legend(wedges,[f"{label} - {percent:.1f}%" for label, percent in zip(gender_counts.index,(gender_counts / gender_counts.sum()) * 100)],
        title= 'gender',loc="center left",bbox_to_anchor=(1, 0, 0.5, 1))
        ax.set_title(f'Songs by Gender')

def convert_to_minutes(duration):
    '''Formatting duration column to nearest minutes'''
    try:
        h, m, s = map(int, duration.split(':'))
        return h * 60 + m + s / 60  
    except:
        return None  

def display_chart(root,fig):
    """Display the Matplotlib figure in a Tkinter window."""
    chart_window = tk.Toplevel(root)
    chart_window.title("Chart Display")
    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    toolbar = NavigationToolbar2Tk(canvas, chart_window)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas.draw()


