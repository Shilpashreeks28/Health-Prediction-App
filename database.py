import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

def create_database():
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD")
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS health_db")
    conn.close()

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(100),
            date_of_birth DATE,
            email VARCHAR(100),
            glucose FLOAT,
            haemoglobin FLOAT,
            cholesterol FLOAT,
            remarks TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_patient(full_name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patients (full_name, date_of_birth, email, glucose, haemoglobin, cholesterol, remarks)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks))
    conn.commit()
    conn.close()

def get_all_patients():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    data = cursor.fetchall()
    conn.close()
    return data

def update_patient(id, full_name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE patients SET full_name=%s, date_of_birth=%s, email=%s,
        glucose=%s, haemoglobin=%s, cholesterol=%s, remarks=%s
        WHERE id=%s
    """, (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks, id))
    conn.commit()
    conn.close()

def delete_patient(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE id=%s", (id,))
    conn.commit()
    conn.close()