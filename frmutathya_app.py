import streamlit as st
import pandas as pd
from datetime import datetime

# --- Config ---
st.set_page_config(page_title="Tathya - Case Management", page_icon="🔎", layout="wide")

# --- Style ---
st.markdown("""
    <style>
        body { background-color: #FFF4D9; }
        .stButton>button {
            background-color: #C7222A; color: white;
            border: none; padding: 0.4rem 1rem;
            font-weight: 600;
        }
        .stButton>button:hover { background-color: #8B151B; }
        .top-left-logo {
            position: absolute;
            top: 10px;
            left: 10px;
        }
        .top-right-logo {
            position: absolute;
            top: 10px;
            right: 10px;
        }
        .footer {
            position: fixed;
            bottom: 5px;
            width: 100%;
            text-align: center;
            font-size: 13px;
            color: #888;
            font-style: italic;
        }
    </style>
""", unsafe_allow_html=True)

# --- Global UI Elements ---
st.markdown('<div class="top-left-logo"><img src="https://yourdomain.com/tathya-logo.png" height="60"></div>', unsafe_allow_html=True)
st.markdown('<div class="top-right-logo"><img src="https://yourdomain.com/abcl-logo.png" height="50"></div>', unsafe_allow_html=True)
st.markdown('<div class="footer">Powered by <strong>FRMU Sanjeevani</strong></div>', unsafe_allow_html=True)

# --- Users ---
USERS = {
    "admin": {"password": "admin123", "role": "Initiator"},
    "reviewer": {"password": "review123", "role": "Reviewer"},
    "approver": {"password": "approve123", "role": "Approver"}
}

# --- Login ---
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
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("Invalid credentials")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    login()
    st.stop()

# --- Main App ---
role = st.session_state.get("role")
menu = st.sidebar.radio("📁 Navigate", ["Home", "Case Entry", "Reviewer Panel", "Approver Panel"])
st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"authenticated": False}))

# --- Session Storage ---
if "cases" not in st.session_state:
    st.session_state.cases = []

# --- Dummy Masters ---
reviewer_l1 = ["Aditya Annamraju", "Alphanso Nagalapurkar", "AdAnthuvan Lourdusamy", "Dipesh Makawana", "Goutam Barman", "Jagruti Bane", "K Guruprasath", "Manmeet Singh", "Pramod Kumar", "Ramandeep Singh", "Rohit Shirwadkar", "Shilpy Dua", "Thiyagarajan Shanmugasundaram"]
reviewer_l2 = ["AdAnthuvan Lourdusamy", "Manmeet Singh", "Ramandeep Singh", "Rohit Shirwadkar", "Suhas Bhalerao"]
approvers = ["Suhas", "Ajay Kanth"]
approver_ids = ["10001", "10002"]
approver_roles = ["Lead-Investigation", "Head-FRMU"]

# --- Home ---
if menu == "Home":
    st.markdown("""
        <h1 style='color:#C7222A;'>🔎 Welcome to Tathya</h1>
        <p style='font-size:18px;'>Case Management Platform - Role: <strong>{}</strong></p>
    """.format(role), unsafe_allow_html=True)

# --- Case Entry ---
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
                new_case = {
                    "Case ID": case_id,
                    "Customer": customer,
                    "Type": case_type,
                    "Region": region,
                    "Category": category,
                    "State": state,
                    "City": city,
                    "Product": product,
                    "Referred By": referred_by,
                    "Loan Amount": loan_amt,
                    "Fraud Loss": fraud_loss,
                    "RCU Recovery": recovery,
                    "Date": str(date),
                    "Description": description
                }
                st.session_state.cases.append(new_case)
                st.success("✅ Case added successfully")
            else:
                st.error("All required fields must be filled")

# --- Reviewer Panel ---
elif menu == "Reviewer Panel" and role == "Reviewer":
    st.subheader("🔍 Reviewer Case View")
    if not st.session_state.cases:
        st.warning("No cases to review")
    else:
        selected = st.selectbox("Select Case", [c["Case ID"] for c in st.session_state.cases])
        case = next(c for c in st.session_state.cases if c["Case ID"] == selected)
        st.json(case)  # Read-only view for now

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
                st.success("✅ Reviewer input saved")

# --- Approver Panel ---
elif menu == "Approver Panel" and role == "Approver":
    st.subheader("🔐 Approver Panel")
    if not st.session_state.cases:
        st.warning("No cases to approve")
    else:
        selected = st.selectbox("Select Case to Approve", [c["Case ID"] for c in st.session_state.cases])
        case = next(c for c in st.session_state.cases if c["Case ID"] == selected)
        st.json(case)

        st.markdown("---")
        st.markdown("### ✅ Approval Form")
        with st.form("approver_form"):
            name = st.selectbox("Approved by Name", approvers)
            aid = st.selectbox("Approved by ID", approver_ids)
            role = st.selectbox("Approved by Role", approver_roles)
            submit = st.form_submit_button("Submit Approval")
            if submit:
                st.success(f"✅ Case {selected} approved by {name} ({role})")
