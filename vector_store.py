#from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from web_scraper import crawl_and_scrape
import os
#from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()

print("GOOGLE_API_KEY:", os.getenv("GOOGLE_API_KEY"))
print("USER_AGENT:", os.getenv("USER_AGENT"))
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001",user_agent=os.getenv("USER_AGENT"))
vectordb=Chroma(persist_directory="./chroma_db",embedding_function=embedding)

'''def get_vector_store():
    base_url="https://abhimo.com/"
    #loader = crawl_and_scrape(base_url)
    documents = crawl_and_scrape(base_url)
    print(documents)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)
    for split in splits:
        split.metadata["file_id"] = 1
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001",user_agent=os.getenv("USER_AGENT"))
    #embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma(persist_directory="./chroma_db", embedding_function=embedding)
    docs = vectordb.get(where={"file_id": 1})   
    vectordb._collection.delete(where={"file_id": 1})
    vectordb.delete_collection()
    print(len(documents),"were added to Vectorstore")
    vectordb = Chroma.from_documents(documents=docs, embedding=embedding, persist_directory="chroma_db")
    vectordb.persist()
    print("========Vectorstore created successfully========")
    return vectordb'''


def get_vector_store():
    base_url="https://abhimo.com/"
    documents = crawl_and_scrape(base_url)
    delete_doc_from_chroma(1)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    for doc in docs:
        doc.metadata['contentID'] = 1
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    '''vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embedding,
        persist_directory="chroma_db"
    )'''
    vectordb.add_documents(docs)
    print(f"{len(docs)} were added to VECTORSTORE")
    vectordb.persist()
    return vectordb
    

def delete_doc_from_chroma(contentID: int):
    try:
        docs = vectordb.get(where={"contentID": contentID})
        print(f"Found {len(docs['ids'])} document chunks for contentID {contentID}")

        vectordb._collection.delete(where={"contentID": contentID})
        print(f"Deleted all documents with contentID {contentID}")

        return True
    except Exception as e:
        print(f"Error deleting document with contentID {contentID} from Chroma: {str(e)}")
        
        return False