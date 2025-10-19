# -*- coding: utf-8 -*-
"""
Created on Sun Sep  7 19:39:12 2025

@author: DELL-PC
"""
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="App_User",          # 🔹 Replace with your MySQL username
        password="pass@1234",     # 🔹 Replace with your MySQL password
        database="placement_db"   # 🔹 Database name in Workbench
    )

def student_exists(student_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE roll_no = %s", (student_id,))
    student = cursor.fetchone()
    conn.close()
    return student is not None

def register_student(student_id, name, email, branch, year, cgpa):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO students (roll_no, name, email, branch, year, cgpa)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (student_id, name, email, branch, year, cgpa))
    conn.commit()
    conn.close()

def get_student_by_id(student_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE roll_no = %s", (student_id,))
    student = cursor.fetchone()
    conn.close()
    return student
