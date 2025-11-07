import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

from langchain.schema import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from vectorstore import VectorStoreManager

load_dotenv()

# document permissions control
ROLE_PERMISSIONS = {
    "Admin": ["all"],
    "Engineering": ["Technical Documentation", "Product Specifications", "Experiments & Results", "Meetings & Planning"],
    "Finance": ["Business & Strategy", "Meetings & Planning"],
    "Compliance": ["Compliance", "Security", "Business & Strategy"],
    "Operations": ["Operations", "Customer Support", "Meetings & Planning"],
    "Support": ["Customer Support", "Product Specifications", "Operations"],
    "Executive": ["Business & Strategy", "Meetings & Planning", "Experiments & Results"]
}


class RAGRetriever:
    # question-answering system using retrieval-augmented generation 
    def __init__(self, 
                 vectorstore_manager: VectorStoreManager,
                 model_name: str = "gemini-2.5-flash",
                 temperature: float = 0.2):

        # initialize RAG retriever.
        # vectorstore_manager: Initialized VectorStoreManager instance
        # model_name: Name of the LLM model to use
        # temperature: LLM temperature (0.0 = deterministic, 1.0 = creative)
        self.vectorstore_manager = vectorstore_manager
        self.model_name = model_name
        self.temperature = temperature
        self.llm = None
        
        api_key = os.getenv("GEMINI_API_KEY")
        
        self._initialize_llm()
    
    def _initialize_llm(self):
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            
            self.llm = ChatGoogleGenerativeAI(
                model=self.model_name,
                temperature=self.temperature,
                convert_system_message_to_human=True,
                google_api_key=api_key
            )
        except Exception as e:
            raise
    
    def _create_prompt_template(self) -> PromptTemplate:

        # to create the prompt template for question answering
        template = """You are an assistant for Skyro's internal knowledge base. Answer questions using only the provided documentation context.

CONTEXT:
{context}

QUESTION: {question}

Guidelines:
- Base answers strictly on the provided context
- State clearly if information is insufficient
- Reference specific details and source documents when applicable
- Use professional language
- Structure answers with bullet points or paragraphs as needed

ANSWER:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
    
    def _format_context(self, documents: List[Document]) -> str:

        # to format retrieved documents into context string
        context_parts = []
        
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get('source', 'Unknown')
            category = doc.metadata.get('category', 'General')
            content = doc.page_content.strip()
            
            context_parts.append(
                f"[Document {i} - {source} ({category})]\n{content}\n"
            )
        
        return "\n".join(context_parts)
    
    def _extract_sources(self, documents: List[Document]) -> List[Dict]:

        # to extract unique source information from documents.
        seen_sources = set()
        sources = []
        
        for doc in documents:
            source_name = doc.metadata.get('source', 'Unknown')
            
            if source_name not in seen_sources:
                seen_sources.add(source_name)
                sources.append({
                    'name': source_name,
                    'category': doc.metadata.get('category', 'General'),
                    'type': doc.metadata.get('file_type', 'unknown')
                })
        
        return sources
    
    def query(self, question: str, k: int = 5) -> Dict:

        # so simple query interface that returns just the answer
        result = self.query_with_context(question, k)
        return {
            "answer": result["answer"],
            "error": result["error"]
        }
    
    def query_with_context(self, question: str, k: int = 5, user_role: str = "Admin") -> Dict:

        # so query the knowledge base and generate an answer with full context
        try:
            # validate inputs
            if not question or not question.strip():
                return {
                    "answer": "Please provide a valid question.",
                    "sources": [],
                    "chunks": [],
                    "error": True
                }
            
            if self.vectorstore_manager.vectorstore is None:
                return {
                    "answer": "Vector store not loaded. Please ensure vectorstore.py has been run.",
                    "sources": [],
                    "chunks": [],
                    "error": True
                }
            
            # retrieve relevant documents
            docs_with_scores = self.vectorstore_manager.similarity_search_with_score(
                question, 
                k=k
            )
            
            if not docs_with_scores:
                return {
                    "answer": "I couldn't find any relevant information in the knowledge base to answer your question.",
                    "sources": [],
                    "chunks": [],
                    "error": False
                }
            
            # separate documents and scores
            documents = [doc for doc, score in docs_with_scores]
            scores = [score for doc, score in docs_with_scores]
            
            # apply access control filtering
            allowed_categories = ROLE_PERMISSIONS.get(user_role, [])
            if "all" not in allowed_categories:
                filtered_docs = []
                filtered_scores = []
                for doc, score in zip(documents, scores):
                    doc_category = doc.metadata.get('category', 'General')
                    if doc_category in allowed_categories:
                        filtered_docs.append(doc)
                        filtered_scores.append(score)
                
                if not filtered_docs:
                    return {
                        "answer": "No access",
                        "sources": [],
                        "chunks": [],
                        "error": False
                    }
                
                documents = filtered_docs
                scores = filtered_scores
            
            # format context for LLM
            context = self._format_context(documents)
            
            # create prompt
            prompt_template = self._create_prompt_template()
            
            # generate answer
            chain = LLMChain(llm=self.llm, prompt=prompt_template)
            
            response = chain.run(
                context=context,
                question=question
            )
            
            # xxtract sources
            sources = self._extract_sources(documents)
            
            # format chunks for display
            chunks = []
            for i, (doc, score) in enumerate(zip(documents, scores), 1):
                chunks.append({
                    'rank': i,
                    'source': doc.metadata.get('source', 'Unknown'),
                    'category': doc.metadata.get('category', 'General'),
                    'score': float(score),  # convert to float for JSON serialization
                    'preview': doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content
                })
            
            return {
                "answer": response.strip(),
                "sources": sources,
                "chunks": chunks,
                "error": False
            }
            
        except Exception as e:
            return {
                "answer": f"An error occurred: {str(e)}",
                "sources": [],
                "chunks": [],
                "error": True
            }
