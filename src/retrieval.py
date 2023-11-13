import time
import os
from fetch_web_content import fetch_web_content
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Qdrant
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

TOP_K = 10

def embeddding_retrieval(contents_list: list, link_list: list, query: str):
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 0
    )
    
    # Mark the chunks with thier webpage index:
    metadatas=[{'url': link} for link in link_list] # VERY IMPORTANT!
    texts = text_splitter.create_documents(contents_list, metadatas=metadatas) # No need to read a document

    db = Chroma.from_documents(
        texts,
        # OpenAIEmbeddings(model='text-embedding-ada-002', openai_api_key='),
        # SentenceTransformerEmbeddings(model_name="shibing624/text2vec-base-chinese"),
        OpenAIEmbeddings(model='text-embedding-ada-002', openai_api_key='')
    )

    retriever = db.as_retriever(search_kwargs={"k": TOP_K}) 
    relevant_docs_list = retriever.get_relevant_documents(query)

    return relevant_docs_list


# Testing this code:
if __name__ == "__main__":
    query = "S&P 500 Index and its components."
    start = time.time()
    web_contents, serper_response = fetch_web_content(query)
    end1 = time.time()
    print("\nWeb crawling time:", end1 - start, "s")

    relevant_docs_list = embeddding_retrieval(web_contents, serper_response['links'], query)

    print("\n\nRelevant Documents from VectorDB:\n")
    print(relevant_docs_list)
    end2 = time.time()
    print("\nEmbedding time:", end2 - end1, "s")
