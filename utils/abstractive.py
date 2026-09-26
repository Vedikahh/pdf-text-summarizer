from functools import lru_cache

from utils.preprocess import remove_title


@lru_cache(maxsize=1)
def _get_summarizer():
    """Load the model only when abstractive summarization is requested."""
    from transformers import pipeline

    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")


def summarize_abstractive(text, max_length=130, min_length=30):
    """Generate an abstractive summary from title-free text.

    Note: distilbart-cnn-12-6 has a hard 1024-token input limit. truncation=True
    ensures long documents are safely cut down instead of crashing with an
    IndexError, but only the first ~800-900 words are actually considered.
    """
    text = remove_title(text).strip()
    if not text:
        return ""

    summarizer = _get_summarizer()
    result = summarizer(
        text,
        max_length=max_length,
        min_length=min(min_length, max_length - 1),
        do_sample=False,
        truncation=True,
    )
    return result[0]["summary_text"].strip()