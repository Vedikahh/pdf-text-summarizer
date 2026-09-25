from functools import lru_cache

from utils.preprocess import remove_title


@lru_cache(maxsize=1)
def _get_summarizer():
    """Load the model only when abstractive summarization is requested."""
    from transformers import pipeline

    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")


def summarize_abstractive(text, max_length=130, min_length=30):
    """Generate an abstractive summary from title-free text."""
    text = remove_title(text).strip()
    if not text:
        return ""

    summarizer = _get_summarizer()
    result = summarizer(
        text,
        max_length=max_length,
        min_length=min(min_length, max_length - 1),
        do_sample=False,
    )
    return result[0]["summary_text"].strip()