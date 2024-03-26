
from flask import Flask, jsonify
import configparser
import psycopg2
import pandas as pd

# Create a ConfigParser object and read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# [Step 1]
# Set up the web framework with Flask and the connection to database with psycopg2

app = Flask(__name__)
app.json.sort_keys = False

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

        import openpyxl

        # Load the Excel file
        workbook = openpyxl.load_workbook('your_excel_file.xlsx')

        # Assuming the table is in the first sheet, you can change the sheet name or index as needed
        sheet = workbook.active

        # Extract header row
        header_row = [cell.value for cell in sheet[1]]

        # Extract all other rows
        data_rows = [[cell.value for cell in row] for row in sheet.iter_rows(min_row=2)]

        # Print header row and data rows
        print("Header Row:", header_row)
        print("Data Rows:", data_rows)

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

    # Generating SQL command to create table 'module'
    create_command = f"CREATE TABLE module ({', '.join([f'{col} VARCHAR(255)' for col in header_row])});"

    # Generating SQL commands to insert data into 'module' table
    insert_commands = []
    for row in data_rows:
        values = ', '.join([f"'{value}'" if value else "NULL" for value in row])
        insert_commands.append(f"INSERT INTO module VALUES ({values});")

    # Join insert commands into a single string
    insert_command = "\n".join(insert_commands)

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

    # Assuming 'cursor' is your cursor object containing the query result

    # Add your codes to get the column names from cursor
    column_names = [column[0] for column in cursor.description]

    # Add your codes to build a list of dictionaries with column_names and values from records
    result_data = []
    for record in cursor.fetchall():
        result_data.append(dict(zip(column_names, record)))

    # Convert result_data to JSON format and return as the API response
    return jsonify(result_data)


if __name__ == "__main__":
    app.run(debug=True)

