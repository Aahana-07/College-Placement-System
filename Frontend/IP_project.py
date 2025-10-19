
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  3 17:56:47 2025

@author: DELL-PC
"""
import streamlit as st
import mysql.connector
import pandas as pd
from db import get_connection

st.set_page_config(page_title="College Placement System", layout="centered")

# -------------------- SESSION INITIALIZATION --------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "student_id" not in st.session_state:
    st.session_state.student_id = None
if "student_name" not in st.session_state:
    st.session_state.student_name = None

# -------------------- HOME PAGE --------------------
if st.session_state.page == "home":
    st.title("🎓 College Placement System")
    st.markdown("---")
    st.subheader("Select Login Role")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("👨‍🎓 Login as Student", use_container_width=True):
            st.session_state.page = "student_login"
            st.rerun()
    with col2:
        if st.button("👨‍💼 Login as Admin", use_container_width=True):
            st.session_state.page = "admin_login"
            st.rerun()

# -------------------- STUDENT LOGIN --------------------
elif st.session_state.page == "student_login":
    st.header("🧑‍🎓 Student Login")

    student_id = st.text_input("Enter Roll Number", value=st.session_state.student_id or "")

    if st.button("Login", use_container_width=True):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students WHERE roll_no = %s", (student_id,))
        student = cursor.fetchone()
        conn.close()

        if student:
            st.session_state.student_id = student_id
            st.session_state.student_name = student["name"]
            st.session_state.page = "student_dashboard"
        else:
            st.session_state.student_id = student_id
            st.session_state.page = "student_register"
        st.rerun()

    if st.button("⬅ Back to Home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

# -------------------- STUDENT DASHBOARD --------------------
elif st.session_state.page == "student_dashboard":
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE roll_no = %s", (st.session_state.student_id,))
    student = cursor.fetchone()
    conn.close()

    if student:
        st.success(f"✅ Welcome, {student['name']}!")
        st.markdown("### 🎯 Student Quick Menu")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("🏠 Dashboard"):
                st.session_state.page = "dashboard"
                st.rerun()
        with col2:
            if st.button("👤 View Profile"):
                st.session_state.page = "view_profile"
                st.rerun()
        with col3:
            if st.button("🏢 View Companies"):
                st.session_state.page = "view_companies"
                st.rerun()
        with col4:
            if st.button("🚪 Logout"):
                st.session_state.page = "home"
                st.session_state.student_id = None
                st.session_state.student_name = None
                st.info("You have been logged out.")
                st.rerun()

# -------------------- DASHBOARD PAGE --------------------
elif st.session_state.page == "dashboard":
    st.header("📘 Dashboard")
    st.info("Use this menu to explore your options.")
    if st.button("⬅ Back"):
        st.session_state.page = "student_dashboard"
        st.rerun()

# -------------------- VIEW PROFILE --------------------
elif st.session_state.page == "view_profile":
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE roll_no = %s", (st.session_state.student_id,))
    student = cursor.fetchone()
    conn.close()

    if student:
        st.header("👤 My Profile")
        st.write(f"**Roll No:** {student['roll_no']}")
        st.write(f"**Name:** {student['name']}")
        st.write(f"**Email:** {student['email']}")
        st.write(f"**Branch:** {student['branch']}")
        st.write(f"**Year:** {student.get('year', 'N/A')}")
        st.write(f"**CGPA:** {student.get('cgpa', 'N/A')}")
        st.write(f"**Created On:** {student['created_date']}")
    if st.button("⬅ Back"):
        st.session_state.page = "student_dashboard"
        st.rerun()

# -------------------- VIEW COMPANIES --------------------
elif st.session_state.page == "view_companies":
    st.header("🏢 Companies Visiting Campus")

    companies = [
        {"Company": "Infosys", "Role": "Software Engineer", "CGPA": 7.0},
        {"Company": "TCS", "Role": "Data Analyst", "CGPA": 6.5},
        {"Company": "Google", "Role": "Intern", "CGPA": 8.0},
        {"Company": "Amazon", "Role": "Cloud Support", "CGPA": 7.5},
        {"Company": "Wipro", "Role": "Web Developer", "CGPA": 6.0},
    ]

    for company in companies:
        with st.container():
            st.markdown(f"### {company['Company']}")
            st.write(f"**Role:** {company['Role']}")
            st.write(f"**Minimum CGPA Required:** {company['CGPA']}")
            st.markdown("---")

    if st.button("⬅ Back"):
        st.session_state.page = "student_dashboard"
        st.rerun()

# -------------------- STUDENT REGISTRATION --------------------
elif st.session_state.page == "student_register":
    st.warning("⚠️ ID not found! Please register below.")
    with st.form("register_form"):
        roll_no = st.text_input("Roll Number", st.session_state.student_id)
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        branch = st.text_input("Branch")
        year = st.number_input("Year of Study", min_value=1, max_value=4, step=1)
        cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, step=0.1)
        submit = st.form_submit_button("Register")

        if submit:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO students (roll_no, name, email, branch, year, cgpa) VALUES (%s, %s, %s, %s, %s, %s)",
                (roll_no, name, email, branch, year, cgpa)
            )
            conn.commit()
            conn.close()
            st.success("🎉 Registration successful! You can now log in.")
            st.session_state.page = "student_login"
            st.rerun()

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# -------------------- ADMIN LOGIN --------------------
elif st.session_state.page == "admin_login":
    st.header("👨‍💼 Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login as Admin", use_container_width=True):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admins WHERE username = %s AND password = %s", (username, password))
        admin = cursor.fetchone()
        conn.close()

        if admin:
            st.success(f"✅ Welcome Admin {admin['username']}!")
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM students")
            data = cursor.fetchall()
            conn.close()

            if data:
                df = pd.DataFrame(data)
                st.dataframe(df)
            else:
                st.info("No students found in the database.")
        else:
            st.error("❌ Invalid credentials. Please register an admin if none exists.")

    if st.button("📝 Register New Admin", use_container_width=True):
        st.session_state.page = "admin_register"
        st.rerun()

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# -------------------- ADMIN REGISTRATION --------------------
elif st.session_state.page == "admin_register":
    st.header("📝 Register New Admin")
    with st.form("admin_form"):
        username = st.text_input("Create Username")
        password = st.text_input("Create Password", type="password")
        submit = st.form_submit_button("Register")

        if submit:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO admins (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            conn.close()
            st.success("✅ Admin registered successfully!")
            st.session_state.page = "admin_login"
            st.rerun()

    if st.button("⬅ Back to Login"):
        st.session_state.page = "admin_login"
        st.rerun()



