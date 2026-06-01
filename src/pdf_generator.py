from fpdf import FPDF

def create_pdf(title, content):
    """
    Creates a PDF document from a list of strings and returns it as bytes.
    
    Args:
        title (str): The title of the document.
        content (list): A list of strings, where each string is a paragraph.
        
    Returns:
        bytes: The generated PDF file as a byte string.
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Set title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, title, 0, 1, 'C')
    pdf.ln(10) # Add a little space

    # Set content font
    pdf.set_font("Arial", '', 12)
    
    for item in content:
        # This encoding handles special characters for writing to the PDF cell
        cleaned_item = item.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, cleaned_item)
        pdf.ln(5) # Add space between questions/answers

    # Return the PDF content as bytes, which is what Streamlit's download button needs.
    # We explicitly convert the bytearray from .output() into bytes.
    return bytes(pdf.output(dest='S'))