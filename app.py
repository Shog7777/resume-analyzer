import streamlit as st
import os
from utils.parser import extract_text_from_pdf, extract_text_from_docx
from utils.analyzer import analyze_match

st.set_page_config(
    page_title="Resume Analyzer | ATS Matcher",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .stApp {
        background: #0f1117;
        color: #e8eaf0;
    }

    .main-header {
        text-align: center;
        padding: 3rem 0 2rem;
    }

    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6ee7f7, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }

    .main-header p {
        color: #8892a4;
        font-size: 1.1rem;
        font-weight: 300;
    }

    .score-ring-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem 0;
    }

    .score-card {
        background: #1a1d2e;
        border: 1px solid #2d3148;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }

    .score-number {
        font-size: 5rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        line-height: 1;
    }

    .score-label {
        font-size: 0.85rem;
        color: #8892a4;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 0.5rem;
    }

    .metric-card {
        background: #1a1d2e;
        border: 1px solid #2d3148;
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }

    .metric-title {
        font-size: 0.8rem;
        color: #8892a4;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 0.6rem;
    }

    .progress-bar-bg {
        background: #2d3148;
        border-radius: 8px;
        height: 8px;
        overflow: hidden;
        margin-top: 0.5rem;
    }

    .keyword-chip {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.2rem;
        font-weight: 500;
    }

    .chip-match {
        background: #0d2e1f;
        color: #4ade80;
        border: 1px solid #166534;
    }

    .chip-missing {
        background: #2d1515;
        color: #f87171;
        border: 1px solid #7f1d1d;
    }

    .section-header {
        font-size: 1rem;
        font-weight: 600;
        color: #c4cadb;
        margin: 1.5rem 0 0.8rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid #2d3148;
    }

    .stTextArea textarea {
        background: #1a1d2e !important;
        color: #e8eaf0 !important;
        border: 1px solid #2d3148 !important;
        border-radius: 10px !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stTextArea textarea:focus {
        border-color: #6ee7f7 !important;
        box-shadow: 0 0 0 2px rgba(110, 231, 247, 0.1) !important;
    }

    .stFileUploader {
        border: 2px dashed #2d3148 !important;
        border-radius: 14px !important;
        background: #1a1d2e !important;
    }

    div[data-testid="stFileUploader"] > div {
        background: #1a1d2e;
        border: 2px dashed #2d3148;
        border-radius: 14px;
        padding: 1.5rem;
    }

    .stButton > button {
        background: linear-gradient(135deg, #6ee7f7, #a78bfa) !important;
        color: #0f1117 !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 2rem !important;
        font-size: 1rem !important;
        width: 100% !important;
        transition: opacity 0.2s !important;
    }

    .stButton > button:hover {
        opacity: 0.9 !important;
    }

    .suggestion-item {
        background: #1a1d2e;
        border-left: 3px solid #a78bfa;
        border-radius: 0 10px 10px 0;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
        font-size: 0.9rem;
        color: #c4cadb;
    }

    div[data-testid="column"] { padding: 0 0.5rem; }

    .stAlert { border-radius: 12px !important; }

    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎯 Resume Analyzer</h1>
    <p>Upload your resume and paste the job description — get an ATS match score instantly</p>
</div>
""", unsafe_allow_html=True)

# Input Section
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-header">📄 Your Resume</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload PDF or DOCX",
        type=["pdf", "docx"],
        label_visibility="collapsed"
    )
    if uploaded_file:
        st.success(f"✅ Loaded: {uploaded_file.name}")

    resume_text_input = st.text_area(
        "Or paste resume text",
        height=200,
        placeholder="Paste your resume content here...",
        label_visibility="collapsed"
    )

with col2:
    st.markdown('<div class="section-header">💼 Job Description</div>', unsafe_allow_html=True)
    job_description = st.text_area(
        "Job description",
        height=320,
        placeholder="Paste the full job description here...",
        label_visibility="collapsed"
    )

st.markdown("<br>", unsafe_allow_html=True)
_, center_col, _ = st.columns([1, 2, 1])
with center_col:
    analyze_btn = st.button("⚡ Analyze Match", use_container_width=True)

# Analysis
if analyze_btn:
    resume_text = ""

    if uploaded_file:
        with st.spinner("Reading your resume..."):
            if uploaded_file.name.endswith(".pdf"):
                resume_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.name.endswith(".docx"):
                resume_text = extract_text_from_docx(uploaded_file)
    elif resume_text_input.strip():
        resume_text = resume_text_input.strip()

    if not resume_text:
        st.error("⚠️ Please upload a resume or paste resume text.")
    elif not job_description.strip():
        st.error("⚠️ Please paste the job description.")
    else:
        with st.spinner("🔍 Analyzing with AI..."):
            results = analyze_match(resume_text, job_description)

        if results:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("---")

            # Score color
            score = results.get("overall_score", 0)
            if score >= 75:
                score_color = "#4ade80"
                verdict = "Strong Match ✅"
            elif score >= 50:
                score_color = "#fbbf24"
                verdict = "Moderate Match ⚠️"
            else:
                score_color = "#f87171"
                verdict = "Weak Match ❌"

            # Score display
            st.markdown(f"""
            <div style="text-align:center; padding: 2rem 0;">
                <div style="display:inline-block; background:#1a1d2e; border:2px solid {score_color}33;
                     border-radius:20px; padding:2rem 3rem;">
                    <div class="score-number" style="color:{score_color}">{score}%</div>
                    <div style="color:{score_color}; font-weight:600; margin-top:0.5rem; font-size:1.1rem">{verdict}</div>
                    <div class="score-label">ATS Match Score</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Metrics
            c1, c2, c3 = st.columns(3)
            metrics = [
                ("Skills Match", results.get("skills_score", 0), c1),
                ("Experience Fit", results.get("experience_score", 0), c2),
                ("Keywords Match", results.get("keywords_score", 0), c3),
            ]
            for title, val, col in metrics:
                bar_color = "#4ade80" if val >= 75 else "#fbbf24" if val >= 50 else "#f87171"
                with col:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">{title}</div>
                        <div style="font-size:1.8rem; font-weight:700; color:{bar_color}; font-family:'JetBrains Mono',monospace">{val}%</div>
                        <div class="progress-bar-bg">
                            <div style="height:100%; width:{val}%; background:{bar_color}; border-radius:8px; transition:width 1s ease"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # Keywords
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown('<div class="section-header">✅ Matched Keywords</div>', unsafe_allow_html=True)
                matched = results.get("matched_keywords", [])
                if matched:
                    chips = "".join([f'<span class="keyword-chip chip-match">{k}</span>' for k in matched])
                    st.markdown(f'<div>{chips}</div>', unsafe_allow_html=True)
                else:
                    st.info("No matched keywords found.")

            with col_b:
                st.markdown('<div class="section-header">❌ Missing Keywords</div>', unsafe_allow_html=True)
                missing = results.get("missing_keywords", [])
                if missing:
                    chips = "".join([f'<span class="keyword-chip chip-missing">{k}</span>' for k in missing])
                    st.markdown(f'<div>{chips}</div>', unsafe_allow_html=True)
                else:
                    st.success("No missing critical keywords!")

            # Suggestions
            suggestions = results.get("suggestions", [])
            if suggestions:
                st.markdown('<div class="section-header">💡 Improvement Suggestions</div>', unsafe_allow_html=True)
                for s in suggestions:
                    st.markdown(f'<div class="suggestion-item">→ {s}</div>', unsafe_allow_html=True)

            # Summary
            summary = results.get("summary", "")
            if summary:
                st.markdown('<div class="section-header">📊 Analysis Summary</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-card" style="color:#c4cadb; line-height:1.7">{summary}</div>', unsafe_allow_html=True)
