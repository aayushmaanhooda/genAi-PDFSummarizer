import os
import streamlit as st
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain_community.llms import OpenAI
from langchain_community.embeddings import OpenAIEmbeddings

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="PDF Summarizer", layout="wide")
st.title("PDF Summarizer (Gen AI)")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
if uploaded_file:
    with st.spinner("Reading PDF..."):
        pdf_path = f"temp_{uploaded_file.name}"
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        loader = PDFPlumberLoader(pdf_path)
        docs = loader.load()
        st.success(f"Loaded {len(docs)} pages from PDF.")

        # Optional: split into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.split_documents(docs)
        st.success(f"Split PDF into {len(docs)} chunks.")

    with st.spinner("Embedding and indexing..."):
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        vectordb = FAISS.from_documents(docs, embeddings)
        st.success("PDF embedded and indexed!")

    os.remove(pdf_path)

    llm = OpenAI(openai_api_key=openai_api_key, temperature=0.6)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectordb.as_retriever(),
        return_source_documents=True,
    )

    st.header("Ask anything about your PDF!")
    question = st.text_input("Your question:")
    if question:
        with st.spinner("Generating answer..."):
            result = qa_chain.invoke({"query": question})
            st.write("**Answer:**", result["result"])
