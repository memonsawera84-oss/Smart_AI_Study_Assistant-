"""
==================================================
PDF Utility Functions

This file extracts text from PDF documents.

Author: SK
==================================================
"""

import pdfplumber


def extract_pdf_text(pdf_file):
    """
    Extract all text from an uploaded PDF.

    Parameters:
        pdf_file: Uploaded PDF file from Streamlit

    Returns:
        String containing all extracted text
    """

    text = ""

    try:
        with pdfplumber.open(pdf_file) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        return f"Error: {e}"

    return text