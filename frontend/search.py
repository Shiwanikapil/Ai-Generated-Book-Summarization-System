import streamlit as st
from utils.database import search_books

# ---------- ENHANCED SEARCH STYLING ----------
st.markdown("""
<style>
.search-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
}

.search-header {
    text-align: center;
    margin-bottom: 3rem;
}

.search-filters {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(20px);
    border: 1.5px solid rgba(0, 212, 255, 0.3);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 2rem;
}

.search-results-container {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(20px);
    border: 1.5px solid rgba(0, 212, 255, 0.3);
    border-radius: 20px;
    padding: 2rem;
}

.search-result-item {
    background: rgba(0, 212, 255, 0.05);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;
}

.search-result-item:hover {
    background: rgba(0, 212, 255, 0.1);
    border-color: rgba(0, 212, 255, 0.5);
    box-shadow: 0 10px 30px rgba(0, 212, 255, 0.15);
    transform: translateY(-4px);
}

.result-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #00d4ff;
    margin-bottom: 1rem;
}

.result-meta {
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
    margin-bottom: 1rem;
    font-size: 0.95rem;
    color: #a0a0c0;
}

.result-meta-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.result-status {
    display: inline-block;
    background: rgba(0, 212, 100, 0.2);
    border: 1px solid rgba(0, 212, 100, 0.4);
    color: #00ff88;
    padding: 6px 12px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.9rem;
}

.no-results {
    text-align: center;
    padding: 3rem;
    color: #888;
}

.no-results-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.results-count {
    background: rgba(0, 212, 255, 0.1);
    border: 1px solid rgba(0, 212, 255, 0.3);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1.5rem;
    color: #00d4ff;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

def show_search_page(user_id):
    st.markdown('<div class="search-container">', unsafe_allow_html=True)

    st.markdown("""
    <div class="search-header">
        <h1>🔍 Search Books</h1>
        <p>Find your books with advanced filters</p>
    </div>
    """, unsafe_allow_html=True)

    # ---------- SEARCH FILTERS ----------
    st.markdown('<div class="search-filters">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #00d4ff; margin-top: 0;">Filter & Search</h2>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1], gap="large")

    with col1:
        title = st.text_input(
            "📘 Book Title",
            placeholder="Search by book title...",
            label_visibility="collapsed"
        )

    with col2:
        status = st.selectbox(
            "📌 Status",
            ["All", "uploaded", "summarized"],
            label_visibility="collapsed"
        )

    with col3:
        search_btn = st.button("🔎 Search", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- SEARCH RESULTS ----------
    if search_btn or title or (status != "All"):
        st.markdown('<div class="search-results-container">', unsafe_allow_html=True)

        results = search_books(
            user_id=user_id,
            title=title if title else None,
            status=status if status != "All" else None
        )

        if not results:
            st.markdown("""
            <div class="no-results">
                <div class="no-results-icon">🔍</div>
                <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">No books found</p>
                <p style="color: #666;">Try adjusting your search filters</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="results-count">
                ✓ Found {len(results)} book{'s' if len(results) != 1 else ''}
            </div>
            """, unsafe_allow_html=True)

            for i, book in enumerate(results):
                st.markdown(f"""
                <div class="search-result-item">
                    <div class="result-title">📘 {book['title']}</div>
                    <div class="result-meta">
                        <div class="result-meta-item">✍️ Author: <strong>{book.get('author', 'N/A')}</strong></div>
                        <div class="result-meta-item">
                            <span class="result-status">{book.get('status', 'uploaded').upper()}</span>
                        </div>
                    </div>
                    <small style="color: #888;">ID: {str(book.get('_id', 'N/A'))[:20]}...</small>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
