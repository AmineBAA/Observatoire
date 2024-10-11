import streamlit as st
import PyPDF2
import difflib

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

# Function to compare two PDFs and highlight differences
def compare_tariffs(pdf1_file, pdf2_file):
    # Extract text from both PDF files
    pdf1_text = extract_text_from_pdf(pdf1_file)
    pdf2_text = extract_text_from_pdf(pdf2_file)

    # Split the text into lines for better comparison (each line represents a service/tariff)
    pdf1_lines = pdf1_text.splitlines()
    pdf2_lines = pdf2_text.splitlines()

    # Find differences between the two files
    diff = difflib.unified_diff(pdf1_lines, pdf2_lines, lineterm='', n=0)

    # Extract changes and affected services
    changes = []
    for line in diff:
        if line.startswith('-') or line.startswith('+'):  # Lines with differences
            changes.append(line)

    return changes

# Streamlit app
st.title("Bank Tariff Comparison")

# File upload section
st.write("Upload two PDF files (from different dates) to compare tariffs:")

# Upload two PDF files
pdf1_file = st.file_uploader("Upload the first PDF file", type="pdf")
pdf2_file = st.file_uploader("Upload the second PDF file", type="pdf")

if pdf1_file is not None and pdf2_file is not None:
    # When both PDFs are uploaded, compare them
    st.write("Comparing the two PDFs...")

    # Compare the tariffs
    tariff_changes = compare_tariffs(pdf1_file, pdf2_file)

    # Display the changes in services/tariffs
    st.write("Changes in services/tariffs:")
    for change in tariff_changes:
        st.write(change)
