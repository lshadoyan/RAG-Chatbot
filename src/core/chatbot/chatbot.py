from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts.prompt import PromptTemplate
import toml
import src.core.prompt_library.prompt_library as p
from dotenv import load_dotenv

load_dotenv()

# Number of user and assistant messages to keep in chat history
history_len = 5

config = toml.load("./configs/config.toml")

async def stream_output(query, context, history):
    """
    Streams the output of a query processed by a language model, using context (retrieved from RAG) and history.

    Args:
        query (str): The user's query to be processed
        context (str): The context in which the query is asked
        history (list): the history of previous interactions
    
    Yields:
        str: The output chunks from the language model
    """
    prompt = PromptTemplate(input_variables=["history", "query", "context"], template=p.chatbot_prompt())
    print(history)
    model = ChatOpenAI(model=config["LLM"]["model"], streaming=True)
    chain = prompt | model
    input={
            "context":context,
            "history": history[-(history_len * 2):],
            "query":query
        }
    for chunk in chain.stream(input):
        yield chunk