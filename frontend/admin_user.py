import streamlit as st
import streamlit.components.v1 as components

from utils.database import (
    get_all_users,
    deactivate_user,
    activate_user,
    delete_user,
    get_user_book_count
)


st.markdown("""
<style>
.users-container {
    max-width: 1250px;
    margin: 0 auto;
    padding: 20px;
}

.users-header {
    position: relative;
    overflow: hidden;
    margin-bottom: 1.2rem;
    padding: 1.6rem;
    border-radius: 22px;
    background: rgba(255, 255, 255, 0.08);
    border: 1.5px solid rgba(0, 212, 255, 0.28);
    backdrop-filter: blur(22px);
    box-shadow: 0 18px 55px rgba(0, 212, 255, 0.08);
    animation: usersFadeUp .65s ease both;
}

.users-header::before {
    content: "";
    position: absolute;
    width: 260px;
    height: 260px;
    right: -100px;
    top: -120px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0, 212, 255, 0.28), transparent 70%);
    animation: usersPulse 4s ease-in-out infinite;
}

.users-header h1 {
    position: relative;
    z-index: 1;
    margin: 0;
    font-size: 2rem;
    font-weight: 800;
}

.users-header p {
    position: relative;
    z-index: 1;
    color: #a0a0c0;
    margin: 0.4rem 0 0;
}

.users-table-container {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(20px);
    border: 1.5px solid rgba(0, 212, 255, 0.26);
    border-radius: 22px;
    padding: 1rem;
    margin-top: 1.1rem;
    box-shadow: 0 18px 55px rgba(0, 212, 255, 0.08);
    animation: usersFadeUp .75s ease both .28s;
}

.user-row-card {
    border-radius: 16px;
    padding: 1rem;
    margin-bottom: 0.85rem;
    background: rgba(0, 212, 255, 0.05);
    border: 1px solid rgba(0, 212, 255, 0.14);
    transition: all 0.3s ease;
}

.user-row-card:hover {
    background: rgba(0, 212, 255, 0.10);
    border-color: rgba(0, 212, 255, 0.34);
    transform: translateX(6px);
}

.user-info {
    padding: 0.2rem 0;
}

.user-name {
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.25rem;
}

.user-email {
    font-size: 0.88rem;
    color: #a0a0c0;
}

.user-meta {
    display: grid;
    gap: 0.35rem;
    font-size: 0.88rem;
    color: #a0a0c0;
}

.user-status-active,
.user-status-inactive {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 86px;
    padding: 7px 12px;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 800;
}

.user-status-active {
    background: rgba(34, 197, 94, 0.14);
    color: #4ade80;
    border: 1px solid rgba(34, 197, 94, 0.34);
}

.user-status-inactive {
    background: rgba(239, 68, 68, 0.14);
    color: #fb7185;
    border: 1px solid rgba(239, 68, 68, 0.34);
}

.users-table-container div.stButton > button {
    min-height: 38px !important;
    height: 38px !important;
    border-radius: 999px !important;
    font-size: 0.82rem !important;
    font-weight: 800 !important;
    margin-bottom: 0.35rem !important;
    transition: all 0.25s ease !important;
}

.users-table-container div.stButton > button:hover {
    transform: translateY(-2px) !important;
}

.empty-users-state {
    text-align: center;
    padding: 4rem 2rem;
    color: #a0a0c0;
}

.empty-users-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

@keyframes usersFadeUp {
    from { opacity: 0; transform: translateY(22px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes usersPulse {
    0%, 100% { opacity: .55; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.14); }
}

@media (max-width: 800px) {
    .user-row-card {
        padding: 0.85rem;
    }
}
</style>
""", unsafe_allow_html=True)


def render_user_stats(total_users, active_users, inactive_users):
    stats_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    * {{
        box-sizing: border-box;
        font-family: Inter, Arial, sans-serif;
    }}

    body {{
        margin: 0;
        background: transparent;
        color: white;
        overflow: hidden;
    }}

    .users-stats-wrap {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        padding: 8px;
    }}

    .stat-card {{
        position: relative;
        overflow: hidden;
        min-height: 138px;
        border-radius: 22px;
        padding: 20px;
        background:
            linear-gradient(145deg, rgba(255,255,255,.12), rgba(255,255,255,.055)),
            rgba(255,255,255,.06);
        border: 1px solid rgba(0,212,255,.28);
        box-shadow:
            0 16px 45px rgba(0,212,255,.12),
            inset 0 1px 0 rgba(255,255,255,.14);
        backdrop-filter: blur(20px);
        animation: cardIn .65s ease both;
        transition: all .3s ease;
    }}

    .stat-card:nth-child(1) {{ animation-delay: .05s; }}
    .stat-card:nth-child(2) {{ animation-delay: .15s; }}
    .stat-card:nth-child(3) {{ animation-delay: .25s; }}

    .stat-card::before {{
        content: "";
        position: absolute;
        width: 150px;
        height: 150px;
        right: -58px;
        bottom: -70px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(124,58,237,.34), transparent 70%);
        transition: .3s ease;
    }}

    .stat-card::after {{
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(110deg, transparent 0 40%, rgba(255,255,255,.13) 50%, transparent 62%);
        transform: translateX(-120%);
    }}

    .stat-card:hover {{
        transform: translateY(-7px) scale(1.015);
        border-color: rgba(0,212,255,.75);
        box-shadow: 0 24px 60px rgba(0,212,255,.20);
    }}

    .stat-card:hover::before {{
        transform: scale(1.25);
        background: radial-gradient(circle, rgba(0,212,255,.38), transparent 70%);
    }}

    .stat-card:hover::after {{
        animation: shimmer .8s ease;
    }}

    .stat-icon {{
        width: 44px;
        height: 44px;
        display: grid;
        place-items: center;
        border-radius: 14px;
        margin-bottom: 12px;
        background: linear-gradient(135deg, rgba(0,212,255,.26), rgba(124,58,237,.26));
        border: 1px solid rgba(255,255,255,.14);
        font-size: 20px;
        position: relative;
        z-index: 1;
    }}

    .stat-value {{
        position: relative;
        z-index: 1;
        font-size: 34px;
        line-height: 1;
        font-weight: 900;
        background: linear-gradient(135deg, #00d4ff, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .stat-label {{
        position: relative;
        z-index: 1;
        margin-top: 7px;
        color: #ffffff;
        font-size: 14px;
        font-weight: 800;
    }}

    @keyframes cardIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes shimmer {{
        from {{ transform: translateX(-120%); }}
        to {{ transform: translateX(120%); }}
    }}

    @media (max-width: 720px) {{
        body {{ overflow: auto; }}
        .users-stats-wrap {{
            grid-template-columns: 1fr;
        }}
    }}
    </style>
    </head>
    <body>
        <div class="users-stats-wrap">
            <div class="stat-card">
                <div class="stat-icon">👥</div>
                <div class="stat-value">{total_users}</div>
                <div class="stat-label">Total Users</div>
            </div>

            <div class="stat-card">
                <div class="stat-icon">✅</div>
                <div class="stat-value">{active_users}</div>
                <div class="stat-label">Active Users</div>
            </div>

            <div class="stat-card">
                <div class="stat-icon">⏸</div>
                <div class="stat-value">{inactive_users}</div>
                <div class="stat-label">Inactive Users</div>
            </div>
        </div>
    </body>
    </html>
    """

    components.html(stats_html, height=170, scrolling=False)


def show_admin_users():
    st.markdown('<div class="users-container">', unsafe_allow_html=True)

    st.markdown("""
    <div class="users-header">
        <h1>👥 Users Management</h1>
        <p>Manage reader accounts, activity status, and uploaded book counts.</p>
    </div>
    """, unsafe_allow_html=True)

    users = get_all_users()

    if not users:
        st.markdown("""
        <div class="empty-users-state">
            <div class="empty-users-icon">👥</div>
            <p style="font-size: 1.1rem;">No users found</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    total_users = len(users)
    active_users = sum(1 for u in users if u.get("is_active", True))
    inactive_users = total_users - active_users

    render_user_stats(total_users, active_users, inactive_users)

    st.markdown('<div class="users-table-container">', unsafe_allow_html=True)

    for user in users:
        st.markdown('<div class="user-row-card">', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns([2.5, 1.3, 1, 1.4], gap="small")

        with col1:
            st.markdown(f"""
            <div class="user-info">
                <div class="user-name">👤 {user["name"]}</div>
                <div class="user-email">{user["email"]}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            joined = user["created_at"].strftime("%d-%m-%Y")
            book_count = get_user_book_count(user["_id"])
            st.markdown(f"""
            <div class="user-meta">
                <span>📅 Joined {joined}</span>
                <span>📚 {book_count} Books</span>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            status = "Active" if user.get("is_active", True) else "Inactive"
            status_class = "user-status-active" if status == "Active" else "user-status-inactive"
            st.markdown(f'<div class="{status_class}">● {status}</div>', unsafe_allow_html=True)

        with col4:
            if user.get("is_active", True):
                if st.button("Deactivate", key=f"deact_{user['_id']}", use_container_width=True):
                    deactivate_user(user["_id"])
                    st.success("✅ User deactivated")
                    st.rerun()
            else:
                if st.button("Activate", key=f"act_{user['_id']}", use_container_width=True):
                    activate_user(user["_id"])
                    st.success("✅ User activated")
                    st.rerun()

            if st.button("Delete", key=f"del_{user['_id']}", use_container_width=True):
                delete_user(user["_id"])
                st.success("✅ User deleted")
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)
