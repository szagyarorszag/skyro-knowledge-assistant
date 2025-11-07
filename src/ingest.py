
# document ingestion module for Skyro Knowledge Assistant - loads and preprocess of multiple formats like md, pdf and docx with overchunkin

import os
from pathlib import Path
from typing import List, Dict

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.document_loaders import (
    UnstructuredMarkdownLoader,
    PyPDFLoader,
    Docx2txtLoader
)


class DocumentIngester:
    # to load and chunks documents for vector store ingestion
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):

        # chunk_size: Size of text chunks in characters
        # chunk_overlap: Overlap between chunks to maintain context
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def load_document(self, file_path: str) -> List[Document]:

        # to just load docs
        file_path = Path(file_path)
        
        if not file_path.exists():
            return []
        
        # determine loader based on file extension
        extension = file_path.suffix.lower()
        
        try:
            if extension == '.md':
                loader = UnstructuredMarkdownLoader(str(file_path))
            elif extension == '.pdf':
                loader = PyPDFLoader(str(file_path))
            elif extension == '.docx':
                loader = Docx2txtLoader(str(file_path))
            else:
                return []
            
            # load document
            documents = loader.load()
            
            # add metadata
            for doc in documents:
                doc.metadata.update({
                    'source': str(file_path.name),
                    'file_type': extension[1:],  # remove the dot
                    'category': self._get_category(file_path),
                    'full_path': str(file_path)
                })
            
            return documents
            
        except Exception as e:
            return []
    
    def load_documents_from_directory(self, directory: str, exclude_files: List[str] = None) -> List[Document]:

        # to load docs from certain dir
        if exclude_files is None:
            exclude_files = []
        
        directory = Path(directory)
        all_documents = []
        
        # supported extensions
        supported_extensions = ['.md', '.pdf', '.docx']
        
        # find all files
        for ext in supported_extensions:
            files = list(directory.rglob(f'*{ext}'))
            
            for file_path in files:
                # skip excluded files
                if file_path.name in exclude_files:
                    continue
                
                # skip overview/summary files
                if file_path.name.upper() in ['DATASET_OVERVIEW.md', 'FILE_FORMATS_SUMMARY.md']:
                    continue
                
                docs = self.load_document(str(file_path))
                all_documents.extend(docs)
        
        return all_documents
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:

        # to split documents into smaller chunks for better retrieval.
        
        chunked_docs = self.text_splitter.split_documents(documents)
        
        # Add chunk metadata
        for i, doc in enumerate(chunked_docs):
            doc.metadata['chunk_id'] = i
        
        return chunked_docs
    
    def _get_category(self, file_path: Path) -> str:

        # to determine document category based on directory structure
        
        # get parent directory name as category
        parent = file_path.parent.name
        
        category_map = {
            'business': 'Business & Strategy',
            'compliance': 'Compliance',
            'experiments': 'Experiments & Results',
            'meetings': 'Meetings & Planning',
            'onboarding': 'Onboarding & Training',
            'operations': 'Operations',
            'product_specs': 'Product Specifications',
            'security': 'Security',
            'support': 'Customer Support',
            'technical': 'Technical Documentation'
        }
        
        return category_map.get(parent, 'General')
    
    def get_statistics(self, documents: List[Document]) -> Dict:

        # to get statistics about loaded documents.
        stats = {
            'total_documents': len(documents),
            'total_characters': sum(len(doc.page_content) for doc in documents),
            'by_type': {},
            'by_category': {}
        }
        
        for doc in documents:
            # count by file type
            file_type = doc.metadata.get('file_type', 'unknown')
            stats['by_type'][file_type] = stats['by_type'].get(file_type, 0) + 1
            
            # count by category
            category = doc.metadata.get('category', 'unknown')
            stats['by_category'][category] = stats['by_category'].get(category, 0) + 1
        
        return stats
