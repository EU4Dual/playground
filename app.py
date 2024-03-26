from flask import Flask, jsonify
import configparser
config.read('config.ini')
import psycopg2
import pandas as pd

# [Step 1]
# Set up the web framework with Flask and the connection to database with psycopg2

app = Flask(__name__)
app.json.sort_keys = False

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the file using the object

# Obtain the configuration values
database = config.get('database', 'database')
user = config.get('database', 'user')
password = config.get('database', 'password')
host = config.get('database', 'host')
port = config.get('database', 'port')

# Establish the connection
connection = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)

# Open a cursor to perform database operations
cursor = connection.cursor()


# [Step 2]
# Read data from Excel file
def read_excel_file(file_path):
    try:
        # We use pandas to read data sets from Excel
        # Reading the documentation of pandas would be useful:
        # https://pandas.pydata.org/pandas-docs/stable/reference/frame.html

        # Read the Excel file
        df = pd.read_excel(file_path)

        # --- BEGIN OF TASK 1 ---

        # Add your code to extract the header row of the table as a list in Excel
        header_row = []

        # Add your code to extract all other rows of the table as a list in Excel
        data_rows = []

        # --- END OF TASK 1 ---

        return header_row, data_rows
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None, None


# Call read_excel_file() function
file_path = 'resources/sample_module_data.xlsx'
header_row, data_rows = read_excel_file(file_path)

# Print the rows in the console for verification
if header_row and data_rows:
    print("\n - Header row -\n", header_row)
    print("\n - Data rows -\n", data_rows)
else:
    print("\nFailed to read Excel file.")


# [Step 3]
# Build the corresponding SQL commands to create table and insert entries
# to the database according to the data extracted from Excel
def generate_sql_commands(header_row, data_rows):
    # Studying how to loop through a list in Python would be useful
    # You will also have to concatenate or format strings, this page provides more information:
    # https://www.digitalocean.com/community/tutorials/python-string-concatenation

    # End if either header_row or data_rows are empty
    if not header_row or not data_rows:
        print("Header row or data rows are empty.")
        return None, None

    # --- BEGIN OF TASK 2 ---

    # Add your codes to generate a SQL command that create a table called 'module' and contains header_row as keys
    create_command = ""

    # Add your codes to generate a SQL command that insert every row from data_rows to the table 'module'
    insert_command = ""

    # --- END OF TASK 2 ---

    return create_command, insert_command


# Call generate_sql_commands() function
create_command, insert_command = generate_sql_commands(header_row, data_rows)

# Print the SQL commands in the console for verification
if create_command and insert_command:
    print("\n - CREATE SQL command -")
    print(create_command)
    print("\n - INSERT SQL commands -")
    print(insert_command)
else:
    print("\nFailed to generate SQL commands.")


# [Step 4]
# Execute the SQL commands
# Delete the table 'module' if exists, this will ensure a new table and entries are created in every execution
# Check if the variables are None before executing the SQL commands
if create_command is not None and insert_command is not None:
    cursor.execute('DROP TABLE IF EXISTS module;')
    cursor.execute(create_command)
    cursor.execute(insert_command)
    connection.commit()


# [Step 5]
# Create an API endpoint with GET method at {hostname:port}/getAllData
# and build the API response
@app.route('/getAllData', methods=['GET'])
def getAllData():
    # We first query all data in table 'module' from the database
    # Then we convert the query results to be serialized into JSON format
    # Finally return that JSON as the API response
    # The documentation of cursor might give you some hints:
    # https://www.psycopg.org/docs/cursor.html

    # Execute a SQL command to select all entries from module
    cursor.execute('SELECT * FROM module;')

    # Retrieve query results
    records = cursor.fetchall()

    # Print the query results in console for verification
    print(records)

    # --- BEGIN OF TASK 3 ---

    # Add your codes to get the column names from cursor
    column_names = []

    # Add your codes to build a list of dictionaries with column_names and values from records
    result_data = []

    # --- END OF TASK 3 ---

    # Convert result_data to JSON format and return as the API response
    return jsonify(result_data)


if __name__ == "__main__":
    app.run(debug=True)
