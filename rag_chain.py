from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from vector_store import get_vector_store


from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from typing import List
from langchain_core.documents import Document
import os

vectordb = get_vector_store()
retriever = vectordb.as_retriever(search_kwargs={"k": 4})

'''
def get_conversational_chain():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.2, 
        user_agent=os.getenv("USER_AGENT")
        )
    
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain


'''
# Output parser
output_parser = StrOutputParser()

# System prompts
contextualize_q_system_prompt = (
    "You are an AI assistant named **Alaukik**. Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is. "
    "If the user refers to you, remember that your name is Alaukik."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant named **Alaukik**, helping in extracting useful information from the documents. "
     "Use the following context and retain it as much as possible to answer the user's question accurately and in an easily understandable structure. "
     "If the response is listable, respond in bullet points. Respond in the requested language."),
    ("system", "Context: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

def get_rag_chain(model):
    # Load the Hugging Face model with the pipeline
    #hf_model = pipeline("text-generation", model=model)
    
    # Create Hugging Face Pipeline for Langchain
    #llm = HuggingFacePipeline(pipeline=hf_model)

    llm=ChatGoogleGenerativeAI(model=model,
                               temperature=0.4,
                               max_retries=5)
    
    # Create retriever and QA chains
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    # Create the RAG chain
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    
    return rag_chain  