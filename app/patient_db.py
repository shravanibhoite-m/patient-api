import mysql.connector
from mysql.connector import Error
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")
def db_connection():
    try:
        conn = mysql.connector.connect(
     host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
)
        return conn
    except Error as e:
        print("DB connection error:", e)
        return None

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS hospital_db")
        cursor.execute("USE hospital_db")
        create_table_query = """
        CREATE TABLE IF NOT EXISTS patients (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            gender VARCHAR(10),
            email VARCHAR(100),
            phone_num VARCHAR(15),
            password VARCHAR(100),
            active BOOLEAN,
            blood_group VARCHAR(5),
            emergency_contact VARCHAR(15),
            city VARCHAR(100),
            pincode INT
        )
        """
        cursor.execute(create_table_query)
        cursor.close()
    except Exception as e:
        print(e)


if __name__== "__main__":
    print("conncetion started..")
    conn=db_connection()
    create_table(conn)
    # insert(conn,patient_data)
    # select(conn)
    print("connection successful..")
