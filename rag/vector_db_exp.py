import chromadb
import pypdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

client = chromadb.PersistentClient(path="./chroma_db")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def extract_text_from_pdf(pdf_path):
    reader = pypdf.PdfReader(pdf_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def chunk_text(text, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_text(text)


def store_pdf_in_chroma(pdf_path, collection_name="pdf_documents"):
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)

    vector_store = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        client=client,
    )

    print(f"Stored {len(chunks)} chunks in Chroma collection '{collection_name}'.")
    print(f"{vector_store._collection.count()} vector stored.")

    return



store_pdf_in_chroma("datas/deekshith_hari_genai_resume.pdf")