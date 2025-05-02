# Leveraging-Data-Analytics-for-Ukulele-Tuesday
Developed a Python-based GUI application to analyze and visualize song data from Ukulele Tuesday events. The tool allows users to query data, generate insights, and explore trends through interactive graphs using libraries like pandas, tkinter, and matplotlib.

# USER MANUAL FOR THE PROGRAM
Our program allows users to interact with Ukulele Tuesday Band’s database and helps to analyse the data in the following ways:
1)Familiarize and summarise the data content
2)Query the data based on user selected columns and data ranges
3)Visualise the data in graphs to understand the trends better
Prerequisites:
For successful running of the program, user would require Python installed in the system along with the following Python libraries:
1)tkinter (for graphical user interface)
2)pandas (for storing and handling the database)
3)numpy and collections (for performing data manipulations)
4)matplotlib (for generating graphs)
5)os (for file manipulation)

# How to run the project:
1) Entire program code is present in 5 files (utils.py, data_handler.py, plotting.py, gui.py, main.py). Store these 5 files and 3 data dictionary files (Tab_data_dict, Play_data_dict, Request_data_dict created from assignment document) in the same directory.
2) Run main.py from command line terminal or Python IDE (Visual Studio) to launch the program with the welcome screen (as shown in the figure).
3) Enter or select the csv file for each database on its respective field and load them (as shown in the figure). Once all three files are loaded the “Next” button will be enabled to proceed to the next stage of analysis.
4) From next screen, select the task that user would like the program to perform.
5) Data summary screen gives information on:
  ➢Data Dictionary (created based on historical data).
  ➢Display of first 10 rows.
  ➢Data types of each column.
  ➢Click on “More Insights” to proceed to the next screen.
  ➢Count of missing values per column of Tab Database.
  ➢Details of Tuesdays which are missing in the database within the date range.
  ➢Data inconsistencies present in Play and Request Database.
  ➢Range of dates for Play and Request Database.
6)Data querying screen helps user to filter the data:
  ➢Data querying screen is provided with two fields to select user’s desired date range and columns to filter the data.
  ➢Enter the range of dates in dd-mm-yyyy format. This will filter the data for the range of dates where songs were played. In case of error in date format, it will throw      error boxes.
  ➢Select the required columns that need to be displayed.
  ➢Along with the columns, the count of times the song was played and the count of times it was requested by Group/Person/Unknown will be displayed.
  ➢By default, the extreme date ranges and entire columns of tab_df are selected. So, make sure to input the field with the desired value you want to view in a query.
  ➢Click on “Apply the filters and display the data” button to view the output on a new screen.
  ➢Output screen also has the functionality to sort each by clicking on the column header and the results will be toggled between ascending or descending order with each click
  ➢To refine the query, close the screen to redo the process.
7)Data visualisation screen helps user to visualise the data better:
  ➢Data visualization screen offers the below 7 distinct plots designed to understand the trends and patterns in your data. Click on the respective radio button to select the graph.
    •Histogram of Songs by Difficulty level
    •Histogram of Songs by Difficulty level
    •Histogram of Songs by Duration
    •Bar chart of Songs by Language
    •Bar chart of Songs by Source
    •Bar chart of Songs by Decade
    •Cumulative Line Chart of Songs Played
    •Donut Chart of Songs by Categorical Column
  ➢To observe how different categories contribute to the overall data, select the desired categorical columns from the dropdown menu and filter the graph.
  ➢To view the graph independently without any categorical addition of values, select the "No Category" filter.
  ➢After selecting the desired graph label and the categorical filter, click on the “Generate Chart” button to view the visual representation of the data in a screen.
  ➢Each graph screen comes with a “Save” option towards the bottom left corner to save the graph as a PNG image to the system.
  ➢To refine the plot, close the screen to redo the process.
8)Each screen is provided with “Back” and “Exit” buttons to navigate to the previous screen and to close the user interface respectively.
