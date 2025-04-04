from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.chains.summarize import load_summarize_chain
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

def main(url: str, open_api_key: str, temperature: int = 0, model_name: str = "gpt-3.5-turbo-16k"):
    """
    Main function to load website data and generate a summary using GPT-3.5.

    Args:
        url (str): The URL of the blog or article.
        open_api_key (str): Your OpenAI API key.
        temperature (int, optional): Temperature setting for the model (default 0).
        model_name (str, optional): The model to use (default "gpt-3.5-turbo-16k").

    Returns:
        str: The generated summary.
    """
    docs = load_data_from_website(url)
    llm = ChatOpenAI(temperature=temperature, model_name=model_name, openai_api_key=open_api_key)
    chain = load_summarize_chain(llm, chain_type="stuff")
    try:
        summary = chain.run(docs)
    except Exception as e:
        raise Exception(f"Failed to generate summary: {e}")
    return summary
