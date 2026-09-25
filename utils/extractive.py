from collections import Counter
from utils.preprocess import get_sentences, get_filtered_words, remove_title


def summarize_extractive(text, summary_ratio=0.3):
    """
    Generate an extractive summary using word-frequency scoring.

    Args:
        text (str): Input text.
        summary_ratio (float): Percentage of sentences to keep.

    Returns:
        summary (str), ranked_sentences (list)
    """

    text = remove_title(text)
    sentences = get_sentences(text)

    # Remove title-like first sentence
    if sentences:
        first_sentence = sentences[0]
        words = first_sentence.split()

        capitalized_words = sum(
            word[0].isupper() for word in words if word and word[0].isalpha()
        )

        if (
            len(words) <= 12
            and capitalized_words / max(len(words), 1) > 0.6
        ):
            sentences = sentences[1:]

    words = get_filtered_words(text)

    if not sentences or not words:
        return "", []

    # Step 1: Count word frequencies
    word_freq = Counter(words)

    # Step 2: Normalize frequencies
    max_freq = max(word_freq.values())

    for word in word_freq:
        word_freq[word] /= max_freq

    # Step 3: Score each sentence
    sentence_scores = {}

    for sentence in sentences:
        sentence_words = get_filtered_words(sentence)

        # Skip headings or very short and citation-like sentences.
        if len(sentence_words) < 5 or len(sentence_words) > 45:
            continue

        for word in sentence_words:
            if word in word_freq:
                sentence_scores[sentence] = (
                    sentence_scores.get(sentence, 0) + word_freq[word]
                )

    # Step 4: Select top sentences
    summary_length = max(1, int(len(sentences) * summary_ratio))

    ranked_sentences = sorted(
        sentence_scores,
        key=sentence_scores.get,
        reverse=True
    )[:summary_length]

    # Step 5: Preserve original order
    ordered_summary = [
        sentence for sentence in sentences
        if sentence in ranked_sentences
    ]

    summary = " ".join(ordered_summary)

    return summary, ranked_sentences