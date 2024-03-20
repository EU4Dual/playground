from flask import Flask, jsonify
import configparser
import psycopg2
import task

app = Flask(__name__)
app.json.sort_keys = False

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the file using the object
config.read('config.ini')

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

# Execute the SQL commands
# Delete the table 'module' if exists, this will ensure a new table and entries are created in every execution
cursor.execute('DROP TABLE IF EXISTS module;')
cursor.execute(task.create_command)
cursor.execute(task.insert_command)
connection.commit()


# Create an API endpoint at /getAllData
@app.route('/getAllData', methods=['GET'])
def getAllData():

    # Execute a SQL command to select all entries from module
    cursor.execute('SELECT * FROM module;')

    # Retrieve query results
    records = cursor.fetchall()

    # Print the query results in terminal for verification
    print(records)

    # Build the API response
    # Get column names from cursor description
    column_names = [desc[0] for desc in cursor.description]

    # Build a list of dictionaries with column headers and values
    result_data = []
    for row in records:
        result_data.append(dict(zip(column_names, row)))

    return jsonify(result_data)


if __name__ == "__main__":
    app.run(debug=True)


