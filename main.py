import streamlit as st
from frontend.role_selector import show_role_selector
from frontend.auth import show_auth_page
from frontend.admin_login import show_admin_login
from frontend.upload import show_upload_page
from frontend.history import show_history_page
from frontend.search import show_search_page
from frontend.admin_dashboard import show_admin_dashboard 
from frontend.admin_user import show_admin_users
from frontend.admin_books import show_admin_books
from frontend.user_dashboard import show_user_dashboard 

st.set_page_config(page_title="AI Book Summarizer", layout="wide", page_icon="📚")

# ---------- GLOBAL APP STYLING ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif !important; }

/* MODERN DARK THEME BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 50%, #16213e 100%);
    min-height: 100vh;
}

/* HIDE DEFAULT SCROLL BAR */
::-webkit-scrollbar { width: 10px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.05); }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 5px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.3); }

/* IMPROVED HEADERS */
h1, h2, h3, h4, h5, h6 {
    background: linear-gradient(135deg, #00d4ff 0%, #7c3aed 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ENHANCED BUTTONS */
div.stButton > button {
    background: linear-gradient(135deg, #00d4ff 0%, #7c3aed 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    height: 50px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 8px 24px rgba(0, 212, 255, 0.3) !important;
}

div.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 32px rgba(0, 212, 255, 0.5) !important;
}

div.stButton > button:active {
    transform: translateY(-1px) !important;
}

/* ENHANCED INPUTS */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > select {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 1.5px solid rgba(0, 212, 255, 0.3) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    padding: 12px 16px !important;
    font-size: 14px !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div > select:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.2) !important;
    background: rgba(255, 255, 255, 0.12) !important;
}

/* FILE UPLOADER */
.stFileUploader {
    border: 2px dashed rgba(0, 212, 255, 0.4) !important;
    border-radius: 16px !important;
    padding: 20px !important;
    background: rgba(0, 212, 255, 0.05) !important;
    transition: all 0.3s ease !important;
}

/* SIDEBAR STYLING */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, rgba(15,15,30,0.9) 0%, rgba(26,26,46,0.9) 100%);
    border-right: 1px solid rgba(0, 212, 255, 0.2);
}

/* METRIC CARDS */
[data-testid="metric-container"] {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 1px solid rgba(0, 212, 255, 0.3) !important;
    border-radius: 16px !important;
    padding: 20px !important;
}

/* EXPANDER STYLING */
.streamlit-expanderHeader {
    background: rgba(0, 212, 255, 0.1) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}

/* DIVIDER */
hr { border-color: rgba(0, 212, 255, 0.2); }

/* STATUS MESSAGES */
.stSuccess { background-color: rgba(0, 212, 100, 0.15) !important; border: 1px solid rgba(0, 212, 100, 0.4) !important; }
.stError { background-color: rgba(255, 100, 100, 0.15) !important; border: 1px solid rgba(255, 100, 100, 0.4) !important; }
.stWarning { background-color: rgba(255, 200, 0, 0.15) !important; border: 1px solid rgba(255, 200, 0, 0.4) !important; }
.stInfo { background-color: rgba(0, 170, 255, 0.15) !important; border: 1px solid rgba(0, 170, 255, 0.4) !important; }

/* RESPONSIVE */
@media (max-width: 768px) {
    .stApp { padding: 0; }
    .element-container { padding: 0.5rem; }
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION DEFAULTS ----------
if "role" not in st.session_state:
    st.session_state.role = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False 

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ---------- ROLE SELECTION ----------
if not st.session_state.role:
    show_role_selector()
    st.stop()

# ---------- USER FLOW ----------
if st.session_state.role == "user":

    if not st.session_state.logged_in:
        show_auth_page()
        st.stop()

    st.sidebar.title("👤 User Panel")

    page = st.sidebar.radio(
        "Navigation",
        [ "Dashboard" ,"Upload", "Search", "History", "Logout"]
    )
    if page == "Dashboard":
        show_user_dashboard(st.session_state.user_id)


    elif page == "Upload": 
      show_upload_page(st.session_state.user_id)

    elif page == "Search":
        show_search_page(st.session_state.user_id)

    elif page == "History":
        show_history_page(st.session_state.user_id)

    elif page == "Logout":
        st.session_state.clear()
        st.rerun()

# ---------- ADMIN FLOW ----------
elif st.session_state.role == "admin":

    if not st.session_state.admin_logged_in:
        show_admin_login()
        st.stop()

    st.sidebar.title("🛠 Admin Panel")

    admin_page = st.sidebar.radio(
        "Admin Navigation",
        ["Dashboard", "Users", "Books", "Logout"]
    )

    if admin_page == "Dashboard":
        show_admin_dashboard()

    elif admin_page == "Users":
        show_admin_users()

    elif admin_page == "Books":
        show_admin_books()

    elif admin_page == "Logout":
        st.session_state.clear()
        st.rerun()
st.sidebar.markdown("---")

if st.sidebar.button("🔁 Switch Role"):
    st.session_state.role = None
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.rerun() 