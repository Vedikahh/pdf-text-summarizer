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

# Project Structure

```text
pdf-text-summarizer/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Ignore venv, cache, etc.
│
├── sample_pdfs/                # Sample PDFs for testing
│   ├── story.pdf
│   ├── research_paper.pdf
│   └── article.pdf
│
├── utils/
│   ├── pdf_reader.py           # Extract text from uploaded PDFs
│   ├── preprocess.py           # Text cleaning, tokenization, stopword removal
│   ├── extractive.py           # Frequency-based extractive summarization
│   ├── abstractive.py          # T5 Transformer abstractive summarization
│   ├── metrics.py              # Compression ratio, word count, reading time
│   └── keywords.py             # Keyword extraction (optional enhancement)
│
├── models/                     # Model-related files
│   └── t5_summarizer.py        # Loads and runs the T5 summarization model
│
├── assets/                     # Images/icons used in README or app
│   ├── banner.png
│   └── logo.png
│
├── outputs/                    # Generated summaries (optional)
│   ├── extractive_summary.txt
│   └── abstractive_summary.txt
│
└── notebooks/                  # Experimentation notebooks (optional)
    └── summarization_experiments.ipynb
```
## Current Implementation Status

| Module | Status |
|--------|--------|
| PDF Text Extraction (PyMuPDF) | ✅ Completed |
| Text Preprocessing (NLTK) | ✅ Completed |
| Extractive Summarization | ✅ Completed |
| Summary Statistics | ✅ Completed |
| Abstractive Summarization (T5) | 🚧 In Progress |
| Extractive vs Abstractive Comparison | 🚧 Planned |
| Download Summary (.txt/.pdf) | 🚧 Planned |
| Keyword Extraction | 🚧 Planned |

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Current Status

- ✅ Extractive Summarization completed.
- 🚧 Abstractive Summarization (T5 Transformer) in progress.
