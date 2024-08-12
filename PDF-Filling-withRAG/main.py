# load the environment variables
from dotenv import load_dotenv
load_dotenv()
import os
import Models
from preprocessing import preprocessing_text, create_retriever, format_docs
from PDFLoad import ReadTenderPDF, load_pdf
# from prompts import promptforfilling, promptwithoutfilling, select_prompt
from generator import GenerateOutputText
from warnings import filterwarnings
filterwarnings("ignore")
# Define the LLM
google_LLM = Models.GoogleGenerativeLLM(google_api_key=os.getenv("GOOGLE_API_KEY"))
print("LLM loaded successfully ......")
# Define the retriever
ModelName = "sentence-transformers/all-mpnet-base-v2"

tenderPDFpath = "PDF-Filling-withRAG\InputData\Tender Information for document filling.pdf"

# Read the tender PDF
tenderPDFtext = ReadTenderPDF(tenderPDFpath)

print("Tender PDF loaded successfully ......")
# Preprocess the text
text_splits = preprocessing_text(tenderPDFtext)

# Create the retriever
retriever = create_retriever(ModelName,text_splits)

print("Retriever created successfully on Tender PDF......")
# Read the document to be filled

developedDocpath = "PDF-Filling-withRAG\InputData\Real Estate Development Tender Document.pdf"

# Load the document
developedDoc = load_pdf(developedDocpath)

print("Document to be filled loaded successfully ......")

output_text = GenerateOutputText(developedDoc,retriever,google_LLM)

print("Document filled successfully ......")
print("*"*50)
print(output_text)
print("*"*50)
# Open a file in write mode ('w') with UTF-8 encoding and save the string
with open('output.txt', 'w', encoding='utf-8') as file:
    file.write(output_text)




