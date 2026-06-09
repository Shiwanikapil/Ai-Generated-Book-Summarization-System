import streamlit as st
import streamlit.components.v1 as components

from utils.database import (
    get_users_with_books,
    admin_get_latest_summary,
    admin_delete_book
)


st.markdown("""
<style>
.admin-books-container {
    max-width: 1250px;
    margin: 0 auto;
    padding: 20px;
}

.admin-books-header {
    position: relative;
    overflow: hidden;
    margin-bottom: 1.2rem;
    padding: 1.7rem;
    border-radius: 22px;
    background: rgba(255, 255, 255, 0.08);
    border: 1.5px solid rgba(0, 212, 255, 0.28);
    backdrop-filter: blur(22px);
    box-shadow: 0 18px 55px rgba(0, 212, 255, 0.08);
    animation: booksFadeUp .65s ease both;
}

.admin-books-header::before {
    content: "";
    position: absolute;
    width: 280px;
    height: 280px;
    right: -110px;
    top: -130px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0, 212, 255, 0.30), transparent 70%);
    animation: booksPulse 4s ease-in-out infinite;
}

.admin-books-header h1 {
    position: relative;
    z-index: 1;
    margin: 0;
    font-size: 2.05rem;
    font-weight: 800;
}

.admin-books-header p {
    position: relative;
    z-index: 1;
    color: #a0a0c0;
    margin: 0.4rem 0 0;
}

.user-section {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(20px);
    border: 1.5px solid rgba(0, 212, 255, 0.26);
    border-radius: 22px;
    padding: 1.2rem;
    margin-bottom: 1.4rem;
    transition: all 0.3s ease;
    box-shadow: 0 16px 45px rgba(0, 212, 255, 0.08);
    animation: booksFadeUp .7s ease both;
}

.user-section:hover {
    border-color: rgba(0, 212, 255, 0.55);
    background: rgba(255, 255, 255, 0.10);
}

.user-section-title {
    color: #ffffff;
    font-size: 1.15rem;
    font-weight: 800;
    margin-bottom: 1rem;
    padding: 0.2rem 0 1rem;
    border-bottom: 1px solid rgba(0, 212, 255, 0.18);
}

.user-section-title span {
    font-size: 0.88rem;
    color: #a0a0c0;
    font-weight: 500;
}

.book-item {
    background: rgba(0, 212, 255, 0.05);
    border: 1px solid rgba(0, 212, 255, 0.16);
    border-radius: 18px;
    padding: 1rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.book-item:hover {
    background: rgba(0, 212, 255, 0.10);
    border-color: rgba(0, 212, 255, 0.38);
    transform: translateX(6px);
}

.book-title-admin {
    font-size: 1.05rem;
    font-weight: 800;
    color: #ffffff;
}

.book-date {
    margin-top: 0.3rem;
    font-size: 0.86rem;
    color: #a0a0c0;
}

.summary-viewer-admin {
    background: rgba(0, 212, 255, 0.05);
    border: 1px solid rgba(0, 212, 255, 0.20);
    border-radius: 14px;
    padding: 1.3rem;
    margin-top: 1rem;
    max-height: 400px;
    overflow-y: auto;
    color: #e0e0e0;
    line-height: 1.7;
    font-size: 0.95rem;
}

.empty-books-state {
    text-align: center;
    padding: 4rem 2rem;
    color: #a0a0c0;
}

.empty-books-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.admin-books-container div.stButton > button {
    min-height: 42px !important;
    height: 42px !important;
    border-radius: 999px !important;
    font-size: 0.86rem !important;
    font-weight: 800 !important;
    transition: all 0.25s ease !important;
}

.admin-books-container div.stButton > button:hover {
    transform: translateY(-2px) !important;
}

/* Summary button */
.admin-books-container div.stButton > button[kind="secondary"] {
    background: linear-gradient(135deg, #00d4ff 0%, #7c3aed 100%) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 12px 26px rgba(0, 212, 255, 0.18) !important;
}

@keyframes booksFadeUp {
    from { opacity: 0; transform: translateY(22px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes booksPulse {
    0%, 100% { opacity: .55; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.14); }
}
</style>
""", unsafe_allow_html=True)


def render_book_stats(total_books, total_users_with_books):
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

    .books-stats-wrap {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
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
        .books-stats-wrap {{
            grid-template-columns: 1fr;
        }}
    }}
    </style>
    </head>
    <body>
        <div class="books-stats-wrap">
            <div class="stat-card">
                <div class="stat-icon">📚</div>
                <div class="stat-value">{total_books}</div>
                <div class="stat-label">Total Books</div>
            </div>

            <div class="stat-card">
                <div class="stat-icon">👥</div>
                <div class="stat-value">{total_users_with_books}</div>
                <div class="stat-label">Users with Books</div>
            </div>
        </div>
    </body>
    </html>
    """

    components.html(stats_html, height=170, scrolling=False)


def show_admin_books():
    st.markdown('<div class="admin-books-container">', unsafe_allow_html=True)

    st.markdown("""
    <div class="admin-books-header">
        <h1>📚 Books Management</h1>
        <p>Manage all user books and summaries from one clean control panel.</p>
    </div>
    """, unsafe_allow_html=True)

    users = get_users_with_books()

    if not users:
        st.markdown("""
        <div class="empty-books-state">
            <div class="empty-books-icon">📚</div>
            <p style="font-size: 1.1rem;">No users or books found</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    total_books = sum(len(u.get("books", [])) for u in users)
    total_users_with_books = sum(1 for u in users if u.get("books"))

    render_book_stats(total_books, total_users_with_books)

    for user in users:
        if not user.get("books"):
            continue

        st.markdown('<div class="user-section">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="user-section-title">
            👤 {user['name']}
            <span>({user['email']})</span>
        </div>
        """, unsafe_allow_html=True)

        for book in user["books"]:
            st.markdown('<div class="book-item">', unsafe_allow_html=True)

            col1, col2 = st.columns([4, 1], gap="small")

            with col1:
                st.markdown(f"""
                <div>
                    <div class="book-title-admin">📘 {book['title']}</div>
                    <div class="book-date">📅 Uploaded on {book['created_at'].strftime('%d %b %Y')}</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                if st.button("Delete", key=f"del_{book['_id']}", use_container_width=True):
                    admin_delete_book(book["_id"])
                    st.success("✅ Book deleted")
                    st.rerun()

            if st.button("View Summary", key=f"view_{book['_id']}", use_container_width=True):
                summary_doc = admin_get_latest_summary(book["_id"])

                if summary_doc:
                    summary_text = (
                        summary_doc.get("summary_text")
                        or summary_doc.get("summary")
                        or "📌 Summary text not found"
                    )

                    st.markdown('<div class="summary-viewer-admin">', unsafe_allow_html=True)
                    st.markdown(summary_text)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ No summary found for this book")

            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
 