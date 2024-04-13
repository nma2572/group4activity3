import csv
import os

def prompt_file_path():
    """
    Prompts the user to enter a file path until a valid CSV file path is provided.
    Returns the valid file path.
    """
    while True:
        file_path = input("Please enter the path to the CSV file: ")
        if os.path.exists(file_path):
            return file_path
        else:
            print("File not found. Please enter a valid path.")

def load_csv_data(file_path):
    """
    Loads CSV data from the given file path and handles any issues with file reading.
    Returns the data as a list of dictionaries and the list of column names.
    """
    try:
        with open(file_path, newline='') as csvfile:
            data = list(csv.DictReader(csvfile))
            if not data:
                raise ValueError("File is empty or has invalid format.")
            return data, data[0].keys()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None, None

def select_numerical_column(columns):
    """
    Prompts the user to select a numerical column from the list of columns provided.
    Returns the selected column name.
    """
    print(f"Available columns: {', '.join(columns)}")
    while True:
        column_choice = input("Please choose a numerical column: ")
        if column_choice in columns:
            return column_choice
        else:
            print("Invalid column. Please choose from the available columns.")

def validate_numerical_data(data, column):
    """
    Validates that the data in the selected column is numerical.
    Returns a boolean indicating whether the data is numerical.
    """
    try:
        for item in data:
            if item[column]:  # Check non-empty strings
                float(item[column])  # Attempt to convert to float
        return True
    except ValueError:
        return False

def replace_empty_with_choice(data, column, choice):
    """
    Replaces empty values in the data column based on the user's choice.
    Choices can be 'min', 'max', or 'average'.
    Returns the modified data.
    """
    numeric_values = [float(row[column]) for row in data if row[column].strip()]
    if not numeric_values:
        raise ValueError("No numeric values available to calculate min, max, or average.")

    if choice == 'min':
        replacement_value = min(numeric_values)
    elif choice == 'max':
        replacement_value = max(numeric_values)
    elif choice == 'average':
        replacement_value = sum(numeric_values) / len(numeric_values)
    else:
        raise ValueError("Invalid replacement choice.")

    return [replacement_value if not row[column].strip() else float(row[column]) for row in data]

def insertion_sort(data, descending=False):
    """
    Sorts the data using the insertion sort algorithm.
    Can sort in ascending (default) or descending order.
    Returns the sorted data.
    """
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and ((key < data[j]) if not descending else (key > data[j])):
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key
    return data

def visualize_data(data, column):
    """
    Visualizes the data by printing '*' characters. Each '*' represents 5 units of the value.
    The maximum number of '*' printed is 20 for values of 100 and above.
    """
    print(f"\nColumn: {column}\nLegend: each '*' represents 5 units\n")
    for value in data:
        stars = min(int(value / 5), 20)  # Calculate number of '*' to print, capped at 20
        print('*' * stars)

def main():
    print("---------------------------------\nWelcome to Data Analysis CLI\n---------------------------------")
    print("Program stages:\n1. Load Data\n2. Clean and prepare data\n3. Analyse Data\n4. Visualize Data")
   
    """
    Prints the welcome message and the stages of the program.
    """
   
    file_path = prompt_file_path()
    data, columns = load_csv_data(file_path)

    if data is None or columns is None:
        return  # Exit if data could not be loaded properly

    while True:
        column_choice = select_numerical_column(columns)
        if validate_numerical_data(data, column_choice):
            break
        else:
            print(f"The column '{column_choice}' contains non-numerical values. Please choose a different column.")
    
    print("Stage 2: Clean and prepare data")
    choice = input("Replace empty cells with (min, max, average): ").lower()
    try:
        prepared_data = replace_empty_with_choice(data, column_choice, choice)
    except ValueError as e:
        print(e)
        return

    print("Stage 3: Analyse data")
    order_choice = input("Sort data in ascending or descending order? (asc/desc): ").lower()
    sorted_data = insertion_sort(prepared_data, descending=(order_choice == 'desc'))

    print("Stage 4: Visualize data")
    visualize_data(sorted_data, column_choice)

if __name__ == "__main__":
    main()
