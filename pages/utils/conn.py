import mysql.connector

# Establish a connection to the database
db_connection = mysql.connector.connect(
    host="localhost",        # XAMPP server is usually on localhost
    user="root",    # Default XAMPP username is 'root'
    password="",# Default XAMPP password is usually empty
    database="data_mining" # Name of your database
)

print("Connected to the database!")