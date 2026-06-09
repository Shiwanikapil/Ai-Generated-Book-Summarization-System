import streamlit as st
from datetime import datetime
from utils.database import (
    get_books,
    delete_book,
    get_all_summaries,
    set_favorite_summary,
    set_default_summary
)
from utils.diff_utils import highlight_diff  

# ---------- ENHANCED HISTORY STYLING ----------
st.markdown("""
<style>
.history-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
}

.history-header {
    text-align: center;
    margin-bottom: 3rem;
}

.book-card-history {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(20px);
    border: 1.5px solid rgba(0, 212, 255, 0.3);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 2rem;
    transition: all 0.3s ease;
}

.book-card-history:hover {
    border-color: rgba(0, 212, 255, 0.6);
    background: rgba(255, 255, 255, 0.12);
    box-shadow: 0 15px 40px rgba(0, 212, 255, 0.15);
}

.book-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}

.book-title-history {
    font-size: 1.5rem;
    font-weight: 700;
    color: #00d4ff;
}

.quick-actions {
    display: flex;
    gap: 0.5rem;
}

.action-btn {
    background: rgba(0, 212, 255, 0.2);
    border: 1px solid rgba(0, 212, 255, 0.3);
    color: #00d4ff;
    padding: 8px 12px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1.1rem;
    transition: all 0.3s ease;
    text-align: center;
}

.action-btn:hover {
    background: rgba(0, 212, 255, 0.4);
    border-color: rgba(0, 212, 255, 0.6);
}

.book-metadata {
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(0, 212, 255, 0.2);
}

.metadata-item {
    font-size: 0.95rem;
    color: #a0a0c0;
}

.metadata-label {
    color: #888;
    margin-right: 0.3rem;
}

.summary-text {
    background: rgba(0, 212, 255, 0.05);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    color: #e0e0e0;
    line-height: 1.6;
    max-height: 400px;
    overflow-y: auto;
}

.action-buttons {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
    flex-wrap: wrap;
}

.version-viewer {
    background: rgba(255, 255, 255, 0.08);
    border: 1.5px solid rgba(0, 212, 255, 0.3);
    border-radius: 16px;
    padding: 2rem;
    margin-top: 2rem;
}

.version-item {
    background: rgba(0, 212, 255, 0.05);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

.empty-state-history {
    text-align: center;
    padding: 4rem 2rem;
    color: #888;
}

.empty-state-history-icon {
    font-size: 3.5rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)


# ================= SUMMARY VERSION VIEW =================
def show_summary_versions(book_id):
    st.markdown('<div class="version-viewer">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #00d4ff; margin-top: 0;">📜 Summary Versions</h2>', unsafe_allow_html=True)

    summaries = get_all_summaries(book_id)
    if not summaries:
        st.info("No summaries found")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # ---------- SHOW ALL VERSIONS ----------
    for i, s in enumerate(summaries):
        version_num = len(summaries) - i
        st.markdown(f"""
        <div class="version-item">
            <h3 style="color: #00d4ff; margin-top: 0;">📝 Version {version_num}</h3>
        </div>
        """, unsafe_allow_html=True)
        st.text_area(
            f"Version {version_num}",
            s["summary_text"],
            height=250,
            disabled=True,
            label_visibility="collapsed"
        )
        st.divider()

    # ---------- COMPARE LATEST TWO ----------
    if len(summaries) >= 2:
        st.markdown('<h3 style="color: #00d4ff;">🔍 Compare Latest Versions</h3>', unsafe_allow_html=True)

        diff_text = highlight_diff(
            summaries[1]["summary_text"],   # older
            summaries[0]["summary_text"]    # latest
        )

        st.text_area("Differences", diff_text, height=300, disabled=True, label_visibility="collapsed")

    st.markdown('</div>', unsafe_allow_html=True)


# ================= HISTORY PAGE =================
def show_history_page(user_id):
    st.markdown('<div class="history-container">', unsafe_allow_html=True)

    st.markdown("""
    <div class="history-header">
        <h1>📚 Your History</h1>
        <p>Manage and review all your book summaries</p>
    </div>
    """, unsafe_allow_html=True)

    books = get_books(user_id)
    if not books:
        st.markdown("""
        <div class="empty-state-history">
            <div class="empty-state-history-icon">📚</div>
            <p style="font-size: 1.1rem;">No uploads yet</p>
            <p style="color: #666;">Start uploading books to build your library</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    for book in books:
        st.markdown('<div class="book-card-history">', unsafe_allow_html=True)

        # Header with title and quick actions
        col1, col2 = st.columns([4, 1], gap="small")
        
        with col1:
            st.markdown(f'<div class="book-title-history">📘 {book["title"]}</div>', unsafe_allow_html=True)
        
        with col2:
            if st.button("🗑️ Delete", key=f"del_{book['_id']}", use_container_width=True):
                delete_book(book["_id"], user_id)
                st.success("✅ Book & summaries deleted")
                st.rerun()

        summaries = get_all_summaries(book["_id"])
        if not summaries:
            st.info("📌 No summaries generated yet")
            st.markdown('</div>', unsafe_allow_html=True)
            continue

        # ---------- PICK DEFAULT OR LATEST ----------
        default_summary = next(
            (s for s in summaries if s.get("is_default")),
            summaries[0]
        )

        # Metadata
        st.markdown(f"""
        <div class="book-metadata">
            <div class="metadata-item">
                <span class="metadata-label">✍️ Author:</span>
                <strong>{book.get('author', 'N/A')}</strong>
            </div>
            <div class="metadata-item">
                <span class="metadata-label">📌 Status:</span>
                <strong style="color: #00d4ff;">{book.get('status', 'uploaded').upper()}</strong>
            </div>
            <div class="metadata-item">
                <span class="metadata-label">📅 Uploaded:</span>
                <strong>{book.get('created_at', 'N/A')}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Show summary
        st.markdown('<h3 style="color: #00d4ff; margin-top: 0;">📝 Current Summary</h3>', unsafe_allow_html=True)
        st.markdown('<div class="summary-text">', unsafe_allow_html=True)
        st.markdown(default_summary["summary_text"])
        st.markdown('</div>', unsafe_allow_html=True)

        # Download and action buttons
        st.markdown('<div class="action-buttons">', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            txt_content = f"""Title: {book['title']}
Author: {book.get('author', 'N/A')}
Date: {datetime.now().strftime('%d-%m-%Y')}

Summary:
{default_summary["summary_text"]}
"""
            st.download_button(
                "⬇️ Download",
                txt_content,
                file_name=f"{book['title'].replace(' ', '_')}_summary.txt",
                mime="text/plain",
                key=f"txt_{book['_id']}",
                use_container_width=True
            )

        with col2:
            fav_label = "⭐ Favorite" if not default_summary.get("is_favorite") else "✅ Favorited"
            if st.button(fav_label, key=f"fav_{default_summary['_id']}", use_container_width=True):
                set_favorite_summary(default_summary["_id"], book["_id"])
                st.success("⭐ Marked as favorite")
                st.rerun()

        with col3:
            def_label = "🏷️ Default" if not default_summary.get("is_default") else "✅ Default"
            if st.button(def_label, key=f"def_{default_summary['_id']}", use_container_width=True):
                set_default_summary(default_summary["_id"], book["_id"])
                st.success("🏷️ Set as default")
                st.rerun()

        with col4:
            if st.button("🔁 Versions", key=f"versions_{book['_id']}", use_container_width=True):
                st.session_state["show_versions_for"] = book["_id"]

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------- VERSION PANEL ----------
    if st.session_state.get("show_versions_for"):
        show_summary_versions(st.session_state["show_versions_for"])

    st.markdown('</div>', unsafe_allow_html=True)