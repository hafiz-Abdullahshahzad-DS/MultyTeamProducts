from PyPDF2 import PdfReader
from langchain.document_loaders import PyPDFLoader
def ReadTenderPDF(PDFFilePath):
    pdf_reader = PdfReader(PDFFilePath)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    return loader.load()