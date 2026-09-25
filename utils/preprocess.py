import re


STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "in", "is", "it", "of", "on", "or", "that", "the", "this", "to",
    "was", "were", "with",
}

def _looks_like_title(line):
    words = line.split()
    capitalized = sum(
        word[0].isupper() for word in words if word and word[0].isalpha()
    )
    return bool(words) and len(words) <= 12 and capitalized / len(words) >= 0.5


def remove_title(text):
    """Remove a title-like first line before text is summarized."""
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if lines and _looks_like_title(lines[0]):
        lines.pop(0)

    cleaned_text = " ".join(lines)
    sentences = re.split(r"(?<=[.!?])\s+", cleaned_text, maxsplit=1)
    if len(sentences) > 1 and _looks_like_title(sentences[0]):
        return sentences[1]
    return cleaned_text


def clean_text(text):
    """Clean PDF text while preserving content structure."""

    cleaned_text = remove_title(text)

    # Remove extra spaces
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)

    return cleaned_text.strip()


def get_sentences(text):
    """Split cleaned text into non-empty sentences."""
    return [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", text) if sentence.strip()]


def get_filtered_words(text):
    """Return lowercase words while excluding common stop words."""
    words = re.findall(r"[A-Za-z]+(?:['-][A-Za-z]+)?", text.lower())
    return [word for word in words if word not in STOP_WORDS]
