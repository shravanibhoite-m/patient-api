import mysql.connector
from mysql.connector import Error
import os
from pathlib import Path
from dotenv import load_dotenv
from patientdata import patient_data
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

# def insert(conn,patient_data):
#     try:
#         cursor=conn.cursor()
#         insert_values=""" 
#         INSERT INTO patients (id, name, age, gender, email, phone_num, password, active, blood_group, emergency_contact, city, pincode)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         for p in patient_data:
#             values=(p["id"], p["name"], p["age"], p["gender"], p["email"],
#                 p["phone_num"], p["pass"], p["active"], p["blood_group"],
#                 p["emergency_contact"], p["address"]["city"], p["address"]["pincode"]
#                 )
#             cursor.execute(insert_values,values)
#         conn.commit()
#         cursor.close()
#     except Exception as e:
#         print(e)
# def select(conn):
#         cursor = conn.cursor()
#         cursor.execute("USE hospital_db")
#         cursor.execute("SELECT * FROM patients WHERE id = 1")
#         print(cursor.fetchall())
if __name__== "__main__":
    print("conncetion started..")
    conn=db_connection()
    create_table(conn)
    # insert(conn,patient_data)
    # select(conn)
    print("connection successful..")
