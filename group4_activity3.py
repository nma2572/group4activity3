'''Abedin, Sayyed has made the prompt_file_path function and part of the main function related to the prompt_file_path
   Alghubash, Shaikha made the validate_numerical_value function and part of main function related to it
   Argaw Natnael has made the insertion_sort load_csv_data  select_numerical_column replace_empty_with_choice visualize_data and the main functions'''


import csv

def prompt_file_path():
    """
    Prompts the user to enter a file path until a valid CSV file path is provided.
    Attempts to open the file directly, and if unsuccessful, prompts the user again.
    Returns the valid file path.
    """
    while True:
        file_path = input("Please enter the path to the CSV file: ")
        try:
            with open(file_path, 'r', newline='') as csvfile:
                # If the file can be opened, we assume it's valid
                return file_path
        except IOError:
            # IOError is raised for various file-related reasons, e.g. file does not exist
            print("File not found or cannot be opened. Please enter a valid path.")

def load_csv_data(file_path):
    """
    Loads CSV data from the given file path using csv.reader.
    Returns the data as a list of rows (excluding the header) and the header row.
    """
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            columns = next(reader)  # This reads the first line which is typically the header
            data = list(reader)  # This reads the rest of the data
            if not data:
                raise ValueError("File is empty or has no data.")
            return data, columns
    except Exception as e:
        print(f"Error reading file: {e}")
        return None, None

def select_numerical_column(columns):
    """
    Prompts the user to select a numerical column from the list of columns provided.
    Returns the selected column index and name.
    """
    print(f"Available columns: {', '.join(columns)}")
    while True:
        column_choice = input("Please choose a numerical column by entering the column name: ")
        if column_choice in columns:
            return columns.index(column_choice), column_choice
        else:
            print("Invalid column. Please choose from the available columns.")

def validate_numerical_data(data, column_index):
    """
    Validates that the data in the selected column is numerical.
    Assumes 'data' is a list of lists and 'column_index' is the index of the selected column.
    Returns a boolean indicating whether the data is numerical.
    """
    try:
        for row in data:
            if row[column_index]:  # Check non-empty strings
                float(row[column_index])  # Attempt to convert to float
        return True
    except ValueError:
        return False

def replace_empty_with_choice(data, column_index, choice):
    """
    Replaces empty values in the data column based on the user's choice.
    Choices can be 'min', 'max', or 'average'.
    Returns the modified data.
    """
    numeric_values = [float(row[column_index]) for row in data if row[column_index].strip()]
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

    for row in data:
        if not row[column_index].strip():
            row[column_index] = replacement_value

    return data

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

def visualize_data(data, column_name):
    """
    Visualizes the data by printing '*' characters. Each '*' represents 5 units of the value.
    The maximum number of '*' printed is 20 for values of 100 and above.
    """
    print(f"\nColumn: {column_name}\nLegend: each '*' represents 5 units\n")
    for value in data:
        stars = min(int(value / 5), 20)  # Calculate number of '*' to print, capped at 20
        print('*' * stars)

def main():
    print("---------------------------------\nWelcome to Data Analysis CLI\n---------------------------------")
    print("Program stages:\n1. Load Data\n2. Clean and prepare data\n3. Analyse Data\n4. Visualize Data")

    file_path = prompt_file_path()
    data, columns = load_csv_data(file_path)

    if data is None or columns is None:
        return  # Exit if data could not be loaded properly

    column_index, column_name = select_numerical_column(columns)
    if not validate_numerical_data(data, column_index):
        print(f"The column '{column_name}' contains non-numerical values. Please choose a different column.")
        return

    print("Stage 2: Clean and prepare data")
    choice = input("Replace empty cells with (min, max, average): ").lower()
    if choice not in ('min', 'max', 'average'):
        print("Invalid choice. Please enter 'min', 'max', or 'average'.")
        return
    data = replace_empty_with_choice(data, column_index, choice)

    print("Stage 3: Analyse data")
    order_choice = input("Sort data in ascending or descending order? (asc/desc): ").lower()
    if order_choice not in ('asc', 'desc'):
        print("Invalid choice. Please enter 'asc' for ascending or 'desc' for descending.")
        return
    
   
    sorted_data = insertion_sort([float(row[column_index]) for row in data], descending=(order_choice == 'desc'))

    print("Stage 4: Visualize data")
    visualize_data(sorted_data, column_name)

if __name__ == "__main__":
    main()

