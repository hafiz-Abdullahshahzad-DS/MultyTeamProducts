
import requests
from PyPDF2 import PdfReader
import ollama
import re
import docx
# from langchain_ollama import ChatOllama

# llm = ChatOllama(
#     model = "llama3.1",
#     temperature=0
# )

# print(llm.invoke("Hi").content)

filepath = r"E:\Data Science Journey\Optimum-Tech Projects\PDF-Filling-withRAG\InputData\Real Estate Development Tender Document.pdf"

text = ""
reader = PdfReader(filepath)

for page in reader.pages:
    text += page.extract_text()

print("PDF Text loaded successfully")




###### Evaluator LLM (Compliance Check)


system_prompt = f"""
 you are specialized AI Assistant that break down the Requirement document to
 small sub requirements (Questionables).
 You will be provided a text of Requirement Document.
 ** output should be a list seperated by commas for further parsing inside [ ]**
"""

user_prompt = f"""
Detailed Requirement:

{text}
"""

data = {

    "model": "llama3.1",
    "messages": [
        {
            "role":"system",
            "content":system_prompt
        },
        {
            "role":"user",
            "content":user_prompt
        }
    ],
    "stream": False
}
url = "http://localhost:11434/api/chat"

response = requests.post(url, json=data)

if response.status_code == 200:
    print(f"Evaluator List completed successfully")
    req_proposal = response.json()['message']['content'].strip()
    print(response.json()['message']['content'].strip())
    # output_text += "\n" + response.json()['message']['content'].strip()
else:
    print(f"Error Occurred ... ")


# Load the Docx file for checking


def load_docx(file_path):
    doc = docx.Document(file_path)
    content = []

    # Iterate through paragraphs and append them to the content list
    for para in doc.paragraphs:
        content.append(para.text)

    return '\n'.join(content)

docx_path = r"E:\Data Science Journey\Optimum-Tech Projects\TestCasesforproposalwriting\SampleProposalRET.docx"

docx_text = load_docx(docx_path)

system_prompt = f"""
    You are specialized AI Proposal Evaluator that reports the user completely whether the Generated proposal meets the user requirements.

    **inputs**
    * User Requirements in the form of list or detailed Text 
    * Proposal generated 

    ** output** 
    * A complet Evaluation Report
    * Percentage score that defines how much requirements are met

"""

user_prompt = f"""
    The Requirements for the proposal are:
    {req_proposal}

    Proposal generated:
    {docx_text}

    Evaluation Report: 
"""

data = {

    "model": "llama3.1",
    "messages": [
        {
            "role":"system",
            "content":system_prompt
        },
        {
            "role":"user",
            "content":user_prompt
        }
    ],
    "stream": False
}
url = "http://localhost:11434/api/chat"

response = requests.post(url, json=data)

if response.status_code == 200:
    print(f"Report completed successfully")
    report = response.json()['message']['content'].strip()
    print("*"*20)
    print(report)
    # output_text += "\n" + response.json()['message']['content'].strip()
else:
    print(f"Error Occurred ... ")







