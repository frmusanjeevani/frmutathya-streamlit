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
            font-weight: bold; text-transform: uppercase; font-size: 18px;
        }
        .stButton>button:hover { background-color: #8B151B; }
        .logo-link {
            position: absolute; top: 10px; font-size: 18px; font-weight: bold;
            color: #C7222A; text-decoration: none;
        }
        .top-left-logo { left: 10px; }
        .top-right-logo { right: 10px; }
        .user-role-box {
            position: absolute; top: 70px; right: 10px;
            background-color: #F5F5F5; padding: 4px 10px;
            font-size: 13px; color: #333; border-radius: 4px;
        }
        .footer {
            position: fixed; bottom: 5px; left: 10px;
            font-size: 13px; color: #888; font-style: italic;
        }
        h1, h2, h3, .title {
            font-family: 'Segoe UI'; color: #C7222A;
            font-weight: bold; font-size: 24px; text-transform: uppercase;
        }
     }
        .css-1d391kg .css-1v0mbdj {
            font-size: 18px !important;
            font-weight: bold !important;
            text-transform: uppercase;
        }
    </style>
    <a href="#Dashboard" class="logo-link top-left-logo">🔎 Tathya</a>
    <a href="https://www.adityabirlacapital.com/" target="_blank" class="logo-link top-right-logo">🏢 ABCL</a>
""", unsafe_allow_html=True)

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

menu = st.sidebar.selectbox("SELECT PAGE", MENU_OPTIONS)
if st.sidebar.button("🚪 LOGOUT"):
    st.session_state.authenticated = False
    st.session_state.clear()
    st.rerun()

st.title(f"Welcome {st.session_state.username}")

if menu == "Dashboard":
    st.subheader("📊 Case Level Dashboard")
    df = pd.read_sql("SELECT * FROM cases", conn)
    if df.empty:
        st.warning("No cases available.")
    else:
        st.dataframe(df.style.set_properties(**{
            'background-color': '#f9f9f9',
            'color': '#000',
            'border-color': '#C7222A',
            'border-width': '1px',
            'border-style': 'solid',
            'font-size': '14px'
        }))

elif menu == "Analytics":
    st.subheader("📈 Analytics")
    st.info("Coming soon...")

elif menu == "Case Entry" and st.session_state.role == "Initiator":
    st.subheader("📄 Enter New Case")

elif menu == "Reviewer Panel" and st.session_state.role == "Reviewer":
    st.subheader("📝 Reviewer Panel")

elif menu == "Approver Panel" and st.session_state.role == "Approver":
    st.subheader("✅ Approver Panel")

elif menu == "Legal - SCN":
    st.subheader("📄 Generate Show Cause Notice")

elif menu == "Legal - Orders":
    st.subheader("📘 Generate Reasoned Order")

elif menu == "Closure Actions":
    st.subheader("🔒 Action Closure Authority")

elif menu == "User Admin" and st.session_state.role == "Admin":
    st.subheader("👤 User Management")
