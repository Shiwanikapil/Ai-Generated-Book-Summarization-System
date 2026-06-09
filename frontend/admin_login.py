import os

import streamlit as st
from dotenv import load_dotenv


load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


def show_admin_login():
    st.set_page_config(page_title="Admin Login", layout="centered")

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            min-height: 100vh;
            overflow: hidden;
            color: #ffffff;
            background:
                radial-gradient(circle at 18% 22%, rgba(255, 255, 255, 0.72) 0 1px, transparent 1.4px),
                radial-gradient(circle at 72% 18%, rgba(255, 255, 255, 0.52) 0 1px, transparent 1.4px),
                radial-gradient(circle at 38% 74%, rgba(255, 255, 255, 0.48) 0 1px, transparent 1.3px),
                radial-gradient(circle at 88% 68%, rgba(255, 255, 255, 0.44) 0 1px, transparent 1.4px),
                radial-gradient(circle at 55% 42%, rgba(31, 150, 190, 0.28), transparent 24rem),
                linear-gradient(180deg, #061528 0%, #063250 54%, #075979 100%);
            background-size:
                120px 120px,
                170px 170px,
                210px 210px,
                260px 260px,
                auto,
                auto;
        }

        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background:
                radial-gradient(circle at 10% 92%, #020816 0 42px, transparent 43px),
                radial-gradient(circle at 78% 99%, rgba(4, 12, 18, 0.92) 0 34px, transparent 35px),
                radial-gradient(circle at 85% 96%, rgba(4, 12, 18, 0.90) 0 18px, transparent 19px),
                linear-gradient(180deg, transparent 0 78%, rgba(3, 13, 22, 0.30) 100%);
        }

        header, footer, [data-testid="stHeader"], [data-testid="stToolbar"] {
            display: none !important;
        }

        .block-container {
            width: min(430px, calc(100vw - 32px)) !important;
            max-width: 430px !important;
            margin: 14vh auto 0 !important;
            padding: 34px 30px 28px !important;
            border-radius: 7px;
            background: rgba(2, 23, 42, 0.36);
            border: 1px solid rgba(255, 255, 255, 0.18);
            box-shadow:
                0 24px 70px rgba(0, 0, 0, 0.30),
                inset 0 0 30px rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }

        .login-title {
            margin: 0 0 26px;
            color: #ffffff;
            text-align: center;
            font-size: 30px;
            font-weight: 800;
            line-height: 1;
            text-shadow: 0 2px 12px rgba(0, 0, 0, 0.34);
        }

        .stTextInput {
            margin-bottom: 18px !important;
        }

        .stTextInput label {
            display: none !important;
        }

        .stTextInput > div > div {
            border-radius: 999px !important;
            background: rgba(3, 39, 68, 0.46) !important;
            border: 1px solid rgba(255, 255, 255, 0.28) !important;
            box-shadow: inset 0 0 16px rgba(255, 255, 255, 0.03) !important;
        }

        .stTextInput input {
            height: 45px !important;
            color: #ffffff !important;
            background: transparent !important;
            border: 0 !important;
            border-radius: 999px !important;
            padding: 0 18px !important;
            font-size: 14px !important;
            font-weight: 600 !important;
        }

        .stTextInput input::placeholder {
            color: rgba(255, 255, 255, 0.86) !important;
            opacity: 1 !important;
        }

        .stTextInput input:focus {
            box-shadow: none !important;
        }

        .helper-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: -4px 0 14px;
            color: #ffffff;
            font-size: 13px;
            font-weight: 600;
        }

        .remember {
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .check-box {
            width: 10px;
            height: 10px;
            border-radius: 2px;
            background: #ffffff;
            box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.45);
        }

        .forgot {
            color: #ffffff;
            text-decoration: none;
        }

        div.stButton > button {
            width: 100%;
            min-height: 45px;
            border: none !important;
            border-radius: 999px !important;
            background: #ffffff !important;
            color: #1c2430 !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.18) !important;
            transition: transform 160ms ease, box-shadow 160ms ease !important;
        }

        div.stButton > button:hover {
            transform: translateY(-2px);
            color: #111827 !important;
            box-shadow: 0 16px 34px rgba(0, 0, 0, 0.24) !important;
        }

        .register-text {
            margin-top: 16px;
            color: #ffffff;
            text-align: center;
            font-size: 13px;
            font-weight: 600;
        }

        .register-text span {
            font-weight: 800;
        }

        div[data-testid="stAlert"] {
            margin-top: 14px;
            border-radius: 10px !important;
            border: 1px solid rgba(255, 255, 255, 0.18) !important;
            background: rgba(2, 23, 42, 0.56) !important;
            color: #ffffff !important;
        }

        @media (max-width: 520px) {
            .block-container {
                margin-top: 11vh !important;
                padding: 30px 22px 24px !important;
            }

            .login-title {
                font-size: 27px;
            }

            .helper-row {
                font-size: 12px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<h1 class="login-title">Login</h1>', unsafe_allow_html=True)

    username = st.text_input("", placeholder="Username")
    password = st.text_input("", type="password", placeholder="Password")

    st.markdown(
        """
        <div class="helper-row">
            <div class="remember"><span class="check-box"></span><span>Remember Me</span></div>
            <a class="forgot" href="#" onclick="return false;">Forget Password?</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Login"):
        if username and password:
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                st.session_state["admin_logged_in"] = True
                st.success("Login successful! Redirecting to dashboard...")
                st.rerun()
            else:
                st.error("Invalid admin credentials")
        else:
            st.error("Please enter both username and password")

    st.markdown(
        '<div class="register-text">Don\'t have an account?<span>Register</span></div>',
        unsafe_allow_html=True,
    )


show_admin_login()
