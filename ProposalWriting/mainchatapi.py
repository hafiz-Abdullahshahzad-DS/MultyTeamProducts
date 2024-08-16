import requests
from PyPDF2 import PdfReader

filepath = r"E:\Data Science Journey\Optimum-Tech Projects\new_files\RFP 202401 Real Estate Bro.pdf"

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

url = "http://localhost:11434/api/chat"

data = {
    "model": "gemma2",
    "messages": [
        {
            "role":"user",
            "content":"Write 5000 words  report on algotrading"
        }
    ],
    "options" : {
        "mirostat": 1,          # Mirostat sampling (0 = disabled)
        "mirostat_eta": 0.3,    # Learning rate for Mirostat feedback
        "mirostat_tau": 2.0,    # Balance between coherence and diversity
        "num_ctx": 8192,        # Size of the context window
        "repeat_last_n": 64,    # Look back to prevent repetition
        "repeat_penalty": 1.1,  # Penalty for repeated phrases
        "temperature": 0.9,     # Creativity of the model
        "seed": 42,             # Random number seed
        "tfs_z": 1.0,           # Tail free sampling parameter
        "top_k": 30,            # Limits the token generation to the top k options
        "top_p": 0.85,           # Cumulative probability for token selection
        "min_p": 0.05           # Minimum probability for token consideration
    },
    "stream": False
}

response = requests.post(url, json=data)


if response.status_code == 200:
    print(response.json()['message']['content'])
    with open("outputllama3-1.txt", "w") as f:
        f.write(response.json()['message']['content'])
else:
    print("Error Occurred")
