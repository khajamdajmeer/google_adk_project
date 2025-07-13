import uuid
import numpy as np
from typing import List, Dict, Any, Optional
from app.core.logging import get_logger

logger = get_logger(__name__, log_file="logs/app.log")

class Document:
    def __init__(self, text: str, metadata: Optional[Dict[str, Any]] = None):
        self.doc_id = str(uuid.uuid4())
        self.text = text
        self.metadata = metadata or {}
        self.embedding = None

class MedicalGuidelinesVectorStore:
    """
    A lightweight, in-memory vector store intended for RAG use-cases in the 
    Healthcare Agentic Backend (e.g. retrieving medical guidelines, billing codes, past patient notes).
    """

    def __init__(self):
        self.documents: Dict[str, Document] = {}
        logger.info("Initialized MedicalGuidelinesVectorStore")
        
    def _mock_embedder(self, text: str) -> np.ndarray:
        """
        Mock embedding function (returns a normalized random vector generated from text hash).
        In production, replace with Google GenAI embedder models (e.g. text-embedding-004) or similar.
        """
        # Create a deterministic mock embedding based on the hash of the text
        np.random.seed(abs(hash(text)) % (2**32))
        vec = np.random.rand(256)
        return vec / np.linalg.norm(vec)

    def add_document(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Adds a single document to the vector store.
        """
        doc = Document(text, metadata)
        doc.embedding = self._mock_embedder(text)
        self.documents[doc.doc_id] = doc
        logger.debug(f"Added document {doc.doc_id} to vector store.")
        return doc.doc_id

    def add_documents(self, texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None) -> List[str]:
        """
        Adds multiple documents to the vector store.
        """
        doc_ids = []
        metadatas = metadatas or [{} for _ in texts]
        for text, meta in zip(texts, metadatas):
            doc_ids.append(self.add_document(text, meta))
        return doc_ids

    def search(self, query: str, top_k: int = 3, threshold: float = 0.5) -> List[Dict[str, Any]]:
        """
        Searches the vector store using cosine similarity against the query.
        """
        if not self.documents:
            return []

        query_embedding = self._mock_embedder(query)
        results = []

        for doc in self.documents.values():
            # Cosine similarity
            score = np.dot(query_embedding, doc.embedding)
            if score >= threshold:
                results.append({
                    "doc_id": doc.doc_id,
                    "text": doc.text,
                    "metadata": doc.metadata,
                    "score": float(score)
                })

        # Sort by highest score first
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

# Singleton instance for the application to use
guidelines_vector_store = MedicalGuidelinesVectorStore()

def seed_default_guidelines():
    """Seed the vector store with some dummy healthcare guidelines for testing."""
    dummy_docs = [
        "Patient must fast for 12 hours prior to a lipid panel blood test.",
        "Standard dosage for Amoxicillin in adults is 500mg every 12 hours.",
        "To process an insurance claim for a routine physical, use billing code 99396.",
        "Symptoms of seasonal allergies include sneezing, runny nose, and red, watery, and itchy eyes."
    ]
    dummy_metadatas = [
        {"category": "lab_prep", "source": "Internal Medical DB"},
        {"category": "pharmacy", "source": "Drug Interactions API"},
        {"category": "billing", "source": "Claims Agent Reference"},
        {"category": "triage", "source": "Triage FAQ"}
    ]
    
    guidelines_vector_store.add_documents(dummy_docs, dummy_metadatas)
    logger.info("Seeded Medical Guidelines Vector Store with dummy data.")

# Auto-seed on import for immediate use in testing your agents
seed_default_guidelines()
