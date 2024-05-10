import streamlit as st
import fitz # PyMuPDF
import re

def read_pdf(pdf_file):
    pdf_doc = fitz.open(stream=pdf_file.read(), filetype='pdf')
    return pdf_doc

def count_pages(pdf_doc):
    total_pages = pdf_doc.page_count
    return total_pages

def extract_img(pdf_doc, page_number):
    page = pdf_doc[page_number -1]
    image_bytes = page.get_pixmap().tobytes()
    return image_bytes

# TODO: Transform to Class
def show_pdf(uploaded_file, key_number):

    pdf_doc = read_pdf(uploaded_file)

    total_pages = count_pages(pdf_doc)
    page_number = st.slider("Select a page", 1, total_pages, key_number)
    st.write(f"Page {page_number}/{total_pages}")

    image_bytes = extract_img(pdf_doc, page_number)
    st.image(image_bytes)

    return

class Redactor:
    
    def get_sensitive_data(self, lines, sensitive_words):
        
        for word in sensitive_words:

            # Create pattern with word boundaries.
            # Ensure word as a whole word,
            # not as part of another word.
            pattern = r'\b' + re.escape(word) + r'\b'
                        
            for line in lines:

                # matching the word to each line
                if re.search(pattern, line, re.IGNORECASE):
                    search = re.search(pattern, line, re.IGNORECASE)
                    yield search.group(1)

    # constructor
    def __init__(self, 
                 uploaded_file,
                 lines, 
                 sensitive_words):
        
        self.uploaded_file = uploaded_file
        self.lines = lines
        self.sensitive_words = sensitive_words
    
    def redaction(self):
        pdf_doc = fitz.open(self.uploaded_file)
        
        for page in pdf_doc:
            
            # For fixing alignment issues with rect boxes
            page._wrapContents()
            
            sensitive = self.get_sensitive_data(page.getText("text").split('\n'))

            for data in sensitive:
                areas = page.searchFor(data)

                # Draw outline over sensitive data
                [page.addRedactAnnot(area, fill = (0, 0, 0)) for area in areas]
            
            page._apply_redactions()
            pdf_doc.save('redacted.pdf')

            st.download_button(
                label = "Download Redacted PDF",

                # TODO: debug path
                data = 'redacted.pdf',
                file_name = "redacted_file.pdf"
           )