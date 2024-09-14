from dotenv import load_dotenv
import os
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import re
import pandas as pd
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
from PyPDF2 import PdfReader
from langchain_core.output_parsers import JsonOutputParser


# load the env Variables from the .env file
load_dotenv()

# # get the value of the env variable]
# print(os.getenv("GOOGLE_API_KEY"))

llm = GoogleGenerativeAI(model="gemini-1.0-pro-latest", google_api_key=os.environ["GOOGLE_API_KEY"],temperature=0.2)

template = """
you are a specialized AI Assistant that convert a text chunk into instruction, input and output.
Generate an instruction, input, and output pair based on the provided text chunk taken from industrial data. Focus on the core concepts and information presented. 

Text: {chunk}
Source: {filename}
Ensure:
* The instruction is clear and concise, specifying the task to be performed.
* The input is relevant and representative of the data in the text chunk.
* The Output is accurate and informative, demonstrating a deep understanding of the text.


Example result:
[
{{
  "instruction": "Summarize the key points of this paragraph in a concise sentence.",
  "input": "The paragraph discusses the challenges faced by the manufacturing industry due to rising energy costs and supply chain disruptions.",
  "output": "The manufacturing industry is struggling with increased energy expenses and disruptions in the supply chain."
}},
{{
  "instruction": "Explain in detail about unique features of PQR",
  "input": "",
  "output": "PQR have countless feature in industiral paradigm it include ....."
}}
]
"""

prompt = PromptTemplate.from_template(template)


# get all the pdfs in the current directory
# pdf_path = os.path.join(os.getcwd(),"new_files") # replace it with the path of the pdfs
pdf_path = r"E:\repos\gitDemo\FilesOT\new_files"
pdfs = [f for f in os.listdir(path=pdf_path) if f.endswith('.pdf')]
print(pdfs)
def visitor_body(text, cm, tm, font_dict, font_size):
    y = tm[5]
    if 50 < y < 715:    # Filter the text based on the y-axis o remove the header and footer
        # print(tm,text)
        parts.append(text)
def text_cleaner(text) -> str:
    # Define the regex pattern to match the lines to be removed
    pattern = r'[\d]+[.][\d]\s[\w]+.*'

    # Use re.sub() to remove the matched lines
    cleaned_text = re.sub(pattern, '', text, flags=re.MULTILINE)

    # Remove any extra newlines that may have been left behind
    cleaned_text = re.sub(r'\n+', '\n', cleaned_text).strip()
    return cleaned_text

def sanitize_string(value):
    if isinstance(value, str):
        value = ILLEGAL_CHARACTERS_RE.sub('', value)
    return value

def save_questions(filename, total_QAs):
    dataframe = pd.DataFrame(columns=['instruction', 'input','output'])
    for QA in total_QAs:
        try:
            # df = pd.DataFrame({'Question': list(QA.keys()), 'Answer': list(QA.values())})
            if isinstance(QA, dict):
                df = pd.DataFrame([QA])
            else:
                df = pd.DataFrame(QA)
            dataframe = pd.concat([dataframe, df], ignore_index=True)
        except:
            print(QA)
            continue
    outfilename = filename[:-4]
    print(dataframe.shape)
    # os.mkdir("IQAs")
    try:
        dataframe.to_excel(f"IQAs/{outfilename}.xlsx", index=False)
    except:
        sanitize_df = dataframe.applymap(sanitize_string)

        sanitize_df.to_excel(f"{outfilename}.xlsx", index=False)
    print(f"IQAs/{outfilename}.xlsx saved")


chunk_size = 500
step = 300
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# splits = text_splitter.split_documents([Document(page_content=cleaned_text)])

# Define the output parser
output_parser = JsonOutputParser()

chain  = prompt | llm | output_parser

for filename in pdfs[:len(pdfs)-1]:

    total_QAs = []
    # text = pdfdata[filename]
    reader = PdfReader(os.path.join(pdf_path, filename))
    total_text = ""
    for page in range(1,len(reader.pages)):
        parts = []
        # apply filtering on the text_body by visitor function
        text = reader.pages[page].extract_text(visitor_text=visitor_body)
        text_body = "".join(parts)
        # 
        #   Write code to filter the page text individually         
        #   Like if the Text body is small, then skip the page

        text_body = text_body.strip()   # Remove the Spaces from the ends
        text_body = text_cleaner(text_body)  # Clean the text
        if len(text_body) < 100:    # Skip the Page if the text is too small
            continue
        total_text += text_body
    text = total_text
    print(f"Total text length for filename:{filename} is {len(text)}")
    IQs = 0

    split_docs = text_splitter.split_documents([Document(page_content=text)])
    print(f"Generating IQAs for {filename} with number of chunks: {len(split_docs)}")
    # print(f"Generating QAs for {filename} with number of chunks: {((len(text)-chunk_size)/step)+1}")
    # for i in range(0, len(text), step):
    for i in range(0, len(split_docs)):
        # chunk = text[i:i+chunk_size]
        chunk = split_docs[i].page_content
        # print(chunk)
        try:
            result = chain.invoke({"chunk": chunk, "filename": filename})
            IQs += 1 # len(result)
        except:
            try:
                result = chain.invoke({"chunk": chunk, "filename": filename})
                IQs += 1 # len(result)
            except:
                print(f"Q/As generation failed for chunk# {i} in {filename}")
                continue
        # check the number of QAs generated
        
        total_QAs.append(result)
        if i % 5 == 0 and i != 0:
            print(f"QAs generated: {IQs}")
            print(f" chunks done: {i}")
    print(f"{filename} done")
    print(f"Total QAs generated: {IQs}")
    # break   # add if you want to test on one file only 
    save_questions(filename, total_QAs)