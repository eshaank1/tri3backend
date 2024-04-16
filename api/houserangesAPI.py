import csv

def find_max_min_in_columns(filename):
    # Initialize dictionaries to store maximum and minimum values for selected columns
    max_values = {}
    min_values = {}

    # Selected headers
    selected_headers = ["bed", "bath", "acre_lot"]

    # Open the CSV file
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)

        # Initialize max_values and min_values dictionaries with selected headers
        for header in selected_headers:
            max_values[header] = float('-inf')
            min_values[header] = float('inf')

        # Iterate over each row and update max_values and min_values for selected columns
        for row in reader:
            for header in selected_headers:
                # Try to convert value to float (assuming numerical data)
                try:
                    value = float(row[header])
                    # Update max value for each column
                    if value > max_values[header]:
                        max_values[header] = value
                    # Update min value for each column
                    if value < min_values[header]:
                        min_values[header] = value
                except ValueError:
                    # Skip non-numeric values
                    continue

    return max_values, min_values

if __name__ == "__main__":
    filename = "realtor-data.csv"  # Change this to your dataset file path
    max_values, min_values = find_max_min_in_columns(filename)

    # Store the values as variables
    max_bed = max_values["bed"]
    max_bath = max_values["bath"]
    max_acre_lot = max_values["acre_lot"]

    min_bed = min_values["bed"]
    min_bath = min_values["bath"]
    min_acre_lot = min_values["acre_lot"]


    '''
    print("Maximum values for selected columns:")
    print(f"Max Bed: {max_bed}")
    print(f"Max Bath: {max_bath}")
    print(f"Max Acre Lot: {max_acre_lot}")

    print("\nMinimum values for selected columns:")
    print(f"Min Bed: {min_bed}")
    print(f"Min Bath: {min_bath}")
    print(f"Min Acre Lot: {min_acre_lot}")
    '''
    