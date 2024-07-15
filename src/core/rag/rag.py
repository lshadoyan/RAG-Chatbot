from src.core.database.chroma_database import DataBase
from pydantic import BaseModel, ValidationError
from typing import List, Union, Optional

class RAG:
    """
    A class to perform retrieval-augmented generation (RAG) tasks

    Attributes:
        vectorstore (object): The vector store object used for similarity search
    """
    def __init__(self):
        """
        Initializes the RAG class and sets up the vectorstore
        """
        db = DataBase()
        self.vectorstore = db.get_vectorstore()

    def retrieval(self, docs):
        """
        Extracts the original context/text from the metadata of the summarized documents

        Args: 
            docs (list): A list of documents
        
        Returns:
            A list of the original text
        """

        text = []
        for doc in docs:
            context = doc.metadata["original"]
            text.append(context)
        return text

    def search(self, query):
        """
        Searches for summarized documents most relevent to input query and retrieves their original text

        Args:
            query (str): The user search query string.

        Returns:
            str: A concatenated string of original texts from the most relevent summarized documents
        """
        search_results = self.vectorstore.similarity_search_with_relevance_scores(query, k=8)
        docs = [doc for doc, score in search_results if score >= 0.7]
        text = self.retrieval(docs)
        context = "\n".join(text)
        return context