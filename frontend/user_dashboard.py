import html
import streamlit as st
import streamlit.components.v1 as components
from utils.database import get_user_dashboard_stats


def show_user_dashboard(user_id):
    stats = get_user_dashboard_stats(user_id)

    books_count = stats["books_count"]
    summaries_count = stats["summaries_count"]
    recent_books = stats["recent_books"]
    recent_count = len(recent_books)
    pending_count = max(books_count - summaries_count, 0)

    if recent_books:
        books_html = ""
        for book in recent_books:
            title = html.escape(str(book["title"]))
            status = html.escape(str(book.get("status", "uploaded")))
            date = book["created_at"].strftime("%d %b %Y")

            books_html += f"""
            <div class="book-card">
                <div>
                    <div class="book-title">{title}</div>
                    <div class="book-meta">Uploaded on {date}</div>
                </div>
                <div class="status-pill">{status}</div>
            </div>
            """
    else:
        books_html = """
        <div class="empty-card">
            <div class="empty-icon">📚</div>
            <div>No books uploaded yet</div>
            <p>Upload your first book and start creating AI summaries.</p>
        </div>
        """

    dashboard_html = f"""
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
        color: white;
        background: transparent;
    }}

    .dashboard {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 18px;
    }}

    .hero-card {{
        position: relative;
        overflow: hidden;
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 22px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(0,212,255,0.28);
        backdrop-filter: blur(18px);
        animation: fadeUp .7s ease both;
    }}

    .hero-card::before {{
        content: "";
        position: absolute;
        width: 280px;
        height: 280px;
        right: -100px;
        top: -120px;
        background: radial-gradient(circle, rgba(0,212,255,.35), transparent 70%);
        animation: pulse 4s infinite ease-in-out;
    }}

    .hero-card h1 {{
        margin: 0;
        font-size: 34px;
        font-weight: 800;
    }}

    .hero-card p {{
        margin: 8px 0 0;
        color: #a0a0c0;
    }}

    .stats-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 18px;
        margin-bottom: 22px;
    }}

    .stat-card {{
        position: relative;
        overflow: hidden;
        min-height: 180px;
        border-radius: 22px;
        padding: 22px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(0,212,255,0.25);
        backdrop-filter: blur(18px);
        animation: fadeUp .7s ease both;
        transition: .35s ease;
    }}

    .stat-card:nth-child(1) {{ animation-delay: .05s; }}
    .stat-card:nth-child(2) {{ animation-delay: .15s; }}
    .stat-card:nth-child(3) {{ animation-delay: .25s; }}
    .stat-card:nth-child(4) {{ animation-delay: .35s; }}

    .stat-card:hover {{
        transform: translateY(-10px) scale(1.02);
        border-color: rgba(0,212,255,.75);
        box-shadow: 0 24px 60px rgba(0,212,255,.18);
    }}

    .stat-card::after {{
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(110deg, transparent, rgba(255,255,255,.12), transparent);
        transform: translateX(-120%);
    }}

    .stat-card:hover::after {{
        animation: shimmer .8s ease;
    }}

    .stat-icon {{
        width: 52px;
        height: 52px;
        display: grid;
        place-items: center;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(0,212,255,.25), rgba(124,58,237,.25));
        font-size: 24px;
        margin-bottom: 20px;
        animation: floatIcon 3s infinite ease-in-out;
    }}

    .stat-number {{
        font-size: 44px;
        line-height: 1;
        font-weight: 900;
        background: linear-gradient(135deg, #00d4ff, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .stat-label {{
        margin-top: 8px;
        font-weight: 800;
        font-size: 16px;
    }}

    .stat-note {{
        color: #a0a0c0;
        font-size: 13px;
        margin-top: 5px;
    }}

    .content-grid {{
        display: grid;
        grid-template-columns: 1.35fr .65fr;
        gap: 18px;
    }}

    .panel-card {{
        border-radius: 22px;
        padding: 22px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(0,212,255,0.25);
        backdrop-filter: blur(18px);
        animation: fadeUp .8s ease both .3s;
    }}

    .panel-head {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 18px;
    }}

    .panel-head h2,
    .panel-head h3 {{
        margin: 0;
        color: #00d4ff;
    }}

    .panel-head span {{
        color: #a0a0c0;
        font-size: 13px;
    }}

    .book-card {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 14px;
        margin-bottom: 12px;
        padding: 16px;
        border-radius: 16px;
        background: rgba(0,212,255,.06);
        border: 1px solid rgba(0,212,255,.18);
        animation: slideIn .55s ease both;
        transition: .3s ease;
    }}

    .book-card:hover {{
        transform: translateX(8px);
        background: rgba(0,212,255,.12);
        border-color: rgba(0,212,255,.42);
    }}

    .book-title {{
        font-weight: 800;
        color: white;
    }}

    .book-meta {{
        margin-top: 4px;
        color: #8e8eaa;
        font-size: 13px;
    }}

    .status-pill {{
        white-space: nowrap;
        padding: 7px 11px;
        border-radius: 999px;
        color: #00d4ff;
        background: rgba(0,212,255,.08);
        border: 1px solid rgba(0,212,255,.28);
        font-size: 12px;
        font-weight: 800;
    }}

    .action-card {{
        padding: 16px;
        margin-top: 12px;
        border-radius: 16px;
        color: white;
        font-weight: 800;
        background: rgba(0,212,255,.07);
        border: 1px solid rgba(0,212,255,.18);
        transition: .3s ease;
    }}

    .action-card:hover {{
        transform: translateX(8px);
        background: rgba(0,212,255,.14);
        border-color: rgba(0,212,255,.45);
    }}

    .motivation-text {{
        color: #a0a0c0;
        line-height: 1.7;
    }}

    .empty-card {{
        text-align: center;
        padding: 40px 20px;
        color: #a0a0c0;
    }}

    .empty-icon {{
        font-size: 46px;
        margin-bottom: 12px;
        animation: floatIcon 3s infinite ease-in-out;
    }}

    @keyframes fadeUp {{
        from {{ opacity: 0; transform: translateY(26px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes slideIn {{
        from {{ opacity: 0; transform: translateX(-18px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}

    @keyframes floatIcon {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-7px); }}
    }}

    @keyframes pulse {{
        0%, 100% {{ opacity: .55; transform: scale(1); }}
        50% {{ opacity: 1; transform: scale(1.15); }}
    }}

    @keyframes shimmer {{
        from {{ transform: translateX(-120%); }}
        to {{ transform: translateX(120%); }}
    }}

    @media (max-width: 950px) {{
        .stats-grid {{
            grid-template-columns: repeat(2, 1fr);
        }}

        .content-grid {{
            grid-template-columns: 1fr;
        }}
    }}

    @media (max-width: 560px) {{
        .stats-grid {{
            grid-template-columns: 1fr;
        }}

        .book-card {{
            flex-direction: column;
            align-items: flex-start;
        }}
    }}
    </style>
    </head>

    <body>
        <div class="dashboard">
            <div class="hero-card">
                <h1>📊 Your Dashboard</h1>
                <p>Your animated book summarization workspace</p>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon">📚</div>
                    <div class="stat-number">{books_count}</div>
                    <div class="stat-label">Books Uploaded</div>
                    <div class="stat-note">Total books in your library</div>
                </div>

                <div class="stat-card">
                    <div class="stat-icon">📝</div>
                    <div class="stat-number">{summaries_count}</div>
                    <div class="stat-label">Summaries Ready</div>
                    <div class="stat-note">AI-generated reading shortcuts</div>
                </div>

                <div class="stat-card">
                    <div class="stat-icon">🕘</div>
                    <div class="stat-number">{recent_count}</div>
                    <div class="stat-label">Recent Uploads</div>
                    <div class="stat-note">Latest books shown below</div>
                </div>

                <div class="stat-card">
                    <div class="stat-icon">⚡</div>
                    <div class="stat-number">{pending_count}</div>
                    <div class="stat-label">Pending Work</div>
                    <div class="stat-note">Books awaiting summaries</div>
                </div>
            </div>

            <div class="content-grid">
                <div class="panel-card">
                    <div class="panel-head">
                        <h2>📘 Recently Uploaded Books</h2>
                        <span>Latest activity</span>
                    </div>
                    {books_html}
                </div>

                <div class="panel-card">
                    <div class="panel-head">
                        <h3>🚀 Keep Growing</h3>
                    </div>
                    <p class="motivation-text">
                        Upload more books to unlock summaries, save time, and build your personal learning archive.
                    </p>

                    <div class="action-card">✨ Turn books into insights</div>
                    <div class="action-card">🔎 Search your knowledge base</div>
                    <div class="action-card">📈 Grow your reading history</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    height = 760 + min(recent_count, 6) * 70
    components.html(dashboard_html, height=height, scrolling=True)
