import streamlit as st
from pdf_reader import extract_text_from_pdf
from preprocess import clean_text, get_sentences, get_filtered_words
from extractive import summarize_extractive

st.set_page_config(page_title="PDF Summarizer", page_icon="📄")

st.title("📄 PDF & Text Summarizer")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:

    # Extract text
    text = extract_text_from_pdf(uploaded_file)
    st.success("PDF uploaded successfully!")
    
    # NLP preprocessing
    cleaned_text = clean_text(text)
    sentences = get_sentences(cleaned_text)
    filtered_words = get_filtered_words(cleaned_text)

    # -------- Extractive Summary --------
    st.subheader("📄 Extractive Summary")
    st.caption(
        "This extractive summary selects the most important sentences from the original document based on word-frequency scoring."
    )

    ratio = st.slider(
        "Summary Length",
        min_value=0.1,
        max_value=0.5,
        value=0.3,
        step=0.05,
    )

    if st.button("Generate Extractive Summary"):

        summary, ranked_sentences = summarize_extractive(
            cleaned_text,
            summary_ratio=ratio,
        )

        st.success("Summary generated!")

        summary_sentences = get_sentences(summary)

        for i, sentence in enumerate(summary_sentences, start=1):
            st.markdown(f"**{i}.** {sentence}")

        original_words = len(cleaned_text.split())
        summary_words = len(summary.split())
        compression = (
            round((1 - summary_words / original_words) * 100, 1)
            if original_words
            else 0.0
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Original Words", original_words)
        col2.metric("Summary Words", summary_words)
        col3.metric("Compression", f"{compression}%")

        st.write(f"**Summary contains {len(ranked_sentences)} sentences.**")

    # -------- Preview --------
    st.subheader("Extracted Text Preview")
    st.text_area("PDF Content", cleaned_text[:3000], height=300)

    # -------- Debug Info --------
    with st.expander("View preprocessing details"):
        st.write(f"Characters: {len(cleaned_text)}")
        st.write(f"Sentences: {len(sentences)}")
        st.write(f"Meaningful Words: {len(filtered_words)}")

        st.write("First 5 sentences:")
        for sentence in sentences[:5]:
            st.write("-", sentence)