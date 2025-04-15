from fastapi import FastAPI, Request
from pydantic import BaseModel
from rag_chain import get_rag_chain
from chat_history import ChatHistory
from web_scraper import crawl_and_scrape
from pydantic_models import QueryRequest
app = FastAPI()
qa_chain = get_rag_chain(model="gemini-2.0-flash")
chat_memory = ChatHistory()

#class QueryRequest(BaseModel):
#    query: str

@app.get("/scrape/")
def scrape(url: str):
    content = crawl_and_scrape(url)
    return {"status": "scraped", "length": len(content)}

@app.post("/chat/")
def chat(req: QueryRequest):
    chat_history = chat_memory.get()
    result = qa_chain.invoke({"question": req.query, "chat_history": chat_history})
    chat_memory.append(req.query, result["answer"])
    return {"response": result["answer"]} 

