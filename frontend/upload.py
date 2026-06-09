from datetime import datetime
import streamlit as st
from docx import Document
import PyPDF2

from utils.full_summary import summarize_large_text
from utils.pdf_export import generate_pdf
from utils.database import (
    create_book,
    save_summary,
    update_book_status
)

MAX_FILE_SIZE_MB = 10
from utils.error_handling import safe_ai_call 

# ---------- ENHANCED UPLOAD STYLING ----------
st.markdown("""
<style>
.upload-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
}

.upload-header {
    text-align: center;
    margin-bottom: 3rem;
}

.upload-header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.upload-header p {
    color: #a0a0c0;
    font-size: 1.1rem;
}

.upload-card {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(20px);
    border: 1.5px solid rgba(0, 212, 255, 0.3);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 2rem;
    transition: all 0.3s ease;
}

.upload-card:hover {
    border-color: rgba(0, 212, 255, 0.6);
    background: rgba(255, 255, 255, 0.12);
}

.upload-section-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #00d4ff;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
}

.upload-item {
    background: rgba(0, 212, 255, 0.05);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.summary-preview {
    background: rgba(255, 255, 255, 0.05);
    border-left: 4px solid #00d4ff;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1rem 0;
}

.success-badge {
    display: inline-block;
    background: rgba(0, 212, 100, 0.2);
    border: 1px solid rgba(0, 212, 100, 0.4);
    color: #00ff88;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.9rem;
}

.info-box {
    background: rgba(0, 170, 255, 0.1);
    border-left: 4px solid #00aaff;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    color: #88ccff;
}
</style>
""", unsafe_allow_html=True)

# ---------- TEXT EXTRACTORS ----------
def extract_text_from_txt(file):
    return file.getvalue().decode("utf-8", errors="ignore")


def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text


def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join(p.text for p in doc.paragraphs)


# ---------- UPLOAD PAGE ----------
def show_upload_page(user_id):

    if not user_id:
        st.error("Please logout and login again")
        return

    st.markdown('<div class="upload-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="upload-header">
        <h1>📤 Upload & Summarize</h1>
        <p>Upload your book and let AI generate intelligent summaries</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="upload-card">', unsafe_allow_html=True)
        st.markdown('<div class="upload-section-title">📎 Upload File</div>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose TXT, PDF, or DOCX file (Max 10 MB)",
            type=["txt", "pdf", "docx"],
            label_visibility="collapsed"
        )
        
        st.markdown('<div class="info-box">📌 Supported formats: TXT, PDF, DOCX</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="upload-card">', unsafe_allow_html=True)
        st.markdown('<div class="upload-section-title">📖 Book Details</div>', unsafe_allow_html=True)
        
        title = st.text_input("📘 Book Title", placeholder="Enter book title", label_visibility="collapsed")
        author = st.text_input("✍️ Author (optional)", placeholder="Author name", label_visibility="collapsed")
        summary_type = st.selectbox(
            "📝 Summary Type",
            ["Comprehensive", "Concise", "Detailed", "Quick Overview"],
            label_visibility="collapsed"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)

    extracted_text = None

    # ---------- FILE VALIDATION & PREVIEW ----------
    if uploaded_file:
        st.markdown('<div class="upload-card">', unsafe_allow_html=True)
        st.markdown('<div class="upload-section-title">✓ File Preview</div>', unsafe_allow_html=True)

        file_size_mb = uploaded_file.size / (1024 * 1024)

        if file_size_mb > MAX_FILE_SIZE_MB:
            st.error(f"❌ File size must be less than 10 MB (Uploaded: {file_size_mb:.2f} MB)")
        else:
            try:
                if uploaded_file.name.endswith(".txt"):
                    extracted_text = extract_text_from_txt(uploaded_file)
                elif uploaded_file.name.endswith(".pdf"):
                    extracted_text = extract_text_from_pdf(uploaded_file)
                elif uploaded_file.name.endswith(".docx"):
                    extracted_text = extract_text_from_docx(uploaded_file)

                # Show file info
                success_text = f"<span class='success-badge'>✅ {uploaded_file.name} ({file_size_mb:.2f} MB)</span>"
                st.markdown(success_text, unsafe_allow_html=True)

                # Show preview
                st.markdown("""
                <div style="margin-top: 1rem; font-size: 0.95rem; color: #888;">
                    📄 File preview (first 500 characters):
                </div>
                """, unsafe_allow_html=True)
                st.text_area(
                    "Preview",
                    extracted_text[:500] + "...",
                    height=150,
                    disabled=True,
                    label_visibility="collapsed"
                )

            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------- GENERATE SUMMARY ----------
    st.markdown('<div class="upload-card" style="text-align: center;">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_btn = st.button("🚀 Generate Summary", use_container_width=True, key="gen_summary")

    st.markdown('</div>', unsafe_allow_html=True)

    if generate_btn:
        if not uploaded_file or not title or not extracted_text:
            st.error("⚠️ Please upload a file and enter the book title")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()

            with st.spinner("🤖 AI is analyzing your book..."):
                status_text.markdown("**Processing:** Extracting text...")
                progress_bar.progress(25)
                
                status_text.markdown("**Processing:** Generating summary...")
                progress_bar.progress(50)
                
                summary = safe_ai_call(summarize_large_text, extracted_text)
                progress_bar.progress(75)

                # Save to database
                status_text.markdown("**Processing:** Saving to database...")
                book_id = create_book(
                    user_id=user_id,
                    title=title,
                    text=extracted_text,
                    author=author
                )
                save_summary(book_id, user_id, summary)
                update_book_status(book_id, "summarized")
                
                progress_bar.progress(100)
                status_text.markdown("**✅ Complete!**")

            st.balloons()

            # Display summary
            st.markdown("""
            <div style="margin-top: 2rem;">
                <div class="upload-card">
                    <div class="upload-section-title">📑 Generated Summary</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="summary-preview">', unsafe_allow_html=True)
            st.text_area("Summary", summary, height=350, disabled=True, label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)

            # Download options
            st.markdown("""
            <div class="upload-card">
                <div class="upload-section-title">📥 Download Options</div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            txt_content = f"""Title: {title}
Author: {author if author else 'N/A'}
Date: {datetime.now().strftime('%d-%m-%Y')}
Summary Type: {summary_type}

Summary:
{summary}
"""

            with col1:
                st.download_button(
                    "⬇️ TXT Format",
                    txt_content,
                    file_name=f"{title.replace(' ', '_')}_summary.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            with col2:
                pdf_path = generate_pdf(title, author, summary)
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        "⬇️ PDF Format",
                        pdf_file,
                        file_name=f"{title.replace(' ', '_')}_summary.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

            with col3:
                st.download_button(
                    "📋 Copy Text",
                    summary,
                    file_name=f"{title.replace(' ', '_')}_summary_text.txt",
                    mime="text/plain",
                    use_container_width=True
                )

    st.markdown('</div>', unsafe_allow_html=True)