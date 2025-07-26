import streamlit as st
import pandas as pd
from datetime import datetime
import sqlite3
import os

st.set_page_config(page_title="Tathya - Case Management", page_icon="🔎", layout="centered")

conn = sqlite3.connect("tathya_cases.db", check_same_thread=False)
cursor = conn.cursor()

# === LOGIN STYLING & SESSION ===
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
        .login-container { max-width: 400px; margin: auto; background-color: #fff5e1; padding: 2rem; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="top-left-logo"><img src="https://yourdomain.com/tathya-logo.png" height="60"></div>', unsafe_allow_html=True)
st.markdown('<div class="top-right-logo"><img src="https://yourdomain.com/abcl-logo.png" height="50"></div>', unsafe_allow_html=True)
if "role" in st.session_state:
    st.markdown(f'<div class="user-role-box">Role: {st.session_state["role"]}</div>', unsafe_allow_html=True)
st.markdown('<div class="footer">Powered by <strong>FRMU Sanjeevani</strong></div>', unsafe_allow_html=True)

# === USERS ===
USERS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "initiator": {"password": "init123", "role": "Initiator"},
    "reviewer": {"password": "review123", "role": "Reviewer"},
    "approver": {"password": "approve123", "role": "Approver"},
    "legal": {"password": "legal123", "role": "Legal Reviewer"},
    "closure": {"password": "closure123", "role": "Action Closure Authority"}
}

# === LOGIN ===
def login():
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
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
        st.markdown('</div>', unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    login()
    st.stop()

# === AFTER LOGIN ===
st.sidebar.title("📁 Navigation")
MENU_OPTIONS = ["Dashboard", "Case Entry", "Analytics"]
if st.session_state.role == "Reviewer":
    MENU_OPTIONS.append("Reviewer Panel")
elif st.session_state.role == "Approver":
    MENU_OPTIONS.append("Approver Panel")
elif st.session_state.role == "Legal Reviewer":
    MENU_OPTIONS.extend(["Legal - SCN", "Legal - Orders"])
elif st.session_state.role == "Action Closure Authority":
    MENU_OPTIONS.append("Closure Actions")
elif st.session_state.role == "Admin":
    MENU_OPTIONS.append("User Admin")
menu = st.sidebar.radio("Go to", MENU_OPTIONS)

st.title(f"Welcome {st.session_state.username}")

if menu == "Dashboard":
    st.subheader("📊 Case Level Dashboard")
    df = pd.read_sql("SELECT * FROM cases", conn)
    st.dataframe(df)

elif menu == "Analytics":
    st.subheader("📈 Analytics")
    st.info("Coming soon...")

elif menu == "Case Entry" and st.session_state.role == "Initiator":
    st.subheader("📄 Enter New Case")
    # (You will implement the single-row input form here)

elif menu == "Reviewer Panel" and st.session_state.role == "Reviewer":
    st.subheader("📝 Reviewer Panel")
    # (Reviewer logic)

elif menu == "Approver Panel" and st.session_state.role == "Approver":
    st.subheader("✅ Approver Panel")
    # (Approver logic)

elif menu == "Legal - SCN":
    st.subheader("📄 Generate Show Cause Notice")
    # (Legal Show Cause form logic)

elif menu == "Legal - Orders":
    st.subheader("📘 Generate Reasoned Order")
    # (Legal Reasoned Order logic)

elif menu == "Closure Actions":
    st.subheader("🔒 Action Closure Authority")
    # (Action Closure form logic)

elif menu == "User Admin" and st.session_state.role == "Admin":
    st.subheader("👤 User Management")
    # (Admin logic to add users)

# === DROPDOWN MASTER ===
TYPE_OPTIONS = ["Lending", "Non Lending"]
CATEGORY_OPTIONS = TYPE_OPTIONS
REGION_OPTIONS = ["East", "North", "South", "West"]
STATE_OPTIONS = ["Andhra Pradesh", "Assam", "Bengaluru", "Bihar", "Chattisgarh", "Chhattisgarh", "Delhi", "Ghodapada", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Odisha", "Punjab", "Raipur", "Rajasthan", "Tamil Nadu", "Telangana", "Uttar Pradesh", "Uttarakhand", "West Bengal"]
CITY_OPTIONS = ["Agra", "Ahemdabad", "Ahmedabad", "Ajmer", "Akkalkuwa", "Akola", "Alamwala", "Aligarh", "Allahabad", "Alwar", "Ambala", "Ambernath", "Ambikapur", "Amdanga", "Amravati", "Amritsar", "Ad", "Angul", "Arambag", "Arrah", "Asansol", "Aurangabad", "Badlapur", "Badvel", "Bahadurgarh", "Balangir"]
PRODUCT_OPTIONS = ["BL", "BTC PL", "DL", "Drop Line LOC", "Finagg", "INSTI - MORTGAGES", "LAP", "Line of Credit", "MLAP", "NA", "PL", "SEG", "SME", "STSL", "STSLP BT + Top - up", "STUL", "Term Loan", "Term Loan Infra", "Udyog Plus", "Unsecured BuyOut"]
REFERRED_BY_OPTIONS = ["Audit Team", "Business Unit", "Collection Unit", "Compliance Team", "Credit Unit", "Customer Service", "GRT", "HR", "Legal Unit", "MD / CEO Escalation", "Operation Risk Management", "Operation Unit", "Other Function", "Policy Team", "Risk Containment Unit", "Sales Unit", "Technical Team"]
L1_MANAGERS = ["Aditya Annamraju", "Alphanso Nagalapurkar", "AdAnthuvan Lourdusamy", "Dipesh Makawana", "Goutam Barman", "Jagruti Bane", "K Guruprasath", "Manmeet Singh", "Nishigandha Shinde", "Pramod Kumar", "Ramandeep Singh", "Rohit Shirwadkar", "Shilpy Dua", "Thiyagarajan Shanmugasundaram"]
L2_MANAGERS = ["AdAnthuvan Lourdusamy", "Ramandeep Singh", "Rohit Shirwadkar"]
INVESTIGATION_STATUS = ["Closed", "Pending"]
PENDING_STAGE = ["SCN Issuance In-progress", "Stage 1 - Awaiting complete case facts/information", "Stage 3 - Investigation Under Progress (L1)", "Stage 4 - Investigation Under Progress (L2)", "Stage 5 - Awaiting NH Review/Approval for IR/FMR"]
POLICE_STATUS = ["Filed", "Not Applicable", "Not Filed", "Pending"]
FMR_STATUS = ["FMR Not Applicable", "Filed", "Not Applicable", "Pending"]
HIGH_RISK_STATUS = ["NA", "Not Applicable", "Pending", "Pending with IT", "Yes"]
APPROVER_NAMES = ["Suhas", "Ajay Kanth"]
APPROVER_IDS = ["10001", "10002"]
APPROVER_ROLES = ["Lead-Investigation", "Head-FRMU"]
