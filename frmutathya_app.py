import streamlit as st
import pandas as pd
from datetime import datetime
import sqlite3
import os

st.set_page_config(page_title="Tathya - Case Management", page_icon="🔎", layout="wide")

conn = sqlite3.connect("tathya_cases.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS cases (
        case_id TEXT PRIMARY KEY,
        customer TEXT,
        type TEXT,
        region TEXT,
        category TEXT,
        state TEXT,
        city TEXT,
        product TEXT,
        referred_by TEXT,
        loan_amount REAL,
        fraud_loss REAL,
        recovery REAL,
        date TEXT,
        description TEXT,
        document_path TEXT,
        reviewer_cat TEXT,
        reviewer_fraud_type TEXT,
        reviewer_l1_mgr TEXT,
        reviewer_l2_mgr TEXT,
        reviewer_status TEXT,
        reviewer_pending_stage TEXT,
        reviewer_remarks TEXT,
        approver_name TEXT,
        approver_id TEXT,
        approver_role TEXT
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )
""")
conn.commit()

st.markdown("""
    <style>
        body { background-color: #FFF4D9; }
        .stButton>button {
            background-color: #C7222A; color: white;
            border: none; padding: 0.4rem 1rem;
            font-weight: 600;
        }
        .stButton>button:hover { background-color: #8B151B; }
        .top-left-logo { position: absolute; top: 10px; left: 10px; }
        .top-right-logo { position: absolute; top: 10px; right: 10px; }
        .user-role-box { position: absolute; top: 70px; right: 10px; background-color: #F5F5F5;
            padding: 4px 10px; font-size: 13px; color: #333; border-radius: 4px; }
        .footer { position: fixed; bottom: 5px; left: 10px; font-size: 13px;
            color: #888; font-style: italic; }
        h1, h2, h3, .title { font-family: 'Segoe UI'; color: #C7222A; font-weight: bold; font-size: 24px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="top-left-logo"><img src="https://yourdomain.com/tathya-logo.png" height="60"></div>', unsafe_allow_html=True)
st.markdown('<div class="top-right-logo"><img src="https://yourdomain.com/abcl-logo.png" height="50"></div>', unsafe_allow_html=True)
if "role" in st.session_state:
    st.markdown(f'<div class="user-role-box">Role: {st.session_state["role"]}</div>', unsafe_allow_html=True)
st.markdown('<div class="footer">Powered by <strong>FRMU Sanjeevani</strong></div>', unsafe_allow_html=True)

USERS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "initiator": {"password": "init123", "role": "Initiator"},
    "reviewer": {"password": "review123", "role": "Reviewer"},
    "approver": {"password": "approve123", "role": "Approver"}
}

def login():
    st.title("🔐 Tathya Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        if submit:
            if username in USERS and USERS[username]["password"] == password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.role = USERS[username]["role"]
                st.rerun()
            else:
                st.error("Invalid credentials")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    login()
    st.stop()

role = st.session_state.get("role")
menu = st.sidebar.radio("📁 Menu", [
    "Dashboard", "Case Entry", "Analytics", "Reviewer Panel", "Approver Panel"] + (["Admin Panel"] if role == "Admin" else []))
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"authenticated": False}))

reviewer_l1 = ["Aditya Annamraju", "Alphanso Nagalapurkar", "AdAnthuvan Lourdusamy", "Dipesh Makawana", "Goutam Barman", "Jagruti Bane", "K Guruprasath", "Manmeet Singh", "Pramod Kumar", "Ramandeep Singh", "Rohit Shirwadkar", "Shilpy Dua", "Thiyagarajan Shanmugasundaram"]
reviewer_l2 = ["AdAnthuvan Lourdusamy", "Manmeet Singh", "Ramandeep Singh", "Rohit Shirwadkar", "Suhas Bhalerao"]
approvers = ["Suhas", "Ajay Kanth"]
approver_ids = ["10001", "10002"]
approver_roles = ["Lead-Investigation", "Head-FRMU"]

if menu == "Dashboard":
    st.markdown("<h1 class='title'>📊 Case Level Dashboard</h1>", unsafe_allow_html=True)
    df = pd.read_sql("SELECT * FROM cases", conn)
    if not df.empty:
        st.dataframe(df.style.set_properties(**{'background-color': '#fff', 'color': '#000'}).format({
            'loan_amount': '{:.2f}', 'fraud_loss': '{:.2f}', 'recovery': '{:.2f}'
        }))
    else:
        st.info("No cases found.")

elif menu == "Case Entry" and role == "Initiator":
    st.markdown("<h1 class='title'>📄 Case Entry</h1>", unsafe_allow_html=True)
    with st.form("case_form"):
        col1, col2 = st.columns(2)
        with col1:
            case_id = st.text_input("Case ID")
            customer = st.text_input("Customer Name")
            loan_amt = st.number_input("Loan Amount (in Lacs)", 0.0)
            fraud_loss = st.number_input("Fraud Loss to Company (in Lacs)", 0.0)
            recovery = st.number_input("RCU Recovery (in Lacs)", 0.0)
            case_type = st.selectbox("Type of Case", ["Lending", "Non-Lending"])
            region = st.selectbox("Region", ["East", "West", "North", "South"])
        with col2:
            date = st.date_input("Case Date", datetime.today())
            description = st.text_area("Case Description")
            category = st.selectbox("Category", ["Fraud", "Non-Fraud", "Under Investigation"])
            state = st.text_input("State")
            city = st.text_input("City")
            product = st.text_input("Product")
            referred_by = st.text_input("Referred By")
        doc = st.file_uploader("Upload Document (PDF/Image)", type=["pdf", "jpg", "png"])
        submitted = st.form_submit_button("Submit Case")
        if submitted:
            cursor.execute("SELECT 1 FROM cases WHERE case_id = ?", (case_id,))
            if cursor.fetchone():
                st.error("⚠️ Case ID already exists.")
            elif case_id and customer:
                file_path = f"uploads/{case_id}_{doc.name}" if doc else ""
                if doc:
                    os.makedirs("uploads", exist_ok=True)
                    with open(file_path, "wb") as f: f.write(doc.read())
                cursor.execute("""
                    INSERT INTO cases VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '', '', '', '', '', '', '', '', '', '')
                """, (case_id, customer, case_type, region, category, state, city, product, referred_by, loan_amt, fraud_loss, recovery, str(date), description, file_path))
                conn.commit()
                st.success("✅ Case added successfully")
            else:
                st.error("All required fields must be filled")

elif menu == "Admin Panel" and role == "Admin":
    st.markdown("<h1 class='title'>👤 Admin - User Management</h1>", unsafe_allow_html=True)
    with st.form("add_user"):
        uname = st.text_input("New Username")
        pwd = st.text_input("Password", type="password")
        role_opt = st.selectbox("Role", ["Initiator", "Reviewer", "Approver"])
        submit = st.form_submit_button("Add User")
        if submit:
            try:
                cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (uname, pwd, role_opt))
                conn.commit()
                st.success("✅ User added successfully")
            except sqlite3.IntegrityError:
                st.error("❌ Username already exists")

elif menu == "Analytics":
    st.markdown("<h1 class='title'>📈 Analytics</h1>", unsafe_allow_html=True)
    st.info("Analytics will be added soon with charts and KPIs.")
