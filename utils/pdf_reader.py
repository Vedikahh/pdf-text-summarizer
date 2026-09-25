import pymupdf

def extract_text_from_pdf(pdf_file):
    """
    Extract text from an uploaded PDF.
    """

    document = pymupdf.open(stream=pdf_file.read(), filetype="pdf")

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text

