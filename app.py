from flask import Flask, render_template, jsonify
import configparser
import psycopg2

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

# Execute a query
cursor.execute("SELECT * FROM campus;")

# Retrieve query results
records = cursor.fetchall()

# Print the query results in terminal
print(records)


# Display the query records in http://127.0.0.1:5000
@app.route('/')
def hello():
    return records


if __name__ == "__main__":
    app.run(debug=True)
