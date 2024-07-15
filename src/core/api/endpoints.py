from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from src.core.database.chat_history import MongoHistory
from dotenv import load_dotenv
from src.core.chatbot.chatbot import stream_output
from src.core.rag.rag import RAG
import asyncio

load_dotenv()

# Initializes FastAPI application
app = FastAPI()

# Initializes RAG and MongoHistory instances
rag = RAG()
mongo_history = MongoHistory()

class ChatQuestion(BaseModel):
    """
    Pydantic model for validating chat questions

    Attributes:
        query (str): The user's query
    """
    query: str

class Session(BaseModel):
    """
    Pydantic model for validating session ID

    Attributes:
    session_id (str): The session ID
    """
    session_id : str

async def llm_response(query, history, session_id):
    """
    Asynchronously generates responses from the language model and streams it

    Args:
        query (str): The user's query
        history (list): The history of previous interactions
        session_id (str): The session ID
    
    Yields:
        str: The output chunks from the llm
    """
    response_text = ""
    context = rag.search(query)
    print(context)
    async for chunk in stream_output(history=history, context= context, query=query):
        response_text += chunk.content
        await asyncio.sleep(0)
        yield chunk.content
    mongo_history.add_message(role="assistant", session_id=session_id, content=response_text)


@app.get("/chat")
async def chat_endpoint(user_question: ChatQuestion, session : Session):
    """
    Endpoint to handle chat requests

    Args:
        user_question (ChatQuestion): The user's chat question
        session (Session): The session ID
    
    Returns:
        StreamingResponse: The streaming response for the language model
    """
    history = mongo_history.get_history(session_id=session.session_id)
    mongo_history.add_message(role="user", session_id=session.session_id, content=user_question.query) 
    return StreamingResponse(llm_response(query=user_question.query, history=history, session_id=session.session_id))

@app.get("/history")
async def get_chat_history(session : Session):
    """
    Endpoint to retrieve chat history for a session

    Args:
        session (Session): The session information
    
    Returns:
        list: The chat history for the session
    """
    history = mongo_history.get_history(session_id=session.session_id)
    return history




