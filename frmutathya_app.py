import streamlit as st
import pandas as pd
from datetime import datetime
import sqlite3
import os

st.set_page_config(page_title="Tathya - Case Management", page_icon="🔎", layout="centered")

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
        .login-container { max-width: 400px; margin: auto; background-color: #fff5e1; padding: 2rem; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
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
    st.markdown("<h1 class='title' style='text-align: center;'>Every Clue Counts</h1>", unsafe_allow_html=True)
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
