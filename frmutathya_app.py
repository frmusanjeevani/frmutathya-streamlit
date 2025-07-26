import streamlit as st

# Initialize default role if not already set
if "role" not in st.session_state:
    st.session_state.role = "Reviewer"  # You can change to "Admin", etc.

# Inject CSS for layout, login container, sidebar
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
            font-size: 18px;
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
    </style>
""", unsafe_allow_html=True)

# === LOGIN HANDLER ===
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

# === USER DICTIONARY ===
USERS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "initiator": {"password": "init123", "role": "Initiator"},
    "reviewer": {"password": "review123", "role": "Reviewer"},
    "approver": {"password": "approve123", "role": "Approver"},
    "legal": {"password": "legal123", "role": "Legal Reviewer"},
    "closure": {"password": "closure123", "role": "Action Closure Authority"}
}

# === AUTHENTICATION LOGIC ===
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    login()
    st.stop()

# === SIDEBAR NAVIGATION ===
st.sidebar.markdown("### 📁 Navigation")

role = st.session_state.get("role", "Reviewer")

base_menu = ["Dashboard", "Case Entry", "Analytics"]
if role == "Reviewer":
    base_menu.append("Reviewer Panel")
elif role == "Approver":
    base_menu.append("Approver Panel")
elif role == "Legal Reviewer":
    base_menu.extend(["Legal - SCN", "Legal - Orders"])
elif role == "Action Closure Authority":
    base_menu.append("Closure Actions")
elif role == "Admin":
    base_menu.append("User Admin")

# Store selected page
if "selected_page" not in st.session_state:
    st.session_state.selected_page = base_menu[0]

# Render buttons in custom style
for item in base_menu:
    if st.sidebar.button(item, key=item):
        st.session_state.selected_page = item

    active_class = "menu-box menu-active" if st.session_state.selected_page == item else "menu-box"
    st.sidebar.markdown(f'<div class="{active_class}">{item}</div>', unsafe_allow_html=True)

# LOGOUT BUTTON
if st.sidebar.button("🚪 Logout"):
    st.session_state.authenticated = False
    st.session_state.clear()
    st.rerun()

# === MAIN CONTENT ===
st.markdown(f"### You selected: {st.session_state.selected_page}")

if st.session_state.selected_page == "Dashboard":
    st.success("📊 Dashboard placeholder")

elif st.session_state.selected_page == "Case Entry":
    st.info("📝 Case Entry form placeholder")

elif st.session_state.selected_page == "Analytics":
    st.warning("📈 Analytics coming soon...")

elif st.session_state.selected_page == "Reviewer Panel":
    st.info("🧑‍💼 Reviewer Panel goes here...")

elif st.session_state.selected_page == "Approver Panel":
    st.info("✅ Approver Panel goes here...")

elif st.session_state.selected_page == "Legal - SCN":
    st.subheader("📄 Generate Show Cause Notice")
    # Your SCN logic here...

elif st.session_state.selected_page == "Legal - Orders":
    st.subheader("📘 Generate Reasoned Order")
    # Your Reasoned Order logic here...

elif st.session_state.selected_page == "Closure Actions":
    st.subheader("🔒 Action Closure Authority Panel")
    # Your Closure form logic here...

elif st.session_state.selected_page == "User Admin":
    st.subheader("👤 Admin User Management")
    # Admin features...
