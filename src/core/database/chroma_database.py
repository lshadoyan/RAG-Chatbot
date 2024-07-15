from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import shutil
import toml
import os

config = toml.load("./configs/config.toml")

class DataBase:
    """
    DataBase class for managing the Chroma vectorstore

    Attributes:
        vectordatabase (Chroma): Instance of Chroma vectorstore
    """
    def __init__(self):
        """
        Initializes the DataBase instance by loading env variables
        and sets up the Chroma vectorstore with the specified embedding
        and directory
        """
        load_dotenv()
        self.vectordatabase = Chroma(embedding_function=OpenAIEmbeddings(), persist_directory=config["CHROMA"]["path"])
    
    def clear_chroma(self):
        """
        Clears the Chroma vectorstore directory if it exists
        """
        if os.path.exists(config["CHROMA"]["path"]):
            shutil.rmtree(config["CHROMA"]["path"])
        
    def get_vectorstore(self):
        """
        Returns the Chroma vectorstore instance

        Returns:
            Chroma: The initialized Chroma vectorstore
        """
        return self.vectordatabase