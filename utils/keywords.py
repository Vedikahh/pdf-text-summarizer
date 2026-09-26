from collections import Counter

from utils.preprocess import get_filtered_words


def extract_keywords(text, top_n=10):
    """
    Extract the most significant keywords from text using normalized word frequency.

    Args:
        text (str): Input text (already cleaned/title-stripped is fine either way).
        top_n (int): Number of keywords to return.

    Returns:
        list[tuple[str, float]]: (keyword, normalized_score) sorted by score, descending.
    """
    words = get_filtered_words(text)
    if not words:
        return []

    # Skip very short tokens (typically noise, not real keywords)
    words = [w for w in words if len(w) > 2]
    if not words:
        return []

    freq = Counter(words)
    max_freq = max(freq.values())

    scored = [(word, round(count / max_freq, 2)) for word, count in freq.items()]
    scored.sort(key=lambda item: item[1], reverse=True)

    return scored[:top_n]