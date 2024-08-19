import requests
from PyPDF2 import PdfReader
import difflib
filepath = r"E:\Data Science Journey\Optimum-Tech Projects\new_files\Natcast-NSTC-Workforce-Partner-Alliance-Program-CFP-REVISED-AS-OF-7-23-2024web.pdf"

text = ""
reader = PdfReader(filepath)

for page in reader.pages:
    text += page.extract_text()

print("PDF Text loaded successfully")


system_prompt = f"""
    
    As a seasoned proposal writer, you possess a unique blend of strategic insight and exceptional writing skills,
    enabling you to craft proposals that not only meet but exceed client expectations. Your approach is meticulous,
    ensuring that every proposal is tailored to address the specific needs outlined in the requirement document.
    You excel in presenting complex information clearly and concisely, utilizing a structured format that enhances
    readability and impact. Your ability to distill technical details into engaging, professional content showcases
    your commitment to delivering proposals that are both compelling and aligned with client objectives.
    With a keen eye for detail and a deep understanding of the proposal process, you consistently help in producing documents
    that stand out for their precision, relevance, and persuasive power.

    **Context:**
    {text}
    
    """


headings = [
    "Executive Summary",
    "Introduction and Background",
    "Scope of Work",
    "Technical Approach",
    "Project Management Plan",
    "Qualifications and Experience",
    "Team Structure and Staffing",
    "Work Plan and Schedule",
    "Cost Proposal",
    "Risk Management Plan",
    "Quality Assurance Plan",
    "Compliance with RFP Requirements",
    "References and Past Performance",
    "Terms and Conditions",
    "Conclusion"
]

url = "http://localhost:11434/api/chat"
output_text = ""
for heading in headings:
    user_prompt = f"Write {heading} in detail for the proposal"
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
    # "options" : {
    #     "mirostat": 0,          # Mirostat sampling (0 = disabled)
    #     "mirostat_eta": 0.1,    # Learning rate for Mirostat feedback
    #     "mirostat_tau": 2.0,    # Balance between coherence and diversity
    #     "num_ctx": 8192,        # Size of the context window
    #     "repeat_last_n": 64,    # Look back to prevent repetition
    #     "repeat_penalty": 1.1,  # Penalty for repeated phrases
    #     "temperature": 0.9,     # Creativity of the model
    #     "seed": 42,             # Random number seed
    #     "tfs_z": 1.0,           # Tail free sampling parameter
    #     "top_k": 30,            # Limits the token generation to the top k options
    #     "top_p": 0.85,           # Cumulative probability for token selection
    #     "min_p": 0.05           # Minimum probability for token consideration
    # },
    "stream": False
    }

    response = requests.post(url, json=data)


    if response.status_code == 200:
        print(f"heading {heading} completed successfully")
        output_text += "\n" + response.json()['message']['content'].strip()

    else:
        print(f"Error Occurred for {heading}")





# Define a function to refine the proposal by removing repetition
def refine_proposal(proposal_text):
    # Split proposal into sentences
    sentences = proposal_text.split('. ')

    # Remove similar sentences
    refined_sentences = []
    for i, sentence in enumerate(sentences):
        if i > 0:
            similarity = difflib.SequenceMatcher(None, sentences[i-1], sentence).ratio()
            if similarity != 1:  # Adjust the threshold as needed
                refined_sentences.append(sentence)
        else:
            refined_sentences.append(sentence)

    # Recombine sentences into a refined proposal
    refined_proposal = '. '.join(refined_sentences)

    return refined_proposal

# Refine the final proposal to remove repetitions
refined_proposal = refine_proposal(output_text)
# saving as txt file
with open("outputN.txt", "w") as f:
    f.write(refined_proposal)


