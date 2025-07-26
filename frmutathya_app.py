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
    st.subheader("📄 Enter New Case")
    
     case_id = str(uuid.uuid4())
    st.text_input("Generated Case ID", value=case_id, disabled=True)

lan = st.text_input("LAN")
case_type = st.selectbox("Type of Case", ["Lending", "Non Lending"])
    
    # 🔽 New Field: Product
    st.selectbox("Product", [
        "BL", "BTC PL", "DL", "Drop Line LOC", "Finagg", "INSTI - MORTGAGES", "LAP",
        "Line of Credit", "MLAP", "NA", "PL", "SEG", "SME", "STSL", "STSLP BT + Top - up",
        "STUL", "Term Loan", "Term Loan Infra", "Udyog Plus", "Unsecured BuyOut"
    ])
    
    st.selectbox("Region", ["East", "North", "South", "West"])
    
    # 🔽 New Field: Referred By
    st.selectbox("Referred By", [
        "Audit Team", "Business Unit", "Collection Unit", "Compliance Team", "Credit Unit",
        "Customer Service", "GRT", "HR", "Legal Unit", "MD / CEO Escalation",
        "Operation Risk Management", "Operation Unit", "Other Function", "Policy Team",
        "Risk Containment Unit", "Sales Unit", "Technical Team"
    ])
    
    st.text_area("Case Description")
    st.date_input("Case Date", datetime.today())
    st.file_uploader("Attach Supporting Document")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Draft"):
            st.success("✅ Draft saved temporarily (implement logic to save if needed)")
    
    with col2:
        if st.button("📤 Submit Final"):
            if not case_id or not case_description:
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

folder_path = "data/cases"
os.makedirs(folder_path, exist_ok=True) 

file_path = os.path.join(folder_path, f"{case_data['case_id']}.json")
with open(file_path, "w") as f:
    json.dump(case_data, f, indent=4)

st.success(f"✅ Case saved to internal path as {case_data['case_id']}.json")

elif st.session_state.selected_page == "Reviewer Panel":
    st.subheader("📝 Reviewer Panel")

elif st.session_state.selected_page == "Approver Panel":
    st.subheader("✅ Approver Panel")

elif st.session_state.selected_page == "Legal - SCN / Orders":
    st.title("📄 Generate Show Cause Notice / Reasoned Order")
    doc_type = st.selectbox("Select Document Type", ["Show Cause Notice", "Reasoned Order"])

    case_id = st.text_input("Case ID / Incident Name")
    recipient = st.text_input("Recipient Name and Designation")
    date_of_issue = st.date_input("Date of Issue", value=datetime.today())
    ref_no = st.text_input("Notice / Order Number")

    if doc_type == "Show Cause Notice":
        allegation = st.text_area("Summary of Allegation")
        evidence = st.text_area("Evidence Summary")
        legal_ref = st.text_area("Legal Reference (if any)")
        response_timeline = st.text_input("Response Deadline (e.g., 7 days)")
        contact_details = st.text_area("Contact for Clarification")

        if st.button("Generate Show Cause Notice"):
            st.markdown(f"""
            ### 🛑 Show Cause Notice – {case_id}
            **To:** {recipient}  
            **Date:** {date_of_issue.strftime('%d-%m-%Y')}  
            **Notice No.:** {ref_no}

            **1. Summary of Allegation:**  
            {allegation}

            **2. Evidence Summary:**  
            {evidence}

            **3. Legal / Policy Reference:**  
            {legal_ref}

            **4. Required Response Timeline:**  
            You are required to respond within **{response_timeline}** from the date of issuance.

            **5. Consequences of Non-Response:**  
            Failure to respond within the given timeframe may result in appropriate disciplinary action.

            **6. Contact Details for Clarification:**  
            {contact_details}

            **Issued by:**  
            [Your Name]  
            [Your Designation]  
            Powered by FRMU Sanjeevani
            """)

    elif doc_type == "Reasoned Order":
        response_status = st.selectbox("Response Received?", ["Yes", "No"])
        summary_of_findings = st.text_area("Findings and Evidence Summary")
        if response_status == "Yes":
            response_summary = st.text_area("Summary of Respondent’s Reply")
        else:
            response_summary = "No response was received from the respondent."

        conclusion = st.text_area("Final Decision")
        action_taken = st.text_area("Action Taken or Recommended")
        appeal_rights = st.text_area("Right to Appeal (if any)")

        if st.button("Generate Reasoned Order"):
            st.markdown(f"""
            ### 📘 Reasoned Order – {case_id}
            **To:** {recipient}  
            **Date:** {date_of_issue.strftime('%d-%m-%Y')}  
            **Order No.:** {ref_no}

            **1. Background:**  
            A Show Cause Notice was issued earlier regarding the above-mentioned matter.

            **2. Summary of Charges:**  
            Referenced under Notice No. {ref_no}.

            **3. Examination of Evidence:**  
            {summary_of_findings}

            **4. Respondent’s Reply:**  
            {response_summary}

            **5. Final Decision:**  
            {conclusion}

            **6. Action Taken:**  
            {action_taken}

            **7. Right to Appeal:**  
            {appeal_rights}

            **Issued by:**  
            [Your Name]  
            [Your Designation]  
            Powered by FRMU Sanjeevani
            """)

elif st.session_state.selected_page == "Closure Actions":
    st.subheader("🔒 Action Closure Authority Panel")
    with st.form("closure_form"):
        st.text_input("Actioner Name")
        st.selectbox("Department Responsible", ["Business Ops", "Legal", "HR", "IT", "Collections"])
        st.selectbox("Action Type", [
            "Clawback", "Recovery", "Police Complaint", "DSA Blacklisting", 
            "Credit Bureau Suppression", "Partner Notification", 
            "IT Tagging", "FMR Reporting"
        ])
        st.text_area("Action Description")
        st.selectbox("Action Status", ["Completed", "In Progress", "Not Started", "Escalated"])
        st.date_input("Action Start Date")
        st.date_input("Completion Date")
        st.file_uploader("Supporting Document(s)")
        st.text_area("Remarks / Justification")
        if st.selectbox("Escalation Required?", ["No", "Yes"]) == "Yes":
            st.text_input("Escalated To")
        st.selectbox("Verification Status", ["Verified", "Pending Verification"])
        st.text_input("Verified By")
        st.date_input("Verification Date")
        st.selectbox("Notification Sent?", ["Yes", "No"])
        st.selectbox("Final Case Status", ["Closed", "Reopened", "Under Review"])

        if st.form_submit_button("Submit"):
            st.success("Action closure submitted successfully.")

elif st.session_state.selected_page == "User Admin":
    st.subheader("👤 Admin Panel")
    st.info("User management functionality coming soon...")
