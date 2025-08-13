
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  3 17:56:47 2025

@author: DELL-PC
"""
import streamlit as st

st.set_page_config(page_title="College Placement System", page_icon="🎓")

# --- Initialize ---
if "role_selected" not in st.session_state:
    st.session_state.role_selected = None
if "registered_students" not in st.session_state:
    st.session_state.registered_students = {}

# --- PAGE 1: ROLE SELECT ---
if st.session_state.role_selected is None:
    st.title("🎓 College Placement Management System")
    st.subheader("Select your login type:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login as Student"):
            st.session_state.role_selected = "Student"
            st.rerun()
    with col2:
        if st.button("Login as Admin"):
            st.session_state.role_selected = "Admin"
            st.rerun()

# --- PAGE 2: STUDENT LOGIN ---
elif st.session_state.role_selected == "Student":
    st.title("👨‍🎓 Student Login")

    if st.button("⬅️ Back"):
        st.session_state.role_selected = None
        st.rerun()

    student_id = st.text_input("Enter your Student ID")

    if st.button("Login"):
        if student_id in st.session_state.registered_students:
            student = st.session_state.registered_students[student_id]
            st.success(f"🎉 Welcome back, {student['name']}!")
            # TODO: student dashboard
        else:
            st.warning("Student ID not found. Please register below.")
            with st.form("register_form"):
                name = st.text_input("Full Name")
                branch = st.selectbox("Branch", ["CSE", "ECE", "IT", "ME", "EE"])
                year = st.number_input("Year", min_value=1, max_value=4, step=1)
                cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, step=0.1)
                submitted = st.form_submit_button("Register")
                if submitted:
                    st.session_state.registered_students[student_id] = {
                        "name": name,
                        "branch": branch,
                        "year": year,
                        "cgpa": cgpa
                    }
                    st.success("✅ Registered successfully! You can now log in.")
                    st.rerun()
if st.session_state.get("student_logged_in"):
    sid = st.session_state.get("student_id")
    student = st.session_state.registered_students.get(sid, {})
    st.success(f"🎉 Welcome back, {student.get('name', 'Student')}!")

    st.subheader("🎓 Student Dashboard")
    option = st.selectbox("Choose an action", [
        "View My Profile",
        "Apply to Available Companies",
        "View Application Status"
    ])

    if option == "View My Profile":
        st.write(student)

    elif option == "Apply to Available Companies":
        st.info("Eligible companies will be listed here.")
        st.button("Apply")

    elif option == "View Application Status":
        st.info("Applied companies and status will be shown here.")


# --- PAGE 2: ADMIN LOGIN (Optional Placeholder) ---
elif st.session_state.role_selected == "Admin":
    st.title("🔐 Admin Login")

    if st.button("⬅️ Back"):
        st.session_state.role_selected = None
        st.rerun()

    username = st.text_input("Enter Admin Username")
    password = st.text_input("Enter Password", type="password")

    # Temporary admin login (replace with MySQL later)
    if st.button("Login"):
        if username == "admin1" and password == "adminpass":
            st.success(f"✅ Welcome, {username}! You are logged in as Admin.")
            # TODO: Add admin dashboard here
        else:
            st.error("❌ Invalid admin credentials.")

if st.session_state.get('role') == "Student":
    st.subheader("🎓 Student Dashboard")

    option = st.selectbox("Choose an action", [
        "View My Profile",
        "Apply to Available Companies",
        "View Application Status"
    ])

    if option == "View My Profile":
        st.info("Student profile will be displayed here (fetched from MySQL).")

    elif option == "Apply to Available Companies":
        st.info("Eligible companies will be listed here.")
        st.button("Apply")

    elif option == "View Application Status":
        st.info("Applied companies and status will be shown here.")


elif  st.session_state.get('role') == "Admin":
    st.subheader("🛠️ Admin Dashboard")

    admin_option = st.selectbox("Choose an action", [
        "View All Students",
        "Add New Student",
        "View Companies",
        "Add New Company",
        "View Applicants for a Company"
    ])

    if admin_option == "View All Students":
        st.info("Student data table will be shown here.")

    elif admin_option == "Add New Student":
        with st.form("add_student_form"):
            sid = st.text_input("Student ID")
            name = st.text_input("Name")
            branch = st.selectbox("Branch", ["CSE", "ECE", "IT", "ME"])
            year = st.number_input("Year", 1, 4)
            cgpa = st.number_input("CGPA", 0.0, 10.0, step=0.1)
            st.form_submit_button("Add Student")

    elif admin_option == "View Companies":
        st.info("Company list will be displayed here.")

    elif admin_option == "Add New Company":
        with st.form("add_company_form"):
            cid = st.text_input("Company ID")
            cname = st.text_input("Company Name")
            allowed_branches = st.multiselect("Allowed Branches", ["CSE", "ECE", "IT", "ME"])
            required_cgpa = st.number_input("Required CGPA", 0.0, 10.0, step=0.1)
            st.form_submit_button("Add Company")

    elif admin_option == "View Applicants for a Company":
        selected_company = st.selectbox("Select Company", ["Company A", "Company B"])
        st.info("List of applicants will appear here.")
