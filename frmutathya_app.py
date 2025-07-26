import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Tathya - Case Management", page_icon="🔎", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
        body { background-color: #FFF4D9; }
        .title { font-size: 42px; font-weight: bold; color: #C7222A; }
        .subtitle { font-size: 18px; color: #231F20; }
        .stButton>button {
            background-color: #C7222A;
            color: white;
            border: none;
            padding: 0.4rem 1rem;
            font-weight: 600;
        }
        .stButton>button:hover { background-color: #8B151B; }
    </style>
""", unsafe_allow_html=True)

# --- Login Gate ---
def login():
    st.markdown('<p class="title">🔐 Login to Tathya</p>', unsafe_allow_html=True)
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("🔓 Login")

        if login_btn:
            if username == "admin" and password == "abcl123":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    login()
    st.stop()

# --- Sidebar Menu ---
menu = st.sidebar.radio("📁 Navigate", ["Home", "Case Entry", "Case Tracker", "Approver Panel", "About Tathya"])
st.sidebar.button("🔒 Logout", on_click=lambda: st.session_state.update({"authenticated": False}))

# --- App Content ---
st.markdown('<p class="title">🔎 Tathya</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Uncover the truth, one case at a time — ABCL Internal Platform</p>', unsafe_allow_html=True)
st.markdown("---")

if "cases" not in st.session_state:
    st.session_state.cases = []

if menu == "Home":
    st.markdown("""
        <div style='background-color: #FFF4D9; padding: 2rem 2rem; border-radius: 12px; border-left: 6px solid #C7222A;'>
            <h1 style='color: #C7222A; font-size: 48px; margin-bottom: 10px;'>🔎 Welcome to Tathya</h1>
            <p style='color: #231F20; font-size: 20px;'>
                <em>"Uncover the truth, one case at a time."</em><br>
                A secure internal platform for managing investigation cases across ABCL regions and products.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="padding: 1rem; border: 1px solid #D0D0CE; border-radius: 10px; background-color: #FFFFFF; text-align: center;">
            <h3 style="color:#C7222A;">📝 Case Entry</h3>
            <p>Enter and assign cases with details including region, type, and reviewer.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="padding: 1rem; border: 1px solid #D0D0CE; border-radius: 10px; background-color: #FFFFFF; text-align: center;">
            <h3 style="color:#C7222A;">📊 Case Tracker</h3>
            <p>Track submitted cases by reviewer and status across hubs.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="padding: 1rem; border: 1px solid #D0D0CE; border-radius: 10px; background-color: #FFFFFF; text-align: center;">
            <h3 style="color:#C7222A;">🔐 Approver Panel</h3>
            <p>Leads can approve, reject, or seek clarifications with full comments.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <br>
        <h4 style='color: #231F20;'>👉 Use the left panel to access different Tathya modules.</h4>
        <br><hr>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <p style="text-align: center; font-size: 14px; color: #77787B;">
            Powered by <strong>ABCL Risk & Automation</strong> | Built using <a href="https://streamlit.io" target="_blank">Streamlit</a>
        </p>
    """)

elif menu == "Case Entry":
    st.subheader("📄 Enter New Case")
    with st.form("case_form"):
        col1, col2 = st.columns(2)
        with col1:
            case_id = st.text_input("Case ID")
            customer_name = st.text_input("Customer Name")
            date = st.date_input("Case Date", datetime.today())
        with col2:
            case_type = st.selectbox("Case Type", ["Fraud", "Negative", "Manual Review"])
            assigned_reviewer = st.selectbox("Assign Reviewer", ["Ravi", "Meena", "Ajay"])
            region = st.selectbox("Region", ["East", "West", "North", "South"])

        submitted = st.form_submit_button("🚀 Submit Case")

        if submitted:
            if case_id and customer_name:
                new_case = {
                    "Case ID": case_id,
                    "Customer": customer_name,
                    "Date": date.strftime("%Y-%m-%d"),
                    "Type": case_type,
                    "Region": region,
                    "Reviewer": assigned_reviewer,
                    "Status": "Pending"
                }
                st.session_state.cases.append(new_case)
                st.success(f"✅ Case '{case_id}' submitted successfully.")
            else:
                st.error("⚠️ Please fill all required fields.")

elif menu == "Case Tracker":
    st.subheader("📊 Track Submitted Cases")
    filter_reviewer = st.selectbox("Filter by Reviewer", ["All", "Ravi", "Meena", "Ajay"])
    filtered = st.session_state.cases

    if filter_reviewer != "All":
        filtered = [c for c in filtered if c["Reviewer"] == filter_reviewer]

    if filtered:
        st.dataframe(pd.DataFrame(filtered))
    else:
        st.info("No cases available for this reviewer.")

elif menu == "Approver Panel":
    st.subheader("🔐 Lead Approver Panel")
    st.warning("Restricted: This section is only for investigation leads.")

    if st.session_state.cases:
        selected_case = st.selectbox("Select Case to Review", [c["Case ID"] for c in st.session_state.cases])
        status = st.selectbox("Mark Final Status", ["Approved", "Rejected", "Needs Clarification"])
        feedback = st.text_area("Approver Feedback")

        if st.button("✅ Submit Review"):
            st.success(f"Review for Case `{selected_case}` submitted with status '{status}'.")
    else:
        st.info("No cases submitted yet.")

elif menu == "About Tathya":
    st.subheader("📘 About Tathya")
    st.markdown("""
        **Tathya** is a secure case management and approval system designed for ABCL's internal use.

        #### 🔍 Key Objectives:
        - Manage fraud/negative/manual review cases
        - Assign reviewers across regions
        - Track end-to-end status
        - Enable reviewer and approver flows
        - Ensure accuracy and transparency

        #### 🛠️ Built With:
        - Python + Streamlit
        - ABCL branding & security compliance
        - Deployable on EC2/AWS infrastructure

        💼 **Maintained by**: FRMU Automation Team
    """)
