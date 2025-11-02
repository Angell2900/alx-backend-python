import mysql.connector

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",         
            password="livinlarge"  
        )
        print("Connected to MySQL server successfully")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",           
            password="livinlarge",  
            database="ALX_prodev"
        )
        print("Connected to ALX_prodev database successfully")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            age INT
        )
    """)
    connection.commit()
    cursor.close()
    print("Table 'user_data' created successfully!")

import csv
import mysql.connector

def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        with open(csv_file, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                cursor.execute(
                    "INSERT INTO user_data (id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (row['id'], row['name'], row['email'], row['age'])
                )
        connection.commit()
        print("Data inserted successfully from CSV!")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    except FileNotFoundError:
        print(f"File not found: {csv_file}")
    finally:
        cursor.close()
