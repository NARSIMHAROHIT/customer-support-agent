import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

DATA_DIR = "data/documents"
VECTOR_DB_DIR = "data/vector_db"


class RAG:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vectorstore = Chroma(
            persist_directory=VECTOR_DB_DIR,
            embedding_function=self.embeddings
        )

    def ingest(self):
        documents = []

        for file in os.listdir(DATA_DIR):
            if file.endswith(".txt"):
                loader = TextLoader(os.path.join(DATA_DIR, file))
                documents.extend(loader.load())

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        chunks = splitter.split_documents(documents)

        Chroma.from_documents(
            chunks,
            embedding=self.embeddings,
            persist_directory=VECTOR_DB_DIR
        )

    def retrieve(self, query: str, k: int = 3) -> str:
        docs = self.vectorstore.similarity_search(query, k=k)
        return "\n\n".join(doc.page_content for doc in docs)
