#Code for displaying the query output and its sorting function
import tkinter as tk
from tkinter import ttk
import pandas as pd

def data_display(root, grouped_df, selected_columns):
    """Create a new child window to display the filtered data."""
    child_window = tk.Toplevel(root)
    child_window.geometry("800x400")
    child_window.title("Filtered Data Display")

    # Initialize the Treeview widget and populate it with data
    tree = ttk.Treeview(child_window, columns=selected_columns, show='headings')
    for col in selected_columns:
        tree.heading(col, text=col, command=lambda c=col: sort_by(c, False))  # Bind sort_by to column header
        tree.column(col, width=100, anchor='center')

    for index, row in grouped_df.iterrows():
        tree.insert("", tk.END, values=list(row))

    tree.pack(fill="both", expand=True)

    # Adding scrollbar
    scrollbar = ttk.Scrollbar(child_window, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    def sort_by(col, reverse):
        """Sort the data based on the clicked column and reverse value"""
        nonlocal grouped_df  # Giving access to the outer scoped grouped_df
        reverse = not reverse  # Toggle the reverse flag

        #Ensuring the correct format of date and sorting the data
        if 'date' in grouped_df.columns:
            grouped_df['date'] = pd.to_datetime(grouped_df['date'], format='%Y%m%d', errors='coerce').dt.date
        sorted_data = grouped_df.sort_values(by=col, ascending=not reverse)

        for row in tree.get_children():
            tree.delete(row)

        #Displaying the sorted data with the clickable headers
        for index, row in sorted_data.iterrows():
            tree.insert("", tk.END, values=list(row))
        tree.heading(col, text=f"{col}", command=lambda c=col: sort_by(c, reverse))
