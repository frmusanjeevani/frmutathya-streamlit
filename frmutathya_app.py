import streamlit as st
import pandas as pd
from datetime import datetime
import sqlite3

st.set_page_config(page_title="Tathya - Case Management", page_icon="🔎", layout="wide")

conn = sqlite3.connect("/mnt/data/tathya_cases.db", check_same_thread=False)
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
        .footer { position: fixed; bottom: 5px; width: 100%; text-align: center; font-size: 13px;
            color: #888; font-style: italic; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="top-left-logo"><img src="https://yourdomain.com/tathya-logo.png" height="60"></div>', unsafe_allow_html=True)
st.markdown('<div class="top-right-logo"><img src="https://yourdomain.com/abcl-logo.png" height="50"></div>', unsafe_allow_html=True)
if "role" in st.session_state:
    st.markdown(f'<div class="user-role-box">Role: {st.session_state["role"]}</div>', unsafe_allow_html=True)
st.markdown('<div class="footer">Powered by <strong>FRMU Sanjeevani</strong></div>', unsafe_allow_html=True)

USERS = {
    "admin": {"password": "admin123", "role": "Initiator"},
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
menu = st.sidebar.radio("📁 Menu", ["Dashboard", "Analytics", "Case Entry", "Reviewer Panel", "Approver Panel"])
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"authenticated": False}))

reviewer_l1 = ["Aditya Annamraju", "Alphanso Nagalapurkar", "AdAnthuvan Lourdusamy", "Dipesh Makawana", "Goutam Barman", "Jagruti Bane", "K Guruprasath", "Manmeet Singh", "Pramod Kumar", "Ramandeep Singh", "Rohit Shirwadkar", "Shilpy Dua", "Thiyagarajan Shanmugasundaram"]
reviewer_l2 = ["AdAnthuvan Lourdusamy", "Manmeet Singh", "Ramandeep Singh", "Rohit Shirwadkar", "Suhas Bhalerao"]
approvers = ["Suhas", "Ajay Kanth"]
approver_ids = ["10001", "10002"]
approver_roles = ["Lead-Investigation", "Head-FRMU"]

if menu == "Dashboard":
    st.title("📊 Case Level Dashboard")
    df = pd.read_sql("SELECT * FROM cases", conn)
    st.dataframe(df)

elif menu == "Case Entry" and role == "Initiator":
    st.subheader("📄 Enter New Case")
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
        submitted = st.form_submit_button("Submit Case")
        if submitted:
            if case_id and customer:
                cursor.execute("""
                    INSERT INTO cases VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '', '', '', '', '', '', '', '', '', '')
                """, (case_id, customer, case_type, region, category, state, city, product, referred_by, loan_amt, fraud_loss, recovery, str(date), description))
                conn.commit()
                st.success("✅ Case added successfully")
            else:
                st.error("All required fields must be filled")

elif menu == "Reviewer Panel" and role == "Reviewer":
    st.subheader("🔍 Reviewer Case View")
    df = pd.read_sql("SELECT * FROM cases", conn)
    if df.empty:
        st.warning("No cases available")
    else:
        selected = st.selectbox("Select Case", df["case_id"])
        selected_case = df[df["case_id"] == selected].iloc[0]
        st.json(selected_case.to_dict())
        st.markdown("---")
        st.markdown("### 📝 Reviewer Inputs")
        with st.form("reviewer_form"):
            cat = st.selectbox("Case Categorization", ["Fraud", "Non-Fraud", "Under Investigation"])
            fraud_type = st.selectbox("Fraud/Others Classification", ["Identity Theft"])
            l1_mgr = st.selectbox("Investigation Manager (L1)", reviewer_l1)
            l2_mgr = st.selectbox("Investigation Manager (L2)", reviewer_l2)
            status = st.selectbox("Investigation Status", ["Closed", "Pending"])
            pending_stage = st.selectbox("Pending Stage", ["SCN Issuance In-progress", "Stage 1 - Awaiting complete case facts/information", "Stage 3 - Investigation Under Progress (L1)", "Stage 4 - Investigation Under Progress (L2)", "Stage 5 - Awaiting NH Review/Approval for IR/FMR"])
            remarks = st.text_area("Investigation Remarks")
            submit = st.form_submit_button("Submit Review")
            if submit:
                cursor.execute("""
                    UPDATE cases SET reviewer_cat=?, reviewer_fraud_type=?, reviewer_l1_mgr=?, reviewer_l2_mgr=?,
                    reviewer_status=?, reviewer_pending_stage=?, reviewer_remarks=? WHERE case_id=?
                """, (cat, fraud_type, l1_mgr, l2_mgr, status, pending_stage, remarks, selected))
                conn.commit()
                st.success("✅ Review submitted")

elif menu == "Approver Panel" and role == "Approver":
    st.subheader("🔐 Approver Panel")
    df = pd.read_sql("SELECT * FROM cases", conn)
    if df.empty:
        st.warning("No cases to approve")
    else:
        selected = st.selectbox("Select Case", df["case_id"])
        selected_case = df[df["case_id"] == selected].iloc[0]
        st.json(selected_case.to_dict())
        st.markdown("### ✅ Approval Form")
        with st.form("approver_form"):
            name = st.selectbox("Approved by Name", approvers)
            aid = st.selectbox("Approved by ID", approver_ids)
            arole = st.selectbox("Approved by Role", approver_roles)
            submit = st.form_submit_button("Submit Approval")
            if submit:
                cursor.execute("""
                    UPDATE cases SET approver_name=?, approver_id=?, approver_role=? WHERE case_id=?
                """, (name, aid, arole, selected))
                conn.commit()
                st.success(f"✅ Approved case {selected}")

elif menu == "Analytics":
    st.subheader("📈 Analytics")
    st.info("Analytics will be added soon with charts and KPIs.")
