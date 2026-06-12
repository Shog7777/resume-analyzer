import io


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract text from a PDF file."""
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
            text = ""
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def extract_text_from_docx(uploaded_file) -> str:
    """Extract text from a DOCX file."""
    try:
        from docx import Document
        doc = Document(io.BytesIO(uploaded_file.read()))
        text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        return text.strip()
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"
