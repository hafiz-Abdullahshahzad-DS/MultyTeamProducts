from langchain_google_genai import GoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
def GoogleGenerativeLLM(google_api_key):
    return GoogleGenerativeAI(model="gemini-1.0-pro-latest", google_api_key=google_api_key)
                         
def LoadEmbeddingModel(ModelName):
    return HuggingFaceEmbeddings(model_name = ModelName)