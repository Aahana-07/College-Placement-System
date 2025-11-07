# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 13:31:15 2025

@author: Aahan
"""
import matplotlib.pyplot as plt
import streamlit as st
import mysql.connector
import pandas as pd
from db import get_connection

# ✅ Must be the very first Streamlit command
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
    st.markdown("<h1 style='text-align:center;'>🎓 College Placement System</h1>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>Select Login Role</h3>", unsafe_allow_html=True)

    # ✅ Custom CSS styling
    st.markdown("""
<style>
div.stButton > button {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 200px;          /* ⬅ smaller width */
    height: 200px;         /* ⬅ smaller height */
    border-radius: 20px;
    border: 2px solid #4CAF50;
    background-color: #111;
    color: white;
    font-size: 20px;       
    transition: all 0.2s ease-in-out;
    padding: 20px;
}

div.stButton > button:hover {
    background-color: #4CAF50;
    color: black;
    transform: scale(1.05);
}


div.stButton > button span:first-child {
    font-size: 70px !important; /* ⬅ emoji size stays prominent */
    line-height: 1 !important;
    display: block;
}

div.stButton > button p {
    font-size: 24px !important;
    margin-top: 5px;
}

/* ✅ Small shift for right alignment */
.block-container div[data-testid="column"]:nth-child(2) {
    margin-left: 30px; /* shift the right box slightly */
}
</style>
""", unsafe_allow_html=True)


    # ✅ Centered buttons inside two columns
   # center with side spacing columns
    col_space1, col1, col2, col_space2 = st.columns([1, 2, 2, 1], gap="large")

    with col1:
       if st.button("👨‍🎓\nStudent"):
        st.session_state.page = "student_login"
        st.rerun()

    with col2:
       if st.button("🧑‍💼\nAdmin"):
        st.session_state.page = "admin_login"
        st.rerun()

# -------------------- END OF HOME PAGE --------------------






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
         st.session_state.student_roll_no = student["roll_no"]  # store roll number separately
         st.session_state.student_id = student["id"]            # store actual numeric ID for FK
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
    # ✅ Add Sidebar Navigation for Students
    st.sidebar.title("🎓 Student Menu")

    if st.sidebar.button("🏠 Dashboard"):
        st.session_state.page = "student_dashboard"
        st.rerun()

    if st.sidebar.button("👤 View Profile"):
        st.session_state.page = "view_profile"
        st.rerun()

    if st.sidebar.button("🏢 View Companies"):
        st.session_state.page = "view_companies"
        st.rerun()

    if st.sidebar.button("🚪 Logout"):
        st.session_state.page = "home"
        st.session_state.student_id = None
        st.session_state.student_name = None
        st.rerun()

    # --- Dashboard main area ---
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE id = %s", (st.session_state.student_id,))
    student = cursor.fetchone()
    conn.close()


    if student:
     st.markdown("""
        <h2 style='text-align:center; color:#4CAF50;'>🎓 Student Dashboard</h2>
        <hr style='border:1px solid #444;'>
    """, unsafe_allow_html=True)

    # --- Welcome Message ---
    st.markdown(f"<h4 style='color:white;'>Welcome back, <span style='color:#4CAF50;'>{student['name']}</span> 👋</h4>", unsafe_allow_html=True)

    # --- Quick Stats Section (Live Data from Database) ---
    st.markdown("### 📊 Overview")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM companies")
    total_companies = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE student_id = %s", (st.session_state.student_id,))
    total_applications = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*) 
    FROM applications a
    INNER JOIN students s ON a.student_id = s.id
    WHERE s.roll_no = %s
""", (st.session_state.student_roll_no,))
    total_applications = cursor.fetchone()[0]


    conn.close()

    col1, col2 = st.columns(2)
    col1.metric("🏢 Registered Companies", total_companies)
    col2.metric("📨 Applications Sent", total_applications)
    


    # --- Recent Company Drives ---
    st.markdown("<br><h4 style='color:#4CAF50;'>📢 Latest Company Drives</h4>", unsafe_allow_html=True)
    import pandas as pd
    data = [
        {"Company": "TCS", "Role": "Software Engineer", "Deadline": "Nov 10"},
        {"Company": "Infosys", "Role": "System Analyst", "Deadline": "Nov 15"},
        {"Company": "Wipro", "Role": "Data Intern", "Deadline": "Nov 18"},
    ]
    st.table(pd.DataFrame(data))






# -------------------- VIEW PROFILE --------------------
elif st.session_state.page == "view_profile":
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE id = %s", (st.session_state.student_id,))
    student = cursor.fetchone()
    conn.close()

    st.header("👤 My Profile")

    if student:
        st.write(f"**Roll No:** {student['roll_no']}")
        st.write(f"**Name:** {student['name']}")
        st.write(f"**Email:** {student['email']}")
        st.write(f"**Branch:** {student['branch']}")
        st.write(f"**Year:** {student.get('year', 'N/A')}")
        st.write(f"**CGPA:** {student.get('cgpa', 'N/A')}")
        st.write(f"**Created On:** {student['created_date']}")
    else:
        st.warning("⚠️ Student record not found. Please check your registration.")

    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "student_dashboard"
        st.rerun()



# -------------------- VIEW COMPANIES --------------------
elif st.session_state.page == "view_companies":
    st.subheader("🏢 Companies Visiting Campus")

    # Fetch companies
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM companies")
        companies = cursor.fetchall()
    except Exception as e:
        st.error("Error fetching companies from the database.")
        st.write(e)
        companies = []
    finally:
        try:
            cursor.close()
        except:
            pass
        conn.close()

    if not companies:
        st.info("No companies available right now.")
    else:
        for company in companies:
            with st.container():
                st.markdown(f"### {company.get('name', 'Company')}")
                st.write(f"**Role:** {company.get('role', 'N/A')}")
                st.write(f"**Package:** {company.get('package', 'N/A')} LPA")
                st.write(f"**Branch Eligible:** {company.get('branch', 'N/A')}")

                # Unique keys per company
                apply_key = f"apply_btn_{company['id']}"
                toggle_key = f"show_form_{company['id']}"
                form_key = f"form_{company['id']}"

                # Initialize toggle state if not present
                if toggle_key not in st.session_state:
                    st.session_state[toggle_key] = False

                # --- Check if student already applied ---
                conn_check = get_connection()
                try:
                    cur_check = conn_check.cursor(dictionary=True)
                    cur_check.execute(
                        "SELECT * FROM applications WHERE student_id = %s AND company_id = %s",
                        (st.session_state.get("student_id"), company["id"]),
                    )
                    already_applied = cur_check.fetchone()
                except Exception as e:
                    st.error("Error checking application status.")
                    already_applied = None
                finally:
                    try:
                        cur_check.close()
                    except:
                        pass
                    conn_check.close()

                # --- If already applied, show a badge ---
                if already_applied:
                    st.markdown("<span style='color:#4CAF50;'>✅ Applied</span>", unsafe_allow_html=True)
                else:
                    # Apply button toggles visibility of the form
                    if st.button(f"📨 Apply to {company.get('name', 'Company')}", key=apply_key):
                        st.session_state[toggle_key] = not st.session_state[toggle_key]
                        st.rerun()

                    # Show form when toggled on
                    if st.session_state[toggle_key]:
                        st.markdown(
                            "<br><h4 style='color:#4FC3F7;'>📝 Apply Form</h4>",
                            unsafe_allow_html=True
                        )

                        with st.form(key=form_key):
                            student_name = st.text_input("Enter your Name")
                            branch = st.text_input("Enter your Branch")
                            cgpa = st.number_input(
                                "Enter your CGPA",
                                min_value=0.0,
                                max_value=10.0,
                                step=0.1
                            )

                            submitted = st.form_submit_button(f"Apply to {company.get('name', 'Company')}")

                            if submitted:
                                student_id = st.session_state.get("student_id")

                                if not student_id:
                                    st.error("⚠️ You must be logged in as a student to apply. Go to Home → Student Login.")
                                else:
                                    conn2 = get_connection()
                                    try:
                                        cur2 = conn2.cursor()
                                        cur2.execute(
                                            """
                                            INSERT INTO applications
                                            (student_id, company_id, student_name, branch, cgpa, company_name, status, applied_date)
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, CURDATE())
                                            """,
                                            (
                                                student_id,
                                                company["id"],
                                                student_name,
                                                branch,
                                                cgpa,
                                                company.get("name", ""),
                                                "Applied",
                                            ),
                                        )
                                        conn2.commit()

                                        st.success(f"✅ Successfully applied to {company.get('name', 'Company')}!")
                                        import time
                                        time.sleep(2)
                                        st.session_state[toggle_key] = False
                                        st.rerun()

                                    except Exception as e:
                                        conn2.rollback()
                                        st.error("Failed to apply. See error below.")
                                        st.write(e)
                                    finally:
                                        try:
                                            cur2.close()
                                        except:
                                            pass
                                        conn2.close()

                st.markdown("---")


   
    if st.button("⬅ Back to Dashboard"):
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
            st.session_state.page = "admin_dashboard"
            st.session_state.admin_username = admin.get("username", "")
            st.rerun()
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
    st.header("🧑‍💼 Register New Admin")

    with st.form("admin_form"):
        email = st.text_input("Enter Email")
        username = st.text_input("Create Username")
        password = st.text_input("Create Password", type="password")
        submit = st.form_submit_button("Register")

    if submit:
        if email and username and password:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO admins (email, username, password) VALUES (%s, %s, %s)",
                (email, username, password)
            )
            conn.commit()
            conn.close()
            st.success("✅ Admin registered successfully!")
            st.session_state.page = "admin_login"
            st.rerun()
        else:
            st.error("Please fill in all the fields before registering.")

    if st.button("← Back to Login"):
        st.session_state.page = "admin_login"
        st.rerun()

# -------------------- ADMIN DASHBOARD --------------------
elif st.session_state.page == "admin_dashboard":
    import matplotlib.pyplot as plt

    st.title("🎓 Admin Dashboard")

    # --- ✅ Styled Sidebar Navigation ---
    st.sidebar.markdown(
        """
        <h2 style='text-align:center; color:white;'> Navigation</h2>
        <hr style='border:1px solid #444;'>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        div.stButton > button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            padding: 10px 0;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            margin-bottom: 8px;
            transition: all 0.3s ease;
        }
        div.stButton > button:hover {
            background-color: #45a049;
            transform: scale(1.05);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Sidebar buttons        
    if st.sidebar.button("🏠 Dashboard"):
       st.session_state.admin_tab = "Dashboard"
    if st.sidebar.button("👥 Students"):
       st.session_state.admin_tab = "Students"
    if st.sidebar.button("📄 Applications"):
       st.session_state.admin_tab = "Applications"
    if st.sidebar.button("📊 Analytics"):
       st.session_state.admin_tab = "Analytics"

    if st.sidebar.button("🚪 Logout"):
        st.session_state.page = "admin_login"
        st.rerun()

    # Default tab
    if "admin_tab" not in st.session_state:
        st.session_state.admin_tab = "Dashboard"

    # --- Database Connection ---
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students_data = cursor.fetchall()
    conn.close()

    students_df = pd.DataFrame(students_data)

    # --- Dashboard Home ---
    if st.session_state.admin_tab == "Dashboard":
        st.subheader("📊 Overview")

        if not students_df.empty:
            col1, col2, col3 = st.columns(3)
            col1.metric("👨‍🎓 Total Students", len(students_df))
            col2.metric("🏫 Total Branches", students_df["branch"].nunique())
            col3.metric("🎯 Average CGPA", round(students_df["cgpa"].mean(), 2))

            st.markdown("---")
            st.dataframe(students_df, use_container_width=True)
        else:
            st.warning("No student data available yet.")

    # --- Students Tab ---
    elif st.session_state.admin_tab == "Students":
        st.subheader("🧾 Student Records")
        if not students_df.empty:
            search = st.text_input("🔍 Search by name or roll no:")
            if search:
                students_df = students_df[
                    students_df["name"].str.contains(search, case=False)
                    | students_df["roll_no"].str.contains(search, case=False)
                ]
            st.dataframe(students_df, use_container_width=True)
        else:
            st.info("No students found in the database.")
            
            
       # --- Applications Tab ---
    elif st.session_state.admin_tab == "Applications":
        st.subheader("📄 Student Applications Summary")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                s.name AS student_name,
                s.roll_no,
                s.branch,
                s.cgpa,
                GROUP_CONCAT(DISTINCT c.name ORDER BY c.name SEPARATOR ', ') AS companies_applied,
                MAX(a.applied_date) AS last_applied
            FROM applications a
            INNER JOIN students s ON a.student_id = s.id
            INNER JOIN companies c ON a.company_id = c.id
            GROUP BY s.id, s.name, s.roll_no, s.branch, s.cgpa
            ORDER BY last_applied DESC;
        """)

        results = cursor.fetchall()
        conn.close()

        if results and len(results) > 0:
            df = pd.DataFrame(results)
            df.rename(columns={
                "student_name": "Student Name",
                "roll_no": "Roll No",
                "branch": "Branch",
                "cgpa": "CGPA",
                "companies_applied": "Companies Applied",
                "last_applied": "Last Application Date"
            }, inplace=True)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No application summary data available.")

       # --- Analytics Tab ---
    elif st.session_state.admin_tab == "Analytics":
        st.subheader("📈 Placement Analytics")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # 1️⃣ --- Chart 1: Students per Branch ---
        st.markdown("### 🎓 Students per Branch")
        cursor.execute("SELECT branch, COUNT(*) AS count FROM students GROUP BY branch")
        branch_data = cursor.fetchall()

        if branch_data:
            df1 = pd.DataFrame(branch_data)
            fig1, ax1 = plt.subplots()
            ax1.bar(df1["branch"], df1["count"])
            ax1.set_xlabel("Branch")
            ax1.set_ylabel("Number of Students")
            ax1.set_title("Students per Branch")
            st.pyplot(fig1)
        else:
            st.info("No student data found.")
        st.markdown("---")

        # 2️⃣ --- Chart 2: Companies vs Students Placed ---
        st.markdown("### 🏢 Companies vs Students Placed")
        cursor.execute("""
    SELECT 
        c.name AS company_name,
        COUNT(a.student_id) AS students_placed
    FROM companies c
    LEFT JOIN applications a 
        ON c.id = a.company_id 
    GROUP BY c.name
    ORDER BY students_placed DESC;
""")

        placement_data = cursor.fetchall()

        if placement_data:
            df2 = pd.DataFrame(placement_data)
            fig2, ax2 = plt.subplots()
            ax2.bar(df2["company_name"], df2["students_placed"])
            ax2.set_xlabel("Company")
            ax2.set_ylabel("Students Placed")
            ax2.set_title("Companies vs Students Placed")
            st.pyplot(fig2)
        else:
            st.info("No placement data found yet.")
        st.markdown("---")

        # 3️⃣ --- Chart 3: Year vs Students Placed (Demo Histogram) ---
        st.markdown("### 📊 Year vs Students Placed")

        data = {
            "Year": ["2020", "2021", "2022", "2023", "2024"],
            "Students_Placed": [45, 58, 76, 83, 92]
        }
        df3 = pd.DataFrame(data)

        fig3, ax3 = plt.subplots()
        ax3.bar(df3["Year"], df3["Students_Placed"])
        ax3.set_xlabel("Year")
        ax3.set_ylabel("Number of Students Placed")
        ax3.set_title("Year vs Students Placed")
        st.pyplot(fig3)

        cursor.close()
        conn.close()






