from langchain.document_loaders import WebBaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from typing import List

def load_data_from_website(url: str) -> List:
    """Load data from the URL and return a list of Document.

    Args:
        url (str): URL to load.

    Returns:
        List: List of Document objects.
    
    Raises:
        ValueError: If the URL is invalid.
        Exception: If loading fails.
    """
    if not url.startswith("http"):
        raise ValueError("Invalid URL: URL must start with http or https")
    loader = WebBaseLoader(url)
    try:
        docs = loader.load()
    except Exception as e:
        raise Exception(f"Failed to load data from {url}: {e}")
    return docs

def main(url: str, query: str, openai_api_key: str, model_name: str = 'gpt-3.5-turbo', temperature: int = 0):
    """
    Main function to process website content and answer questions using GPT-3.5.

    This function:
      1. Loads website data.
      2. Splits the data into manageable chunks.
      3. Stores text chunks in a vector database using FAISS.
      4. Retrieves relevant chunks and generates an answer based on the query.

    Args:
        url (str): The URL of the blog or article.
        query (str): The question to be answered.
        openai_api_key (str): Your OpenAI API key.
        model_name (str, optional): The model to use (default "gpt-3.5-turbo").
        temperature (int, optional): Temperature setting for the model (default 0).

    Returns:
        str: The generated answer.
    """
    docs = load_data_from_website(url)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    documents = text_splitter.split_documents(docs)
    try:
        db = FAISS.from_documents(documents=documents, embedding=OpenAIEmbeddings(openai_api_key=openai_api_key))
    except Exception as e:
        raise Exception(f"Failed to create vector database: {e}")
    llm = ChatOpenAI(model_name=model_name, temperature=temperature, openai_api_key=openai_api_key)
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())
    try:
        result = qa_chain({"query": query})
    except Exception as e:
        raise Exception(f"Failed to generate answer: {e}")
    return result['result']
