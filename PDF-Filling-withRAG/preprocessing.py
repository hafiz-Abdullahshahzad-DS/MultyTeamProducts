from langchain_community.vectorstores.faiss import FAISS
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from Models import LoadEmbeddingModel

def preprocessing_text(data):
    chara_text_splitter = CharacterTextSplitter()
    recur_text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
    )
    texts = chara_text_splitter.split_text(data)
    doc_data = [Document(page_content=t) for t in texts]
    text_splits = recur_text_splitter.split_documents(doc_data)
    return text_splits


def create_retriever(ModelName,text_splits):
    embedding_model = LoadEmbeddingModel(ModelName)
    vector_db = FAISS.from_documents(text_splits, embedding_model)
    retriever = vector_db.as_retriever(search_type="mmr", search_kwargs={"k": 3})
    return retriever
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
