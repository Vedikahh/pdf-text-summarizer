import streamlit as st

from utils.pdf_reader import extract_text_from_pdf
from utils.preprocess import clean_text, get_sentences, get_filtered_words
from utils.extractive import summarize_extractive
from utils.metrics import compute_stats
from utils.exporter import build_txt, build_pdf
from utils.keywords import extract_keywords

try:
    from utils.abstractive import summarize_abstractive
    ABSTRACTIVE_AVAILABLE = True
except ImportError:
    ABSTRACTIVE_AVAILABLE = False


st.set_page_config(
    page_title="Content Summarizer",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# THEME
# ---------------------------------------------------------------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

ACCENT = "#EC4899"
ACCENT_HOVER = "#DB2777"
ACCENT_TINT = "rgba(236, 72, 153, 0.12)"

if st.session_state.dark_mode:
    BG = "#0F0F13"
    PANEL_BG = "#1A1A20"
    BORDER = "#2C2C34"
    TEXT_MAIN = "#F2F2F5"
    TEXT_MUTED = "#9A9AA6"
else:
    BG = "#FFFFFF"
    PANEL_BG = "#FAF7F8"
    BORDER = "#EEE6EA"
    TEXT_MAIN = "#1C1C22"
    TEXT_MUTED = "#84848F"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

    html, body, .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stMain"],
    [data-testid="stBottomBlockContainer"] {{
        background-color: {BG} !important;
        color: {TEXT_MAIN};
    }}
    #MainMenu, footer {{ visibility: hidden; }}
    [data-testid="stToolbar"] {{ visibility: hidden; }}
    [data-testid="stDecoration"] {{ display: none; }}

    .page-title {{ font-size: 1.5rem; font-weight: 700; margin-bottom: 0.15rem; color: {TEXT_MAIN}; }}
    .page-subtitle {{ color: {TEXT_MUTED}; font-size: 0.9rem; margin-bottom: 1.25rem; }}

    /* Real Streamlit bordered containers — this is what actually wraps our panels now */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: {PANEL_BG} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 12px !important;
    }}
    [data-testid="stVerticalBlockBorderWrapper"] > div {{ padding: 0.25rem; }}

    .field-label {{
        font-size: 0.78rem; font-weight: 600; color: {TEXT_MUTED};
        margin: 0.9rem 0 0.35rem 0; text-transform: uppercase; letter-spacing: 0.03em;
    }}

    div[data-testid="stFileUploaderDropzone"] {{
        background-color: {BG} !important;
        border: 1.5px dashed {BORDER} !important;
        border-radius: 10px;
    }}
    div[data-testid="stFileUploaderDropzone"] * {{
        color: {TEXT_MAIN} !important;
        fill: {TEXT_MAIN} !important;
    }}
    div[data-testid="stFileUploaderDropzone"] button {{
        background-color: {PANEL_BG} !important;
        border: 1px solid {BORDER} !important;
        color: {TEXT_MAIN} !important;
    }}
    div[data-testid="stFileUploaderDropzone"]:hover {{ border-color: {ACCENT}; }}

    /* Uploaded-file preview chip is a separate internal component — style it explicitly.
       Cast a wide net since the exact internal DOM/testid can differ by Streamlit version. */
    [data-testid="stFileUploaderFile"],
    [data-testid="stFileUploaderFile"] > div,
    [data-testid="stFileUploaderFile"] > div > div,
    section[data-testid="stFileUploader"] li,
    section[data-testid="stFileUploader"] ul {{
        background-color: {PANEL_BG} !important;
        border-radius: 8px;
    }}
    [data-testid="stFileUploaderFile"] {{
        border: 1px solid {BORDER} !important;
    }}
    [data-testid="stFileUploaderFile"] *,
    section[data-testid="stFileUploader"] li * {{
        color: {TEXT_MAIN} !important;
        fill: {TEXT_MAIN} !important;
    }}
    [data-testid="stFileUploaderFileName"] {{ color: {TEXT_MAIN} !important; }}
    [data-testid="stFileUploaderDeleteBtn"] svg {{ fill: {TEXT_MUTED} !important; }}
    small {{ color: {TEXT_MUTED} !important; }}

    button[data-baseweb="tab"] {{ font-weight: 600; color: {TEXT_MUTED}; }}
    button[data-baseweb="tab"][aria-selected="true"] {{ color: {TEXT_MAIN}; }}
    div[data-baseweb="tab-highlight"] {{ background-color: {ACCENT}; height: 2.5px; }}

    div.stButton > button, div.stDownloadButton > button {{
        background-color: {ACCENT};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.4rem;
        font-weight: 600;
        transition: background-color 0.15s ease;
    }}
    div.stButton > button:hover, div.stDownloadButton > button:hover {{
        background-color: {ACCENT_HOVER}; color: white;
    }}
    div.stButton > button[kind="secondary"] {{
        background-color: {BG}; color: {TEXT_MAIN}; border: 1px solid {BORDER};
    }}
    div.stButton > button[kind="secondary"]:hover {{ background-color: {PANEL_BG}; }}

    .summary-header {{ font-weight: 700; font-size: 1rem; margin-bottom: 0.75rem; color: {TEXT_MAIN}; }}
    .summary-body {{ color: {TEXT_MAIN}; line-height: 1.65; font-size: 0.94rem; }}

    .compare-col-title {{
        font-weight: 700; font-size: 0.9rem; margin-bottom: 0.5rem;
        padding-bottom: 0.4rem; border-bottom: 2px solid {BORDER};
        color: {TEXT_MAIN};
    }}

    .stat-row {{ display: flex; gap: 0.7rem; margin-top: 1rem; }}
    .stat-pill {{
        flex: 1; background-color: {BG};
        border: 1px solid {BORDER}; border-radius: 10px;
        padding: 0.65rem 0.85rem; text-align: center;
    }}
    .stat-pill .num {{ font-weight: 700; font-size: 1.1rem; color: {TEXT_MAIN}; }}
    .stat-pill .label {{ font-size: 0.72rem; color: {TEXT_MUTED}; }}

    table.comparison-table {{
        width: 100%; border-collapse: collapse; margin-top: 1rem; font-size: 0.87rem; color: {TEXT_MAIN};
    }}
    table.comparison-table th, table.comparison-table td {{
        border: 1px solid {BORDER};
        padding: 0.45rem 0.75rem;
        text-align: center;
    }}
    table.comparison-table th {{ background-color: {BG}; font-weight: 600; }}
    table.comparison-table td:first-child, table.comparison-table th:first-child {{
        text-align: left; font-weight: 500;
    }}

    .keyword-row {{ display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.6rem; }}
    .keyword-chip {{
        background-color: {ACCENT_TINT};
        color: {ACCENT};
        border: 1px solid {ACCENT};
        border-radius: 999px;
        padding: 0.22rem 0.7rem;
        font-size: 0.78rem;
        font-weight: 600;
    }}
    .section-label {{
        font-size: 0.78rem; font-weight: 600; color: {TEXT_MUTED};
        margin-top: 1.1rem; text-transform: uppercase; letter-spacing: 0.03em;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# HEADER (title + subtitle, with a sun/moon icon toggle top-right)
# ---------------------------------------------------------------------------
head_left, head_right = st.columns([6, 1])
with head_left:
    st.markdown('<div class="page-title">Content Summarizer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Extractive &amp; abstractive NLP summarization, with keyword extraction.</div>',
        unsafe_allow_html=True,
    )
with head_right:
    sun_col, moon_col = st.columns(2)
    with sun_col:
        if st.button(" ", icon=":material/light_mode:", use_container_width=True,
                      type="primary" if not st.session_state.dark_mode else "secondary"):
            st.session_state.dark_mode = False
            st.rerun()
    with moon_col:
        if st.button(" ", icon=":material/dark_mode:", use_container_width=True,
                      type="primary" if st.session_state.dark_mode else "secondary"):
            st.session_state.dark_mode = True
            st.rerun()

# ---------------------------------------------------------------------------
# INPUT PANEL
# ---------------------------------------------------------------------------
left, right = st.columns([1.1, 1], gap="large")

with left:
    with st.container(border=True):
        tabs = st.tabs(["PDF", "Text"])
        uploaded_file = None
        pasted_text = ""

        with tabs[0]:
            uploaded_file = st.file_uploader(
                "Upload PDF File", type=["pdf"],
                help="File must be in PDF format and under 10MB.",
            )
        with tabs[1]:
            pasted_text = st.text_area(
                "Paste your text here", height=180,
                placeholder="Paste an article, report, or any text you'd like summarized...",
            )

        st.markdown('<div class="field-label">Summary length</div>', unsafe_allow_html=True)
        ratio = st.slider(
            "Summary length", min_value=10, max_value=50, value=30, step=5, format="%d%%",
            label_visibility="collapsed",
        )

        st.markdown('<div class="field-label">Summary type</div>', unsafe_allow_html=True)
        mode_options = ["Extractive"]
        if ABSTRACTIVE_AVAILABLE:
            mode_options += ["Abstractive", "Both (Compare)"]
        summary_mode = st.radio(
            "Summary type", mode_options, horizontal=True, label_visibility="collapsed",
        )

        col_a, col_b = st.columns([1, 1])
        with col_a:
            clear_clicked = st.button("Clear", use_container_width=True, type="secondary")
        with col_b:
            summarize_clicked = st.button("Summarize", use_container_width=True, type="primary")

# ---------------------------------------------------------------------------
# SUMMARIZE LOGIC
# ---------------------------------------------------------------------------
if clear_clicked:
    st.session_state.pop("results", None)

if summarize_clicked:
    raw_text = ""
    if uploaded_file is not None:
        raw_text = extract_text_from_pdf(uploaded_file)
    elif pasted_text.strip():
        raw_text = pasted_text

    if not raw_text.strip():
        st.session_state["results"] = {"error": "Upload a PDF or paste some text first."}
    else:
        cleaned = clean_text(raw_text)
        results = {"original": cleaned, "keywords": extract_keywords(cleaned, top_n=10)}

        if summary_mode in ("Extractive", "Both (Compare)"):
            results["extractive"], _ = summarize_extractive(cleaned, summary_ratio=ratio / 100)

        if summary_mode in ("Abstractive", "Both (Compare)") and ABSTRACTIVE_AVAILABLE:
            with st.spinner("Generating abstractive summary — this can take up to a minute on CPU..."):
                results["abstractive"] = summarize_abstractive(cleaned)

        st.session_state["results"] = results

# ---------------------------------------------------------------------------
# OUTPUT PANEL
# ---------------------------------------------------------------------------
with right:
    with st.container(border=True):
        st.markdown('<div class="summary-header">Summary</div>', unsafe_allow_html=True)

        results = st.session_state.get("results")

        if not results:
            st.markdown(
                f'<span style="color:{TEXT_MUTED};">Your summary will appear here once you upload a file or paste text and click Summarize.</span>',
                unsafe_allow_html=True,
            )
        elif "error" in results:
            st.warning(results["error"])
        else:
            original = results["original"]
            has_extractive = "extractive" in results
            has_abstractive = "abstractive" in results

            if has_extractive and has_abstractive:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('<div class="compare-col-title">Extractive</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="summary-body">{results["extractive"]}</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown('<div class="compare-col-title">Abstractive</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="summary-body">{results["abstractive"]}</div>', unsafe_allow_html=True)

                ext_stats = compute_stats(original, results["extractive"])
                abs_stats = compute_stats(original, results["abstractive"])

                st.markdown(
                    f"""
                    <table class="comparison-table">
                        <tr><th>Metric</th><th>Original</th><th>Extractive</th><th>Abstractive</th></tr>
                        <tr><td>Words</td><td>{ext_stats['original_words']}</td><td>{ext_stats['summary_words']}</td><td>{abs_stats['summary_words']}</td></tr>
                        <tr><td>Sentences</td><td>{ext_stats['original_sentences']}</td><td>{ext_stats['summary_sentences']}</td><td>{abs_stats['summary_sentences']}</td></tr>
                        <tr><td>Compression</td><td>—</td><td>{ext_stats['compression']}%</td><td>{abs_stats['compression']}%</td></tr>
                    </table>
                    """,
                    unsafe_allow_html=True,
                )

                export_sections = {
                    "Extractive Summary": results["extractive"],
                    "Abstractive Summary": results["abstractive"],
                }
            else:
                key = "extractive" if has_extractive else "abstractive"
                label = "Extractive Summary" if has_extractive else "Abstractive Summary"
                st.markdown(f'<div class="summary-body">{results[key]}</div>', unsafe_allow_html=True)

                stats = compute_stats(original, results[key])
                st.markdown(
                    f"""
                    <div class="stat-row">
                        <div class="stat-pill"><div class="num">{stats['original_words']}</div><div class="label">Original words</div></div>
                        <div class="stat-pill"><div class="num">{stats['summary_words']}</div><div class="label">Summary words</div></div>
                        <div class="stat-pill"><div class="num">{stats['compression']}%</div><div class="label">Compression</div></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                export_sections = {label: results[key]}

            keywords = results.get("keywords", [])
            if keywords:
                st.markdown('<div class="section-label">Keywords</div>', unsafe_allow_html=True)
                chips = "".join(f'<span class="keyword-chip">{word}</span>' for word, _ in keywords)
                st.markdown(f'<div class="keyword-row">{chips}</div>', unsafe_allow_html=True)
                export_sections["Keywords"] = ", ".join(word for word, _ in keywords)

            st.markdown('<div class="section-label">Export</div>', unsafe_allow_html=True)
            dl_col1, dl_col2 = st.columns(2)
            with dl_col1:
                st.download_button(
                    "Download as TXT",
                    data=build_txt(export_sections),
                    file_name="summary.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            with dl_col2:
                st.download_button(
                    "Download as PDF",
                    data=build_pdf("Content Summary", export_sections),
                    file_name="summary.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )