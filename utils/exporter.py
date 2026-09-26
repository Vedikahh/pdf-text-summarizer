def build_txt(sections):
    """sections: dict of {heading: text}. Returns a plain-text string."""
    parts = []
    for heading, text in sections.items():
        if not text:
            continue
        parts.append(heading.upper())
        parts.append("-" * len(heading))
        parts.append(text.strip())
        parts.append("")
    return "\n".join(parts).strip()


def build_pdf(title, sections):
    """sections: dict of {heading: text}. Returns PDF bytes."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 10, title)
    pdf.ln(4)

    for heading, text in sections.items():
        if not text:
            continue
        pdf.set_font("Helvetica", "B", 12)
        pdf.multi_cell(0, 8, heading)
        pdf.ln(1)
        pdf.set_font("Helvetica", "", 11)
        # Latin-1 fallback since core PDF fonts don't support full unicode
        safe_text = text.encode("latin-1", "replace").decode("latin-1")
        pdf.multi_cell(0, 6, safe_text)
        pdf.ln(4)

    return bytes(pdf.output(dest="S"))