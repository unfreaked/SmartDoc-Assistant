import PyPDF2
import pdfplumber

def extract_text_from_pdf(file):
    """Extracts text from a PDF file object."""
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_txt(file):
    """Extracts text from a TXT file object."""
    return file.read().decode('utf-8')

def parse_document(file, file_type):
    if file_type == 'pdf':
        return extract_text_from_pdf(file)
    elif file_type == 'txt':
        return extract_text_from_txt(file)
    else:
        raise ValueError('Unsupported file type') 