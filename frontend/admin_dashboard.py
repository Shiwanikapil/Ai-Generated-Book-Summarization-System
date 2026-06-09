import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

from utils.database import (
    get_total_users,
    get_active_users,
    get_total_books,
    get_total_summaries,
    get_most_active_users,
)


st.markdown("""
<style>
[data-testid="stPlotlyChart"] {
    background: rgba(255, 255, 255, 0.08);
    border: 1.5px solid rgba(0, 212, 255, 0.28);
    border-radius: 22px;
    padding: 18px;
    box-shadow: 0 18px 55px rgba(0, 212, 255, 0.10);
    backdrop-filter: blur(22px);
    animation: adminFadeUp .7s ease both;
}

.admin-chart-title {
    margin: 26px 0 12px;
    color: #00d4ff;
    font-size: 1.35rem;
    font-weight: 800;
}

.admin-chart-subtitle {
    color: #a0a0c0;
    margin-top: -8px;
    margin-bottom: 14px;
    font-size: .9rem;
}

@keyframes adminFadeUp {
    from { opacity: 0; transform: translateY(22px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)


def show_admin_dashboard():
    total_users = get_total_users()
    active_users = get_active_users()
    total_books = get_total_books()
    total_summaries = get_total_summaries()
    active_users_data = get_most_active_users(limit=5)

    cards_html = f"""
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
        overflow: hidden;
    }}

    .admin-wrap {{
        position: relative;
        padding: 10px;
    }}

    .admin-wrap::before,
    .admin-wrap::after {{
        content: "";
        position: absolute;
        width: 280px;
        height: 280px;
        border-radius: 50%;
        filter: blur(28px);
        opacity: .55;
        pointer-events: none;
        animation: driftGlow 7s ease-in-out infinite alternate;
    }}

    .admin-wrap::before {{
        left: -90px;
        top: 40px;
        background: radial-gradient(circle, rgba(0,212,255,.38), transparent 70%);
    }}

    .admin-wrap::after {{
        right: -90px;
        bottom: -90px;
        background: radial-gradient(circle, rgba(124,58,237,.42), transparent 70%);
        animation-delay: 1.2s;
    }}

    .hero {{
        position: relative;
        overflow: hidden;
        border-radius: 28px;
        padding: 32px;
        margin-bottom: 20px;
        background:
            linear-gradient(135deg, rgba(255,255,255,.14), rgba(255,255,255,.05)),
            radial-gradient(circle at 84% 24%, rgba(0,212,255,.26), transparent 30%);
        border: 1px solid rgba(0,212,255,.32);
        box-shadow:
            0 24px 75px rgba(0,212,255,.14),
            inset 0 1px 0 rgba(255,255,255,.16);
        backdrop-filter: blur(22px);
        animation: heroEnter .75s cubic-bezier(.2,.8,.2,1) both;
    }}

    .hero::before {{
        content: "";
        position: absolute;
        inset: 0;
        background:
            linear-gradient(90deg, rgba(255,255,255,.05) 1px, transparent 1px),
            linear-gradient(rgba(255,255,255,.04) 1px, transparent 1px);
        background-size: 42px 42px;
        opacity: .35;
        mask-image: radial-gradient(circle at 70% 40%, black, transparent 70%);
    }}

    .hero::after {{
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(110deg, transparent 0 34%, rgba(255,255,255,.14) 47%, transparent 60%);
        transform: translateX(-120%);
        animation: shimmer 4.6s ease-in-out infinite;
    }}

    .chip {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 13px;
        border-radius: 999px;
        color: #dff8ff;
        background: rgba(0,212,255,.12);
        border: 1px solid rgba(0,212,255,.34);
        font-size: 12px;
        font-weight: 850;
        position: relative;
        z-index: 1;
    }}

    .chip-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #22c55e;
        box-shadow: 0 0 18px #22c55e;
        animation: blinkDot 1.4s ease-in-out infinite;
    }}

    .hero h1 {{
        margin: 15px 0 8px;
        font-size: 38px;
        font-weight: 900;
        position: relative;
        z-index: 1;
    }}

    .hero p {{
        margin: 0;
        color: #a0a0c0;
        position: relative;
        z-index: 1;
        line-height: 1.6;
    }}

    .metrics {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 17px;
    }}

    .card {{
        position: relative;
        overflow: hidden;
        min-height: 196px;
        padding: 23px;
        border-radius: 26px;
        background:
            linear-gradient(145deg, rgba(255,255,255,.12), rgba(255,255,255,.055)),
            rgba(255,255,255,.06);
        border: 1px solid rgba(0,212,255,.27);
        box-shadow:
            0 18px 55px rgba(0,212,255,.10),
            inset 0 1px 0 rgba(255,255,255,.13);
        backdrop-filter: blur(22px);
        transition: transform .35s ease, border-color .35s ease, box-shadow .35s ease, background .35s ease;
        animation: cardEnter .75s cubic-bezier(.2,.8,.2,1) both;
    }}

    .card:nth-child(1) {{ animation-delay: .08s; }}
    .card:nth-child(2) {{ animation-delay: .18s; }}
    .card:nth-child(3) {{ animation-delay: .28s; }}
    .card:nth-child(4) {{ animation-delay: .38s; }}

    .card::before {{
        content: "";
        position: absolute;
        width: 210px;
        height: 210px;
        right: -82px;
        bottom: -94px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(124,58,237,.36), transparent 68%);
        transition: .35s ease;
        animation: pulseOrb 4.5s ease-in-out infinite;
    }}

    .card::after {{
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(110deg, transparent 0 40%, rgba(255,255,255,.14) 50%, transparent 62%);
        transform: translateX(-120%);
    }}

    .card:hover {{
        transform: translateY(-12px) scale(1.025);
        border-color: rgba(0,212,255,.82);
        background:
            linear-gradient(145deg, rgba(255,255,255,.16), rgba(255,255,255,.07)),
            rgba(255,255,255,.08);
        box-shadow:
            0 30px 80px rgba(0,212,255,.22),
            inset 0 1px 0 rgba(255,255,255,.18);
    }}

    .card:hover::before {{
        transform: scale(1.25);
        background: radial-gradient(circle, rgba(0,212,255,.42), transparent 68%);
    }}

    .card:hover::after {{
        animation: quickShimmer .85s ease;
    }}

    .icon {{
        width: 56px;
        height: 56px;
        display: grid;
        place-items: center;
        border-radius: 18px;
        margin-bottom: 20px;
        font-size: 26px;
        background:
            linear-gradient(135deg, rgba(0,212,255,.28), rgba(124,58,237,.28));
        border: 1px solid rgba(255,255,255,.16);
        box-shadow: 0 12px 30px rgba(0,212,255,.10);
        animation: floatIcon 3.2s ease-in-out infinite;
        position: relative;
        z-index: 1;
    }}

    .value {{
        font-size: 46px;
        line-height: 1;
        font-weight: 950;
        background: linear-gradient(135deg, #00d4ff, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        position: relative;
        z-index: 1;
    }}

    .label {{
        margin-top: 9px;
        color: white;
        font-size: 16px;
        font-weight: 850;
        position: relative;
        z-index: 1;
    }}

    .note {{
        margin-top: 5px;
        color: #a0a0c0;
        font-size: 13px;
        position: relative;
        z-index: 1;
    }}

    .mini-line {{
        position: relative;
        z-index: 1;
        height: 6px;
        margin-top: 18px;
        border-radius: 999px;
        background: rgba(255,255,255,.10);
        overflow: hidden;
    }}

    .mini-line span {{
        display: block;
        height: 100%;
        width: 68%;
        border-radius: inherit;
        background: linear-gradient(90deg, #00d4ff, #7c3aed);
        animation: lineFill 1.3s ease both .55s;
    }}

    @keyframes heroEnter {{
        from {{ opacity: 0; transform: translateY(26px) scale(.98); }}
        to {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}

    @keyframes cardEnter {{
        from {{ opacity: 0; transform: translateY(30px) scale(.96); }}
        to {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}

    @keyframes driftGlow {{
        from {{ transform: translate(0, 0) scale(1); }}
        to {{ transform: translate(26px, -18px) scale(1.12); }}
    }}

    @keyframes shimmer {{
        0%, 45% {{ transform: translateX(-120%); }}
        75%, 100% {{ transform: translateX(120%); }}
    }}

    @keyframes quickShimmer {{
        from {{ transform: translateX(-120%); }}
        to {{ transform: translateX(120%); }}
    }}

    @keyframes floatIcon {{
        0%, 100% {{ transform: translateY(0) rotate(0); }}
        50% {{ transform: translateY(-8px) rotate(2deg); }}
    }}

    @keyframes pulseOrb {{
        0%, 100% {{ opacity: .55; transform: scale(1); }}
        50% {{ opacity: .95; transform: scale(1.12); }}
    }}

    @keyframes blinkDot {{
        0%, 100% {{ opacity: .55; transform: scale(.9); }}
        50% {{ opacity: 1; transform: scale(1.15); }}
    }}

    @keyframes lineFill {{
        from {{ width: 0; }}
    }}

    @media (max-width: 900px) {{
        body {{ overflow: auto; }}
        .metrics {{ grid-template-columns: repeat(2, 1fr); }}
    }}

    @media (max-width: 520px) {{
        .metrics {{ grid-template-columns: 1fr; }}
        .hero h1 {{ font-size: 28px; }}
    }}
    </style>
    </head>
    <body>
        <div class="admin-wrap">
            <div class="hero">
                <div class="chip"><span class="chip-dot"></span> Live System Control</div>
                <h1>Admin Dashboard</h1>
                <p>Monitor users, uploads, summaries, and platform activity with a polished analytics view.</p>
            </div>

            <div class="metrics">
                <div class="card">
                    <div class="icon">👥</div>
                    <div class="value">{total_users}</div>
                    <div class="label">Total Users</div>
                    <div class="note">Registered reader accounts</div>
                    <div class="mini-line"><span></span></div>
                </div>

                <div class="card">
                    <div class="icon">✅</div>
                    <div class="value">{active_users}</div>
                    <div class="label">Active Users</div>
                    <div class="note">Currently active profiles</div>
                    <div class="mini-line"><span></span></div>
                </div>

                <div class="card">
                    <div class="icon">📚</div>
                    <div class="value">{total_books}</div>
                    <div class="label">Books Uploaded</div>
                    <div class="note">Total library content</div>
                    <div class="mini-line"><span></span></div>
                </div>

                <div class="card">
                    <div class="icon">📝</div>
                    <div class="value">{total_summaries}</div>
                    <div class="label">Summaries Generated</div>
                    <div class="note">AI summary output</div>
                    <div class="mini-line"><span></span></div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    components.html(cards_html, height=390, scrolling=False)

    col1, col2 = st.columns([1.2, 0.8], gap="large")

    with col1:
        st.markdown('<div class="admin-chart-title">Most Active Users</div>', unsafe_allow_html=True)
        st.markdown('<div class="admin-chart-subtitle">Top readers by books uploaded</div>', unsafe_allow_html=True)

        if active_users_data:
            df_users = pd.DataFrame(active_users_data)

            fig = px.bar(
                df_users,
                x="book_count",
                y="name",
                orientation="h",
                text="book_count",
                color="book_count",
                color_continuous_scale=["#00d4ff", "#7c3aed"],
                labels={"name": "", "book_count": "Books"},
            )

            fig.update_traces(
                textposition="outside",
                marker_line_color="rgba(255,255,255,.35)",
                marker_line_width=1.2,
                hovertemplate="<b>%{y}</b><br>Books uploaded: %{x}<extra></extra>",
            )

            fig.update_layout(
                template="plotly_dark",
                height=420,
                margin=dict(l=10, r=36, t=10, b=10),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", color="#dbeafe"),
                xaxis=dict(gridcolor="rgba(255,255,255,.08)", zeroline=False),
                yaxis=dict(gridcolor="rgba(255,255,255,0)", categoryorder="total ascending"),
                coloraxis_showscale=False,
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No activity data available")

    with col2:
        st.markdown('<div class="admin-chart-title">System Overview</div>', unsafe_allow_html=True)
        st.markdown('<div class="admin-chart-subtitle">Distribution of platform activity</div>', unsafe_allow_html=True)

        df_overview = pd.DataFrame({
            "Metric": ["Total Users", "Active Users", "Books Uploaded", "Summaries Generated"],
            "Count": [total_users, active_users, total_books, total_summaries],
        })

        fig2 = px.pie(
            df_overview,
            names="Metric",
            values="Count",
            hole=0.62,
            color="Metric",
            color_discrete_map={
                "Total Users": "#00d4ff",
                "Active Users": "#22c55e",
                "Books Uploaded": "#7c3aed",
                "Summaries Generated": "#f59e0b",
            },
        )

        fig2.update_traces(
            textinfo="percent",
            textfont_size=13,
            marker=dict(line=dict(color="rgba(255,255,255,.18)", width=2)),
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>",
        )

        fig2.update_layout(
            template="plotly_dark",
            height=420,
            margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color="#dbeafe"),
            legend=dict(orientation="h", y=-0.12, x=0.5, xanchor="center"),
            annotations=[
                dict(
                    text="System<br>Health",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(size=16, color="#ffffff"),
                )
            ],
        )

        st.plotly_chart(fig2, use_container_width=True)

    note_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    body {
        margin: 0;
        background: transparent;
        color: #c7eaff;
        font-family: Inter, Arial, sans-serif;
    }

    .note {
        position: relative;
        overflow: hidden;
        margin: 8px;
        padding: 22px;
        border-radius: 22px;
        background: rgba(255,255,255,.08);
        border: 1px solid rgba(0,212,255,.25);
        box-shadow: 0 18px 55px rgba(0,212,255,.10);
        backdrop-filter: blur(20px);
    }

    .note::before {
        content: "";
        position: absolute;
        width: 220px;
        height: 220px;
        right: -90px;
        top: -110px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(124,58,237,.30), transparent 70%);
        animation: noteGlow 4s ease-in-out infinite;
    }

    .note strong {
        color: #00d4ff;
    }

    @keyframes noteGlow {
        0%, 100% { opacity: .55; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.16); }
    }
    </style>
    </head>
    <body>
        <div class="note">
            <strong>Real-Time Analytics</strong><br>
            This dashboard uses live database values. Metrics and charts update as users upload books and generate summaries.
        </div>
    </body>
    </html>
    """

    components.html(note_html, height=105, scrolling=False)
