import streamlit as st


def show_role_selector():
    st.set_page_config(page_title="Book Summarizer", layout="wide")

    selected_role = st.query_params.get("selected_role")
    if selected_role in ("user", "admin"):
        st.session_state.role = selected_role
        st.query_params.clear()
        st.rerun()

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        :root {
            --bg: #061026;
            --panel: rgba(7, 21, 48, 0.86);
            --panel-strong: rgba(9, 29, 63, 0.92);
            --cyan: #6de7ff;
            --blue: #4d8dff;
            --violet: #8b5cf6;
            --orange: #f0a46b;
            --text: #f4f8ff;
            --muted: #b8c4dd;
        }

        html, body, [data-testid="stAppViewContainer"] {
            min-height: 100%;
        }

        .stApp {
            font-family: 'Inter', sans-serif;
            color: var(--text);
            background:
                radial-gradient(circle at 23% 20%, rgba(122, 89, 255, 0.28), transparent 26rem),
                radial-gradient(circle at 72% 56%, rgba(0, 225, 255, 0.20), transparent 24rem),
                linear-gradient(135deg, #130a34 0%, #061026 38%, #041327 100%);
            overflow-x: hidden;
        }

        .block-container {
            max-width: 1500px;
            padding: 0 2.6rem !important;
        }

        header, footer, [data-testid="stHeader"], [data-testid="stToolbar"] {
            display: none !important;
        }

        .screen {
            position: relative;
            min-height: 100vh;
            display: grid;
            grid-template-columns: minmax(280px, 0.78fr) minmax(580px, 1.72fr);
            gap: 34px;
            align-items: stretch;
            padding: 28px 0 22px;
        }

        .screen::before,
        .screen::after {
            content: "";
            position: fixed;
            inset: auto;
            pointer-events: none;
            z-index: 0;
        }

        .screen::before {
            width: 560px;
            height: 560px;
            left: -150px;
            top: -120px;
            background: radial-gradient(circle, rgba(123, 97, 255, 0.34), transparent 68%);
            filter: blur(18px);
        }

        .screen::after {
            width: 520px;
            height: 520px;
            right: 10%;
            bottom: -180px;
            background: radial-gradient(circle, rgba(91, 226, 255, 0.20), transparent 70%);
            filter: blur(20px);
        }

        .intro-panel,
        .dashboard-panel {
            position: relative;
            z-index: 1;
            border: 1px solid rgba(126, 214, 255, 0.22);
            background: linear-gradient(180deg, rgba(7, 20, 48, 0.90), rgba(8, 14, 37, 0.82));
            box-shadow: 0 0 42px rgba(92, 106, 255, 0.22), inset 0 0 40px rgba(109, 231, 255, 0.04);
        }

        .intro-panel {
            border-right: 4px solid rgba(142, 91, 255, 0.72);
            border-radius: 0 28px 28px 0;
            min-height: calc(100vh - 50px);
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: clamp(28px, 4vw, 56px);
            overflow: hidden;
        }

        .intro-panel::before {
            content: "";
            position: absolute;
            inset: 0;
            background-image:
                linear-gradient(90deg, rgba(109, 231, 255, 0.10) 1px, transparent 1px),
                linear-gradient(rgba(109, 231, 255, 0.08) 1px, transparent 1px);
            background-size: 54px 54px;
            mask-image: radial-gradient(circle at 45% 55%, black, transparent 72%);
            opacity: 0.45;
        }

        .intro-content {
            position: relative;
            z-index: 1;
        }

        .kicker {
            color: var(--cyan);
            font-size: 13px;
            font-weight: 800;
            letter-spacing: 0;
            text-transform: uppercase;
        }

        .brand-title {
            margin-top: 14px;
            color: #dff4ff;
            font-size: clamp(42px, 4.6vw, 74px);
            font-weight: 900;
            line-height: 1.05;
            text-transform: uppercase;
            text-shadow: 0 0 16px rgba(109, 231, 255, 0.54), 0 0 42px rgba(139, 92, 246, 0.36);
        }

        .intro-list {
            display: grid;
            gap: 18px;
            margin-top: 48px;
            color: #e4ecff;
            font-size: clamp(17px, 1.7vw, 25px);
            font-weight: 700;
        }

        .intro-list div {
            display: flex;
            align-items: center;
            gap: 14px;
            text-shadow: 0 0 12px rgba(255, 255, 255, 0.18);
        }

        .dot {
            width: 13px;
            height: 13px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--cyan), var(--violet));
            box-shadow: 0 0 18px rgba(109, 231, 255, 0.88);
            flex: 0 0 auto;
        }

        .book-chip {
            width: min(230px, 70%);
            aspect-ratio: 1.15;
            margin: 60px auto 0;
            border-radius: 26px;
            display: grid;
            place-items: center;
            color: #dff8ff;
            background:
                linear-gradient(145deg, rgba(109, 231, 255, 0.25), rgba(139, 92, 246, 0.16)),
                linear-gradient(180deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.02));
            border: 1px solid rgba(109, 231, 255, 0.30);
            box-shadow: 0 0 44px rgba(109, 231, 255, 0.24);
        }

        .book-icon {
            position: relative;
            width: 98px;
            height: 116px;
            border-radius: 12px 22px 22px 12px;
            background: linear-gradient(135deg, #173e78, #1d9fc5);
            box-shadow: 12px 10px 0 rgba(17, 21, 55, 0.55), 0 0 28px rgba(109, 231, 255, 0.6);
            transform: rotate(-8deg);
        }

        .book-icon::before {
            content: "AI";
            position: absolute;
            inset: 26px 14px auto;
            height: 50px;
            display: grid;
            place-items: center;
            border: 1px solid rgba(255, 255, 255, 0.42);
            border-radius: 8px;
            font-size: 30px;
            font-weight: 900;
        }

        .book-icon::after {
            content: "";
            position: absolute;
            left: 16px;
            right: 18px;
            bottom: 18px;
            height: 3px;
            background: rgba(255, 255, 255, 0.62);
            box-shadow: 0 10px 0 rgba(255, 255, 255, 0.42);
        }

        .dashboard-panel {
            border-radius: 24px;
            min-height: calc(100vh - 50px);
            padding: clamp(24px, 3.5vw, 52px);
            overflow: hidden;
        }

        .dashboard-panel::before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(90deg, transparent 0 8%, rgba(109, 231, 255, 0.10) 8% 8.25%, transparent 8.25% 100%),
                radial-gradient(circle at 48% 50%, rgba(21, 201, 255, 0.18), transparent 28%),
                radial-gradient(circle at 68% 45%, rgba(139, 92, 246, 0.22), transparent 22%);
            opacity: 0.72;
        }

        .dashboard-panel::after {
            content: "";
            position: absolute;
            inset: 28px;
            border-top: 1px solid rgba(109, 231, 255, 0.18);
            border-bottom: 1px solid rgba(109, 231, 255, 0.18);
            pointer-events: none;
        }

        .dashboard-content {
            position: relative;
            z-index: 1;
        }

        .welcome {
            text-align: center;
            margin: 18px 0 32px;
            color: #fbfdff;
            font-size: clamp(25px, 2.55vw, 40px);
            font-weight: 900;
            text-transform: uppercase;
            text-shadow: 0 0 18px rgba(255, 255, 255, 0.24);
        }

        .role-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(250px, 1fr));
            gap: 34px;
            max-width: 780px;
            margin: 0 auto;
        }

        .role-card {
            position: relative;
            min-height: 492px;
            border-radius: 16px;
            padding: 18px;
            padding-bottom: 96px;
            background: linear-gradient(180deg, rgba(9, 31, 70, 0.88), rgba(7, 18, 45, 0.88));
            border: 2px solid rgba(109, 231, 255, 0.72);
            box-shadow: 0 0 22px rgba(109, 231, 255, 0.20), inset 0 0 22px rgba(109, 231, 255, 0.05);
        }

        .role-card.admin {
            border-color: rgba(240, 164, 107, 0.82);
            box-shadow: 0 0 22px rgba(240, 164, 107, 0.20), inset 0 0 22px rgba(139, 92, 246, 0.06);
        }

        .avatar {
            height: 178px;
            display: grid;
            place-items: center;
            margin-bottom: 14px;
        }

        .reader-orb,
        .admin-orb {
            position: relative;
            width: 132px;
            height: 132px;
            border-radius: 50%;
            display: grid;
            place-items: center;
            color: #eafaff;
            font-size: 56px;
            font-weight: 900;
            background: radial-gradient(circle at 35% 30%, #e8fbff, #57c5ff 32%, #4968ff 68%, #7d55ff);
            box-shadow: 0 0 28px rgba(109, 231, 255, 0.62), 0 18px 0 rgba(139, 92, 246, 0.18);
        }

        .admin-orb {
            background: radial-gradient(circle at 35% 30%, #fff3df, #f0a46b 35%, #7857ff 78%);
            box-shadow: 0 0 28px rgba(240, 164, 107, 0.62), 0 18px 0 rgba(109, 231, 255, 0.14);
        }

        .reader-orb::after {
            content: "";
            position: absolute;
            width: 78px;
            height: 48px;
            bottom: -5px;
            border-radius: 10px;
            background: linear-gradient(135deg, #1d7fc0, #6de7ff);
            box-shadow: inset 0 0 0 3px rgba(255, 255, 255, 0.24);
            transform: rotate(-8deg);
        }

        .admin-orb::after {
            content: "";
            position: absolute;
            width: 116px;
            height: 72px;
            bottom: -16px;
            border-radius: 12px;
            border: 2px solid rgba(109, 231, 255, 0.76);
            background:
                linear-gradient(90deg, rgba(109, 231, 255, 0.35), transparent 2px),
                linear-gradient(rgba(109, 231, 255, 0.30), transparent 2px);
            background-size: 28px 22px;
            transform: perspective(120px) rotateX(18deg);
        }

        .role-title {
            width: 100%;
            border-radius: 9px;
            padding: 11px 14px;
            color: #f7fbff;
            text-align: center;
            font-size: clamp(18px, 1.6vw, 25px);
            font-weight: 900;
            text-transform: uppercase;
            background: linear-gradient(90deg, rgba(55, 155, 204, 0.92), rgba(125, 76, 225, 0.92));
            box-shadow: 0 0 18px rgba(109, 231, 255, 0.22);
        }

        .admin .role-title {
            background: linear-gradient(90deg, rgba(166, 112, 79, 0.95), rgba(125, 76, 225, 0.92));
            box-shadow: 0 0 18px rgba(240, 164, 107, 0.22);
        }

        .feature-list {
            margin: 18px 0 18px;
            display: grid;
            gap: 12px;
            color: #ffffff;
            font-size: clamp(14px, 1.25vw, 18px);
            line-height: 1.25;
        }

        .feature-list div {
            display: grid;
            grid-template-columns: 22px 1fr;
            gap: 10px;
            align-items: start;
        }

        .mini-icon {
            color: var(--cyan);
            font-weight: 900;
            text-align: center;
        }

        .admin .mini-icon {
            color: var(--orange);
        }

        .card-action {
            position: absolute;
            left: 18px;
            right: 18px;
            bottom: 18px;
            min-height: 58px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid rgba(109, 231, 255, 0.72);
            border-radius: 999px;
            color: #eaf6ff;
            background: linear-gradient(90deg, rgba(27, 117, 169, 0.86), rgba(109, 72, 204, 0.82));
            box-shadow: 0 0 20px rgba(109, 231, 255, 0.36), inset 0 0 18px rgba(255, 255, 255, 0.06);
            font-size: 15px;
            font-weight: 900;
            text-transform: uppercase;
            text-decoration: none;
            transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
        }

        .card-action:hover {
            transform: translateY(-3px);
            color: #ffffff;
            border-color: rgba(255, 255, 255, 0.90);
            box-shadow: 0 0 30px rgba(109, 231, 255, 0.56);
            text-decoration: none;
        }

        .admin .card-action {
            border-color: rgba(240, 164, 107, 0.78);
            background: linear-gradient(90deg, rgba(31, 117, 169, 0.86), rgba(103, 64, 188, 0.84));
            box-shadow: 0 0 20px rgba(240, 164, 107, 0.26), inset 0 0 18px rgba(255, 255, 255, 0.06);
        }

        .copyright {
            position: absolute;
            z-index: 1;
            left: 0;
            right: 0;
            bottom: 22px;
            text-align: center;
            color: rgba(255, 255, 255, 0.76);
            font-size: 13px;
        }

        @media (max-width: 1050px) {
            .block-container {
                padding: 0 1rem !important;
            }

            .screen {
                grid-template-columns: 1fr;
                gap: 18px;
                padding: 16px 0;
            }

            .intro-panel,
            .dashboard-panel {
                min-height: auto;
                border-radius: 22px;
                border-right-width: 1px;
            }

            .intro-list {
                margin-top: 26px;
            }

            .book-chip {
                margin-top: 32px;
                width: 190px;
            }

            .role-grid {
                max-width: 720px;
            }

            .copyright {
                position: relative;
                bottom: auto;
                margin-top: 26px;
            }
        }

        @media (max-width: 720px) {
            .dashboard-panel {
                padding: 22px 16px;
            }

            .role-grid {
                grid-template-columns: 1fr;
                gap: 24px;
            }

            .role-card {
                min-height: 470px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <main class="screen">
            <section class="intro-panel">
                <div class="intro-content">
                    <div class="kicker">AI-powered learning suite</div>
                    <div class="brand-title">AI-Powered<br>Book Summaries</div>
                    <div class="intro-list">
                        <div><span class="dot"></span><span>Instant Key Insights</span></div>
                        <div><span class="dot"></span><span>Unlock Knowledge Faster</span></div>
                        <div><span class="dot"></span><span>Summaries of Bestsellers</span></div>
                        <div><span class="dot"></span><span>Effortless Learning</span></div>
                    </div>
                    <div class="book-chip" aria-hidden="true">
                        <div class="book-icon"></div>
                    </div>
                </div>
            </section>
            <section class="dashboard-panel">
                <div class="dashboard-content">
                    <h1 class="welcome">Welcome To Our Summarization Platform</h1>
                    <div class="role-grid">
                        <div class="role-card reader">
                            <div class="avatar"><div class="reader-orb">R</div></div>
                            <div class="role-title">Log In As Reader</div>
                            <div class="feature-list">
                                <div><span class="mini-icon">#</span><span>Access Diverse Book Summaries</span></div>
                                <div><span class="mini-icon">+</span><span>Create Reading Lists</span></div>
                                <div><span class="mini-icon">*</span><span>Rate and Review</span></div>
                                <div><span class="mini-icon">&gt;</span><span>Personalized Recommendations</span></div>
                            </div>
                            <a class="card-action" href="?selected_role=user">Go To Reader Dashboard</a>
                        </div>
                        <div class="role-card admin">
                            <div class="avatar"><div class="admin-orb">A</div></div>
                            <div class="role-title">Log In As Admin</div>
                            <div class="feature-list">
                                <div><span class="mini-icon">[]</span><span>Manage Book Content</span></div>
                                <div><span class="mini-icon">@</span><span>Monitor Platform Activity</span></div>
                                <div><span class="mini-icon">%</span><span>Analyze Usage Trends</span></div>
                                <div><span class="mini-icon">o</span><span>User Account Management</span></div>
                            </div>
                            <a class="card-action" href="?selected_role=admin">Access Admin Panel</a>
                        </div>
                    </div>
                </div>
                <div class="copyright">Copyright (c) 2026 Summaries, Inc.</div>
            </section>
        </main>
        """,
        unsafe_allow_html=True,
    )


show_role_selector()
