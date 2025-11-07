import os
from pathlib import Path
from typing import List, Optional, Dict

from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

from ingest import DocumentIngester


class vectorStoreManager:
    # for vector storing operations (embedding generation and similarity search)
    
    def __init__(self, persist_directory: str = "./chroma_db", embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):

        # persist_directory: Directory to persist ChromaDB data
        # embedding_model: HuggingFace model for embeddings
        self.persist_directory = persist_directory #
        self.embedding_model_name = embedding_model
        self.vectorstore = None
        self.embeddings = None
        
    def _initialize_embeddings(self):
        # to initialize the embedding model
        if self.embeddings is None:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.embedding_model_name,
                model_kwargs={'device': 'cpu'},  # Use 'cuda' if GPU available
                encode_kwargs={'normalize_embeddings': True}
            )
        return self.embeddings
    
    def create_vectorstore(self, documents: List[Document], batch_size: int = 100) -> bool:

        # to create a new vector store from documents
        try:
            if not documents:
                return False
            
            # initialize embeddings
            embeddings = self._initialize_embeddings()
            
            # create vector store
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=embeddings,
                persist_directory=self.persist_directory,
                collection_name="skyro_knowledge"
            )
            
            # persist to disk
            self.vectorstore.persist()
            return True
            
        except Exception as e:
            return False
    
    def load_vectorstore(self) -> bool:

        # to load existing vector store from disk
        try:
            persist_path = Path(self.persist_directory)
            
            if not persist_path.exists():
                return False
            
            # Initialize embeddings
            embeddings = self._initialize_embeddings()
            
            # Load vector store
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=embeddings,
                collection_name="skyro_knowledge"
            )
            
            return True
            
        except Exception as e:
            return False
    
    def similarity_search(self, query: str, k: int = 5, filter_dict: Optional[Dict] = None) -> List[Document]:

        # to search for similar documents
        # k: Number of results to return
        if self.vectorstore is None:
            return []
        
        try:
            if filter_dict:
                results = self.vectorstore.similarity_search(
                    query, 
                    k=k, 
                    filter=filter_dict
                )
            else:
                results = self.vectorstore.similarity_search(query, k=k)
            
            return results
            
        except Exception as e:
            return []
    
    def similarity_search_with_score(self, query: str, k: int = 5) -> List[tuple]:
        # to search with relevance scores
        if self.vectorstore is None:
            return []
        
        try:
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            return results
            
        except Exception as e:
            return []
    
    def get_collection_stats(self) -> Dict:

        # to get statistics about the vector store collection
        if self.vectorstore is None:
            return {
                "total_documents": 0,
                "embedding_dimension": 0,
                "model_name": self.embedding_model_name,
                "status": "not_loaded"
            }
        
        try:
            # get collection
            collection = self.vectorstore._collection
            count = collection.count()
            
            return {
                "total_documents": count,
                "embedding_dimension": 384,  # all-MiniLM-L6-v2 dimension
                "model_name": self.embedding_model_name,
                "persist_directory": self.persist_directory,
                "status": "loaded"
            }
            
        except Exception as e:
            return {
                "total_documents": 0,
                "embedding_dimension": 0,
                "model_name": self.embedding_model_name,
                "status": "error"
            }
    
    def delete_vectorstore(self) -> bool:
        # to delete vector store
        try:
            import shutil
            persist_path = Path(self.persist_directory)
            
            if persist_path.exists():
                shutil.rmtree(persist_path)
                self.vectorstore = None
                return True
            else:
                return False
                
        except Exception as e:
            return False
