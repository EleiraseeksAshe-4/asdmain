import pandas as pd

# Path to your Excel file
excel_file = 'path_to_your_excel_file.xlsx'


def import_static_data(excel_file):
    # Read the Excel file
    xls = pd.ExcelFile(excel_file)

    # Create a dictionary to store DataFrames
    dataframes = {}

    # Iterate through each sheet and read it into a DataFrame
    for sheet in xls.sheet_names:
        dataframes[sheet] = pd.read_excel(xls, sheet_name=sheet)

    return dataframes


answers = import_static_data(
    '/Users/johnbridges/Dropbox/NewHope Psychology/JoyConsulting/GateInc/ExpertReports/ChrisMacArthurSettle/word/cars_qpc.xlsx')
scoring = import_static_data(
    '/Users/johnbridges/Dropbox/NewHope Psychology/JoyConsulting/GateInc/ExpertReports/templates/carseval_data.xlsx')

print(answers)
# Example of accessing individual DataFrames
#for sheet_name, df in dataframes.items():
#    print(f"DataFrame for sheet: {sheet_name}")
#    print(df.head())  # Print the first few rows of each DataFrame
