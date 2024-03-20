import pandas as pd


def read_excel_file(file_path):
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)

        # Extract the header row
        header_row = df.columns.tolist()

        # Extract the other rows
        data_rows = df.values.tolist()

        return header_row, data_rows
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None, None


def generate_sql_commands(header_row, data_rows):
    # End if either header_row or data_rows are empty
    if not header_row or not data_rows:
        print("Header row or data rows are empty.")
        return

    # BEGIN OF YOUR TASK

    # Add your codes to generate a SQL command that create a table called 'module' and contains header_row as keys
    create_command = ""

    # Add your codes to generate a SQL command that insert every row from data_rows to the table 'module'
    insert_command = ""

    # END OF YOUR TASK

    return create_command, insert_command


# ---- Execution ----
# Example usage
file_path = 'resources/sample_module_data.xlsx'
header_row, data_rows = read_excel_file(file_path)

# Print the rows in the terminal for verification
if header_row and data_rows:
    print("\n - Header row -\n", header_row)
    print("\n - Data rows -\n", data_rows)
else:
    print("\nFailed to read Excel file.")

create_command, insert_command = generate_sql_commands(header_row, data_rows)

# Print the SQL commands in the terminal for verification
if create_command and insert_command:
    print("\n - CREATE SQL command -")
    print(create_command)
    print("\n - INSERT SQL commands -")
    print(insert_command)
else:
    print("\nFailed to generate SQL commands.")
