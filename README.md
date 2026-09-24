# PDF & Text Summarizer (NLP)

A Streamlit-based NLP application that summarizes PDF documents and text using both **Extractive** and **Abstractive** summarization techniques.

## Features

- Upload PDF documents.
- Extract text using PyMuPDF.
- Clean and preprocess text using NLTK.
- Generate extractive summaries using a frequency-based NLP algorithm.
- Adjustable summary length.
- Summary statistics (original words, summary words, compression ratio).

## Tech Stack

- Python
- Streamlit
- PyMuPDF
- NLTK
- spaCy (preprocessing)
- Transformers (coming next for abstractive summarization)

## Project Structure

```text
pdf-text-summarizer/
│── app.py
│── pdf_reader.py
│── preprocess.py
│── extractive.py
│── README.md
│── requirements.txt
│── .gitignore
```

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Current Status

- ✅ Extractive Summarization completed.
- 🚧 Abstractive Summarization (T5 Transformer) in progress.