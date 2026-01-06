import os
from typing import Tuple
import warnings

# suppress known benign chroma warning
warnings.filterwarnings("ignore", category=UserWarning)
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
    def retrieve(
        self,
        query: str,
        k: int = 3,
        min_score: float = 0.3
    ) -> Tuple[str, bool]:
        results = self.vectorstore.similarity_search_with_relevance_scores(
            query, k=k
        )

        relevant_docs = []

        for doc, score in results:
            score = max(0.0, min(score, 1.0))
            if score >= min_score:
                relevant_docs.append(doc.page_content)

        if not relevant_docs:
            return "", False

        return "\n\n".join(relevant_docs), True
