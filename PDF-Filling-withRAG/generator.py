from langchain_core.runnables import RunnablePassthrough
from langchain.docstore.document import Document
from tqdm import tqdm
from prompts import select_prompt
from preprocessing import format_docs

def GenerateOutputText(developedDoc,retriever,LLM):
    output_text = ""
    # filledpages = []
    print("starting filling the document ......")

    for document in tqdm(developedDoc, desc="Processing Documents"):
        prompt = select_prompt(document.page_content)
        rag_chain = (
            {"context": retriever | format_docs, "input": RunnablePassthrough()}
            | prompt
            | LLM
            )
        out = rag_chain.invoke(document.page_content)
        # filledpages.append(Document(page_content= out))
        output_text +=out
    return output_text