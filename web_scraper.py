from bs4 import BeautifulSoup
import requests
from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader
unreachable_pages=[]
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Step 1: Extract all links from a given webpage
def extract_links(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    extracted_count=0
    links = set()
    for a_tag in soup.find_all("a", href=True):
        link = a_tag["href"]
        print(type(link),"\n","link:",link)

        extracted_count+=1
        if link.startswith("http"):  # Ensure absolute URLs
            links.add(link)
        else: 
            full_link="https://abhimo.com/"+link
            links.add(full_link)
            print("full_link:",full_link)
    print(f'''extracted:"{extracted_count}\n visted:{len(links)}''')
    return list(links)

# Step 2: Use WebBaseLoader to load content from extracted links


def load_webpages(urls):
    try:
        loader = WebBaseLoader(urls)
        docs = loader.load()
        if not docs==None:
            return docs
    except:
        unreachable_pages.append(urls) 

# Example Usage
'''def crawl_and_scrape(main_url):
    #main_url = "https://playarena.in/"  # Replace with the target website
    extracted_links = extract_links(main_url)
    for link in extracted_links:
        print(f"Extracted Link: {link}")

    print("Total number of links:",len(extracted_links))
    extracted_docs=[]
    # Limit to first 5 links for demonstration
    for link in extracted_links:
        extracted_docs.append(load_webpages(link))
        print("----------------------------------------------")
        print(extracted_docs)
    print("Total number of unreachable pages:",len(unreachable_pages))

    for pages in unreachable_pages:
        print(f"Unreachable pages:{pages}\n")
    # Print results
    for doc in extracted_docs:
        print(f"URL: {doc.metadata['source']}\nContent: {doc.page_content[:500]}\n")
    return extracted_docs'''
'''
def crawl_and_scrape(main_url):
    #main_url = "https://playarena.in/"  # Replace with the target website
    extracted_links = extract_links(main_url)
    for link in extracted_links:
        print(f"Extracted Link: {link}")

    print("Total number of links:",len(extracted_links))

    # Limit to first 5 links for demonstration
    for link in extracted_links:
        extracted_docs=load_webpages(link)
        print("----------------------------------------------")
        print(extracted_docs)
    print("Total number of unreachable pages:",len(unreachable_pages))

    for pages in unreachable_pages:
        print(f"Unreachable pages:{pages}\n")
    # Print results
    for doc in extracted_docs:
        print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print(f"URL: {doc.metadata['source']}\nContent: {doc.page_content[:500]}\n")
    return extracted_docs
'''

def crawl_and_scrape(main_url: str) -> list[Document]:
    all_docs = []
    extracted_links = extract_links(main_url)
    
    print("Total number of links:", len(extracted_links))

    for link in extracted_links:
        extracted_docs = load_webpages(link)
        if extracted_docs:
            all_docs.extend(extracted_docs)
        print(f"Extracted {len(extracted_docs)} docs from: {link}")

    print("Total number of unreachable pages:", len(unreachable_pages))
    for page in unreachable_pages:
        print(f"Unreachable page: {page}")
    
    print("Total number of documents extracted:", len(all_docs))
    return all_docs