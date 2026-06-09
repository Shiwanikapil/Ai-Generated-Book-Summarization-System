import streamlit as st
from utils.database import create_user, get_user_by_email, verify_user


def inject_auth_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', sans-serif !important;
    }

    .stApp::before,
    .stApp::after {
        display: none !important;
    }

    header, footer, [data-testid="stHeader"], [data-testid="stToolbar"] {
        display: none !important;
    }

    .block-container {
        position: relative;
        z-index: 2;
        width: min(430px, calc(100vw - 32px)) !important;
        max-width: 430px !important;
        margin: 12vh auto 0 !important;
        padding: 42px 34px 34px !important;
        border-radius: 22px !important;
        background: rgba(255, 255, 255, 0.075) !important;
        border: 1px solid rgba(255, 255, 255, 0.16) !important;
        box-shadow:
            0 24px 70px rgba(0, 0, 0, 0.28),
            inset 0 1px 0 rgba(255, 255, 255, 0.12) !important;
        backdrop-filter: blur(22px) saturate(150%) !important;
        -webkit-backdrop-filter: blur(22px) saturate(150%) !important;
        animation: cardIn .7s ease both, softFloat 5.5s ease-in-out infinite .8s;
    }

    @keyframes cardIn {
        from {
            opacity: 0;
            transform: translateY(26px) scale(.97);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    @keyframes softFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-6px); }
    }

    .auth-title {
        text-align: center;
        color: #ffffff;
        font-size: 31px;
        font-weight: 800;
        margin-bottom: 30px;
        letter-spacing: 0;
        animation: fadeDown .65s ease both .1s;
    }

    .auth-title small {
        display: block;
        margin-bottom: 8px;
        color: rgba(180, 235, 255, 0.85);
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
    }

    .stTextInput {
        margin-bottom: 20px !important;
        animation: fadeUp .65s ease both .18s;
    }

    .stTextInput label {
        display: none !important;
    }

    .stTextInput input {
        height: 54px !important;
        border-radius: 14px !important;
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(0, 212, 255, 0.28) !important;
        color: #ffffff !important;
        padding: 0 17px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        transition: all .25s ease !important;
        box-shadow: inset 0 0 18px rgba(255, 255, 255, 0.03) !important;
    }

    .stTextInput input::placeholder {
        color: rgba(235, 245, 255, 0.62) !important;
    }

    .stTextInput input:focus {
        background: rgba(255, 255, 255, 0.13) !important;
        border-color: rgba(0, 212, 255, 0.75) !important;
        box-shadow:
            0 0 0 3px rgba(0, 212, 255, 0.14),
            0 0 30px rgba(0, 212, 255, 0.13) !important;
        transform: translateY(-2px);
    }

    .stCheckbox,
    .forgot-link {
        animation: fadeUp .65s ease both .26s;
    }

    .stCheckbox label,
    .stCheckbox p {
        color: rgba(245, 250, 255, 0.86) !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }

    .forgot-link {
        text-align: right;
        color: rgba(180, 235, 255, 0.88);
        font-size: 13px;
        font-weight: 700;
        margin-top: 2px;
    }

    div.stButton {
        animation: fadeUp .65s ease both .34s;
    }

    div.stButton > button {
        width: 100% !important;
        height: 54px !important;
        border-radius: 14px !important;
        border: none !important;
        background: linear-gradient(135deg, #00d4ff 0%, #7c3aed 100%) !important;
        color: white !important;
        font-size: 15px !important;
        font-weight: 800 !important;
        box-shadow: 0 16px 34px rgba(0, 212, 255, 0.20) !important;
        transition: all .25s ease !important;
    }

    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.01) !important;
        box-shadow: 0 20px 44px rgba(0, 212, 255, 0.34) !important;
    }

    .auth-footer-text {
        text-align: center;
        color: rgba(245, 250, 255, 0.78);
        font-size: 13px;
        font-weight: 600;
        margin-top: 15px;
        animation: fadeUp .65s ease both .42s;
    }

    .auth-footer-link {
        color: #00d4ff;
        font-weight: 800;
    }

    .auth-message {
        padding: 12px;
        margin: 14px 0;
        border-radius: 12px;
        text-align: center;
        color: white;
        font-weight: 700;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.16);
        animation: fadeUp .35s ease both;
    }

    .auth-error {
        border-color: rgba(255, 120, 120, .55);
        background: rgba(239, 68, 68, 0.12);
    }

    .auth-success {
        border-color: rgba(120, 255, 180, .55);
        background: rgba(34, 197, 94, 0.12);
    }

    .auth-warning {
        border-color: rgba(255, 210, 120, .55);
        background: rgba(245, 158, 11, 0.12);
    }

    @keyframes fadeDown {
        from {
            opacity: 0;
            transform: translateY(-14px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeUp {
        from {
            opacity: 0;
            transform: translateY(16px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @media (max-width: 520px) {
        .block-container {
            margin-top: 7vh !important;
            padding: 34px 24px 28px !important;
        }

        .auth-title {
            font-size: 27px;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def show_auth_page():
    inject_auth_css()

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    if st.session_state.auth_mode == "login":
        show_login()
    else:
        show_signup()


def show_login():
    st.markdown(
        '<div class="auth-title"><small>Reader Account</small>Welcome Back</div>',
        unsafe_allow_html=True
    )

    email = st.text_input("Email Address", placeholder="Email Id", label_visibility="collapsed")
    password = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")

    col1, col2 = st.columns([1, 1])
    with col1:
        remember = st.checkbox("Remember me")
    with col2:
        st.markdown('<div class="forgot-link">Forgot Password?</div>', unsafe_allow_html=True)

    if st.button("Sign in", use_container_width=True):
        if not email or not password:
            st.markdown('<div class="auth-message auth-error">Please fill in all fields</div>', unsafe_allow_html=True)
        else:
            user = verify_user(email, password)
            if not user:
                st.markdown('<div class="auth-message auth-error">Invalid credentials</div>', unsafe_allow_html=True)
            else:
                st.session_state.logged_in = True
                st.session_state.user_id = str(user["_id"])
                st.session_state.user_name = user["name"]
                st.markdown('<div class="auth-message auth-success">Login successful!</div>', unsafe_allow_html=True)
                st.balloons()
                st.rerun()

    st.markdown(
        '<div class="auth-footer-text">Don\'t have an account? <span class="auth-footer-link">Register</span></div>',
        unsafe_allow_html=True
    )

    if st.button("Create new account", use_container_width=True, key="to_signup"):
        st.session_state.auth_mode = "signup"
        st.rerun()


def show_signup():
    st.markdown(
        '<div class="auth-title"><small>Reader Account</small>Create Account</div>',
        unsafe_allow_html=True
    )

    name = st.text_input("Full Name", placeholder="Full name", label_visibility="collapsed")
    email = st.text_input("Email Address", placeholder="Email Id", label_visibility="collapsed", key="signup_email")
    password = st.text_input("Password", type="password", placeholder="Create password", label_visibility="collapsed", key="signup_pass")
    password_confirm = st.text_input("Confirm Password", type="password", placeholder="Repeat password", label_visibility="collapsed")

    if st.button("Create Account", use_container_width=True):
        if not name or not email or not password or not password_confirm:
            st.markdown('<div class="auth-message auth-error">Please fill in all fields</div>', unsafe_allow_html=True)
        elif password != password_confirm:
            st.markdown('<div class="auth-message auth-error">Passwords do not match</div>', unsafe_allow_html=True)
        elif len(password) < 6:
            st.markdown('<div class="auth-message auth-warning">Password must be at least 6 characters</div>', unsafe_allow_html=True)
        elif get_user_by_email(email):
            st.markdown('<div class="auth-message auth-warning">Email already registered</div>', unsafe_allow_html=True)
        else:
            create_user(name, email, password)
            st.markdown('<div class="auth-message auth-success">Account created successfully!</div>', unsafe_allow_html=True)
            st.balloons()
            st.session_state.auth_mode = "login"
            st.rerun()

    st.markdown(
        '<div class="auth-footer-text">Already have an account? <span class="auth-footer-link">Sign In</span></div>',
        unsafe_allow_html=True
    )

    if st.button("Back to Login", use_container_width=True, key="to_login"):
        st.session_state.auth_mode = "login"
        st.rerun()
