import docx
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
import numpy as np
from PyPDF2 import PdfReader

# filepath = r"E:\Data Science Journey\Optimum-Tech Projects\new_files\Natcast-NSTC-Workforce-Partner-Alliance-Program-CFP-REVISED-AS-OF-7-23-2024web.pdf"
# filepath = r"/content/Tender 2.pdf"
filepath = r"/content/Real Estate Development Tender Document.pdf"

pdftext = ""
reader = PdfReader(filepath)

for page in reader.pages:
    pdftext += page.extract_text()

# print(pdftext)
def load_docx(file_path):
    doc = docx.Document(file_path)
    content = []

    # Iterate through paragraphs and append them to the content list
    for para in doc.paragraphs:
        content.append(para.text)
    
    return '\n'.join(content)

# Example usage
# file_path = r'/content/output_1724136240.6095726.docx'  # Replace with your file path
file_path = r'/content/SampleProposalRET.docx'  # Replace with your file path

docx_text = load_docx(file_path)


# Load the pre-trained SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def chunk_text(text, chunk_size=1):
    sentences = text.split('. ')
    return ['. '.join(sentences[i:i + chunk_size]) for i in range(0, len(sentences), chunk_size)]

def calculate_document_similarity(text1, text2, chunk_size=1):
    # Split the texts into chunks
    chunks1 = chunk_text(text1, chunk_size)
    chunks2 = chunk_text(text2, chunk_size)
    # print(len(chunks1))
    # print(chunks1[0])
    # Encode the chunks into embeddings
    embeddings1 = model.encode(chunks1)
    embeddings2 = model.encode(chunks2)
    
    # Calculate pairwise cosine similarity between all chunks
    similarities = np.array([[1 - cosine(emb1, emb2) for emb2 in embeddings2] for emb1 in embeddings1])
    # Aggregate the similarities (e.g., mean of the max similarities for each chunk in text1)
    similarity_score = np.mean(np.max(similarities, axis=1))
    return similarity_score

# # Example usage
# text1 = "This is a long document with many sentences. It contains detailed information on various topics. ..."
# text2 = "This is another long document that has overlapping topics with the first one. It discusses similar details. ..."

similarity = calculate_document_similarity(docx_text, pdftext, chunk_size=1)
print(f"Similarity Score: {similarity:.4f}")