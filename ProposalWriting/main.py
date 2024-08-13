import requests
from PyPDF2 import PdfReader

filepath = r"E:\Data Science Journey\Optimum-Tech Projects\PDF-Filling-withRAG\InputData\Real Estate Development Tender Document.pdf"

text = ""
reader = PdfReader(filepath)

for page in reader.pages:
    text += page.extract_text()

print("PDF Text loaded successfully")


prompt = f"""
Create a comprehensive and persuasive project proposal based on the following requirements:

**Requirements:**
{text}

**Proposal Guidelines:**
* Adhere to professional and formal writing standards.
* Provide a clear and detailed overview of the project scope, objectives, and deliverables.
* Develop a compelling project plan outlining timelines, milestones, and resource allocation.
* Clearly articulate the project's value proposition and expected outcomes.
* Showcase your team's expertise and qualifications to execute the project successfully.
* Include a comprehensive budget breakdown and financial projections.
* Address potential risks and mitigation strategies.
* Conclude with a strong call to action and next steps.

**Proposal Structure (Suggested):**
* Executive Summary
* Project Overview
* Project Objectives and Scope
* Project Methodology
* Project Timeline and Milestones
* Project Budget
* Risk Assessment
* Team Qualifications
* Appendices (optional)

** Make Proposal as detailed as possible.**

**Additional Tips:**
* Tailor the proposal to the specific audience and their needs.
* Proofread carefully to ensure clarity and professionalism.
* Highlight unique selling points and competitive advantages.


**Proposal:**

"""

url = "http://localhost:11434/api/generate"

data = {
    "model": "llama3.1",
    "prompt": prompt,
    "stream": False
}

response = requests.post(url, json=data)

if response.status_code == 200:
    with open("output.txt", "w") as f:
        f.write(response.json()['response'])
else:
    print("Error Occurred")
