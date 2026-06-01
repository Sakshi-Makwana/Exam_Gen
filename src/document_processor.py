from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_pdf_text(pdf_doc):
    """
    Extracts text from an uploaded PDF document.
    
    Args:
        pdf_doc: The uploaded PDF file object.
        
    Returns:
        A single string containing all the text from the PDF.
    """
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def get_text_chunks(text):
    """
    Splits a long string of text into smaller, overlapping chunks.
    
    Args:
        text: The input string.
        
    Returns:
        A list of text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Size of each chunk in characters
        chunk_overlap=200, # Number of characters to overlap between chunks
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks