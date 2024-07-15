from pydantic import BaseModel, ValidationError
from pymongo import MongoClient
from datetime import datetime
import time
import toml

config = toml.load("./configs/config.toml")

class Message(BaseModel):
    """
    Data model for a message using Pydantic for validation.

    Attributes:
        session_id (str): The session ID for the message
        role (str): The role of the sender (user or assistant)
        content (str): The content of the message
        timestamp (datetime): The timestamp when the message was created 
    """
    session_id : str
    role : str
    content : str
    timestamp : datetime

class MongoHistory:
    """
    MongoHistory class for managing message history in a MongoDB collection

    Attributes: 
        collection (Collection): The MongoDB collection to store and retrieve chat history
    """
    def __init__(self):
        """
        Initializes the MongoHistory instance by connecting to the MongoDB database
        """
        client = MongoClient(config["MONGO"]["host"], config["MONGO"]["port"])
        db = client["multi_modal_database"]
        self.collection =  db["test_collection"]

    def add_message(self, session_id, role, content):
        """
        Adds a message to the MongoDB collection

        Args:
            session_id (str): The session ID of the message
            role (str): The role of the sender (user or assistant)
            content (str): The content of the message
        """
        message = Message(
            session_id = session_id,
            role = role,
            content = content,
            timestamp = datetime.fromtimestamp(time.time(), None)
        )
        self.collection.insert_one(message.model_dump())

    def get_history(self, session_id):
        """
        Retrieves the message history for a given session ID, sorted by timestamp

        Args: 
            session_id (str): The session ID to retrieve the history
        
        Returns:
            list: A list of messages sorted by timestamp
        """
        projection = {"_id" : 0, "role" : 1, "content" : 1}

        sorted_history = self.collection.find({"session_id" : session_id}, projection).sort({"timestamp" : 1})
        return list(sorted_history) 
        
    def mongo_view(self):
            """
            Prints all documents in the MongoDB collection for debugging purposes
            """
            for c in self.collection.find():
                print(c)

    def clear_mongo(self):
            """
            Clears all documents in the MongoDB collection
            """
            self.collection.drop()



