import streamlit as st
import requests

st.set_page_config(page_title="Gemini Chatbot", layout="centered")

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000/chat/"

st.title("Abhimo Tecchnologies")
welcome_message = "Hello I am alaukik, your assistant"


# Chat history maintained in Streamlit session
if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assiatant","content": welcome_message}]

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
query = st.chat_input("Ask me anything about the website...")

if query:
    # Add user query to history
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Send query to FastAPI chatbot
    try:
        response = requests.post(API_URL, json={"query": query})
        response.raise_for_status()
        result = response.json()
        answer = result.get("response", "Sorry, no response received.")
    except Exception as e:
        answer = f"❌ Error: {str(e)}"

    # Add bot response to history
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)