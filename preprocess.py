import re


STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "in", "is", "it", "of", "on", "or", "that", "the", "this", "to",
    "was", "were", "with",
}

def clean_text(text):
    """Clean PDF text while preserving content structure."""

    # Split into lines and remove empty ones
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # Remove the first line if it looks like a title
    if lines:
        first_line = lines[0]
        words = first_line.split()

        capitalized = sum(
            word[0].isupper() for word in words if word and word[0].isalpha()
        )

        if len(words) <= 12 and capitalized / len(words) > 0.6:
            lines.pop(0)

    # Join the remaining lines into one paragraph
    cleaned_text = " ".join(lines)

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