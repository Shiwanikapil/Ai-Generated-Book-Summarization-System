import streamlit as st
from utils.database import create_user, get_user_by_email, verify_user

# ---------- UI STYLE ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

/* remove default spacing */
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
}

/* full height */
html, body, [data-testid="stAppViewContainer"] {
    height: 100%;
}

/* ORIGINAL CARD */
.auth-container {
    max-width: 450px;
    width: 100%;
    padding: 2rem;
    background: linear-gradient(145deg, #0d1117 0%, #161b22 100%);
    border-radius: 24px;
    box-shadow: 
        0 25px 50px -12px rgba(0, 0, 0, 0.7),
        0 0 0 1px rgba(255, 255, 255, 0.05), 
        inset 0 1px 0 0 rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.title {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #64ffda, #00d4ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sub {
    text-align: center;
    color: #8b949e;
    margin-bottom: 2rem;
}

.error-message { color: #f85149; }
.success-message { color: #64ffda; }

</style>
""", unsafe_allow_html=True)


# ---------- AUTH PAGE ----------
def show_auth_page():
    with st.sidebar:
        st.markdown("### 📚 AI Books")

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "signup"

    # 🔥 TOP SPACE (vertical centering)
    st.markdown("<div style='height:20vh'></div>", unsafe_allow_html=True)

    # 🔥 HORIZONTAL CENTER
    left, center, right = st.columns([1, 2, 1])

    with center:
        st.markdown("<div class='auth-container'>", unsafe_allow_html=True)

        if st.session_state.auth_mode == "signup":
            show_signup()
        else:
            show_login()

        st.markdown("</div>", unsafe_allow_html=True)

    # 🔥 BOTTOM SPACE (balance)
    st.markdown("<div style='height:20vh'></div>", unsafe_allow_html=True)


# ---------- SIGNUP ----------
def show_signup():
    st.markdown("<div class='title'>✨ Create Account</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub'>Join now</div>", unsafe_allow_html=True)

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if not all([name, email, password]):
            st.markdown("<div class='error-message'>Fill all fields</div>", unsafe_allow_html=True)
            return

        if get_user_by_email(email):
            st.markdown("<div class='error-message'>User exists</div>", unsafe_allow_html=True)
            return

        create_user(name, email, password)
        st.success("Account created")
        st.session_state.auth_mode = "login"
        st.rerun()

    if st.button("Go to Login"):
        st.session_state.auth_mode = "login"
        st.rerun()


# ---------- LOGIN ----------
def show_login():
    st.markdown("<div class='title'>👋 Welcome Back</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub'>Login to continue</div>", unsafe_allow_html=True)

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        user = verify_user(email, password)
        if not user:
            st.markdown("<div class='error-message'>Invalid credentials</div>", unsafe_allow_html=True)
            return

        st.session_state.logged_in = True
        st.success("Logged in")
        st.rerun()

    if st.button("Create Account"):
        st.session_state.auth_mode = "signup"
        st.rerun()