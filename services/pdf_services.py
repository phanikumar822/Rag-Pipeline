from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)


def extract_text(file_path: str):
    loader = PyPDFLoader(file_path)

    documents = loader.load()

    return documents


def create_chunks(documents):
    chunks = splitter.split_documents(documents)

    return chunks