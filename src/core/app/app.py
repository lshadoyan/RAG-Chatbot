import streamlit as st
import requests
import uuid
import toml

config = toml.load("./configs/config.toml")

base_url = config["URL"]["base_fastapi"]

headers = {
        "Content-Type": "application/json"
    }

# app title
st.title("ChatBot")

# Initializes session id
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Chat History
st.session_state.history = requests.get(
    url=f"{base_url}/history/",
    headers=headers,
    json={"session_id" : st.session_state.session_id}
).json()

# Displays chat history
for history in st.session_state.history:
    with st.chat_message(history["role"]):
        st.markdown(history["content"])

# Input query
query = st.chat_input("Enter:")

# Displays llm's response
if query:
    with st.chat_message("user"):
        st.markdown(query)
    with st.chat_message("assistant"):
        text=  ""
        placeholder = st.empty()
        print("hi!")
        for response in requests.get(url=f"{base_url}/chat/",
                                    json={"user_question" : {"query":query}, "session" : {"session_id" : st.session_state.session_id}},
                                    headers=headers,
                                    stream=True):
            text += response.decode("utf-8")
            placeholder.markdown(text)
