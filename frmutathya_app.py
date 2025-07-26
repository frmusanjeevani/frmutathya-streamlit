import streamlit as st
import uuid
import os
import json
from datetime import datetime

# === USER DATABASE ===
USERS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "initiator": {"password": "init123", "role": "Initiator"},
    "reviewer": {"password": "review123", "role": "Reviewer"},
    "approver": {"password": "approve123", "role": "Approver"},
    "legal": {"password": "legal123", "role": "Legal Reviewer"},
    "closure": {"password": "closure123", "role": "Action Closure Authority"}
}

# === PAGE CONFIG & STYLING ===
st.set_page_config(layout="wide")
st.markdown("""
    <style>
        .login-container {
            max-width: 300px;
            margin: 15vh auto 0 auto;
            background-color: #fff5e1;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
        }
        .menu-box {
            background-color: #f4f4f4;
            padding: 8px 14px;
            margin-bottom: 6px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 16px;
            text-transform: uppercase;
            transition: 0.2s ease;
            cursor: pointer;
        }
        .menu-box:hover {
            background-color: #e0e0e0;
        }
        .menu-active {
            background-color: #d0d0ce !important;
        }
        .logo-link {
            position: absolute;
            top: 8px;
            font-size: 16px;
            font-weight: bold;
            color: #C7222A;
            text-decoration: none;
            z-index: 999;
        }
        .top-left-logo { left: 10px; }
        .top-right-logo { right: 10px; }
    </style>
    <a href="#Dashboard" class="logo-link top-left-logo">🔎 Tathya</a>
    <a href="https://www.adityabirlacapital.com/" target="_blank" class="logo-link top-right-logo">🏢 ABCL</a>
""", unsafe_allow_html=True)

# === SESSION & LOGIN ===
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login():
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

if not st.session_state.authenticated:
    login()
    st.stop()

# === SIDEBAR MENU ===
role = st.session_state.get("role", "Reviewer")
base_menu = ["Dashboard", "Case Entry", "Analytics"]

if role == "Reviewer":
    base_menu.append("Reviewer Panel")
elif role == "Approver":
    base_menu.append("Approver Panel")
elif role == "Legal Reviewer":
    base_menu.append("Legal - SCN / Orders")
elif role == "Action Closure Authority":
    base_menu.append("Closure Actions")
elif role == "Admin":
    base_menu.append("User Admin")

if "selected_page" not in st.session_state:
    st.session_state.selected_page = base_menu[0]

st.sidebar.markdown("### 📁 Navigation")
for item in base_menu:
    if st.sidebar.button(item, key=item):
        st.session_state.selected_page = item
    active_class = "menu-box menu-active" if st.session_state.selected_page == item else "menu-box"
    st.sidebar.markdown(f'<div class="{active_class}">{item}</div>', unsafe_allow_html=True)

if st.sidebar.button("🚪 Logout"):
    st.session_state.authenticated = False
    st.session_state.clear()
    st.rerun()

# === MAIN CONTENT ===
st.markdown(f"###: {st.session_state.selected_page}")

if st.session_state.selected_page == "Dashboard":
    st.success("📊 Dashboard placeholder")

elif st.session_state.selected_page == "Case Entry":
if st.session_state.selected_page == "Dashboard":
    st.subheader("📊 All Submitted Cases")

    folder_path = "data/cases"
    if not os.path.exists(folder_path):
        st.info("No cases submitted yet.")
    else:
        case_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]
        all_cases = []

        for file in case_files:
            file_path = os.path.join(folder_path, file)
            with open(file_path, "r") as f:
                case_data = json.load(f)
                all_cases.append(case_data)

        if all_cases:
            import pandas as pd
            df = pd.DataFrame(all_cases)
            df = df.sort_values("submitted_at", ascending=False)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No data available yet.")

    case_id = st.text_input("Case ID")
    lan = st.text_input("LAN")
    case_type = st.selectbox("Type of Case", ["Lending", "Non Lending"])

    product = st.selectbox("Product", [
        "BL", "BTC PL", "DL", "Drop Line LOC", "Finagg", "INSTI - MORTGAGES", "LAP",
        "Line of Credit", "MLAP", "NA", "PL", "SEG", "SME", "STSL", "STSLP BT + Top - up",
        "STUL", "Term Loan", "Term Loan Infra", "Udyog Plus", "Unsecured BuyOut"
    ])

    region = st.selectbox("Region", ["East", "North", "South", "West"])

    referred_by = st.selectbox("Referred By", [
        "Audit Team", "Business Unit", "Collection Unit", "Compliance Team", "Credit Unit",
        "Customer Service", "GRT", "HR", "Legal Unit", "MD / CEO Escalation",
        "Operation Risk Management", "Operation Unit", "Other Function", "Policy Team",
        "Risk Containment Unit", "Sales Unit", "Technical Team"
    ])

    case_description = st.text_area("Case Description")
    case_date = st.date_input("Case Date", datetime.today())
    st.file_uploader("Attach Supporting Document")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Draft"):
            st.success("✅ Draft saved temporarily (implement logic to save if needed)")

    with col2:
        if st.button("📤 Submit Final"):
            if not case_id.strip() or not lan.strip() or not case_description.strip():
                st.warning("Please fill required fields before submitting.")
            else:
                case_data = {
                    "case_id": case_id,
                    "lan": lan,
                    "case_type": case_type,
                    "product": product,
                    "region": region,
                    "referred_by": referred_by,
                    "case_description": case_description,
                    "case_date": case_date.strftime("%Y-%m-%d"),
                    "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                folder_path = "data/cases"
                os.makedirs(folder_path, exist_ok=True)

                file_path = os.path.join(folder_path, f"{case_id}.json")
                with open(file_path, "w") as f:
                    json.dump(case_data, f, indent=4)

                st.success(f"✅ Case saved to internal path as {case_id}.json")
