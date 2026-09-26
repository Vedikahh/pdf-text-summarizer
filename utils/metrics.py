import re


def _sentence_count(text):
    if not text.strip():
        return 0
    return len([s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()])


def compute_stats(original_text, summary_text):
    """Return word/sentence counts and compression % for a summary vs its source text."""
    original_words = len(original_text.split())
    summary_words = len(summary_text.split())

    compression = 0.0
    if original_words > 0:
        compression = round(100 - (summary_words / original_words * 100), 1)

    return {
        "original_words": original_words,
        "summary_words": summary_words,
        "original_sentences": _sentence_count(original_text),
        "summary_sentences": _sentence_count(summary_text),
        "compression": compression,
    }