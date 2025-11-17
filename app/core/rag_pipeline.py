# rag_pipeline.py
# RAG infrastructure for managing submission vectorstore

import os
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv

from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()


class RAGPipeline:
    """RAG pipeline for indexing and retrieving student submissions."""

    def __init__(self,
                 persist_directory: Optional[str] = None,
                 embedding_model: str = "text-embedding-3-large",
                 llm_model: str = "gpt-4o-mini",
                 chunk_size: int = 1000,
                 chunk_overlap: int = 200):
        """
        Initialize RAG pipeline.

        Args:
            persist_directory: Directory to persist Chroma vectorstore
            embedding_model: OpenAI embedding model name
            llm_model: OpenAI LLM model name
            chunk_size: Text chunk size for splitting
            chunk_overlap: Overlap between chunks
        """
        self.persist_directory = persist_directory or "./chroma_db"
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Initialize embeddings and LLM
        self.embeddings = OpenAIEmbeddings(model=self.embedding_model, chunk_size=1)
        self.llm = ChatOpenAI(model=self.llm_model, temperature=0.2)

        # Initialize vectorstore
        self.vectorstore = None

        # Text splitter
        self.text_splitter = CharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len
        )

    def get_vectorstore(self, collection_name: str = "submissions_collection"):
        if self.vectorstore is not None:
            return self.vectorstore

        self.vectorstore = Chroma(
            collection_name=collection_name,
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
        return self.vectorstore

    def add_submission(self,
                       submission_id: str,
                       content: str,
                       metadata: Optional[Dict] = None):
        """
        Add a submission to the vectorstore.

        Args:
            submission_id: Unique identifier for the submission
            content: Submission text content
            metadata: Additional metadata (student_id, assignment_id, type, etc.)
        """
        vs = self.get_vectorstore()


        # Split text into chunks
        texts = self.text_splitter.create_documents([content])

        # Add submission_id + your metadata directly to the Document objects
        for doc in texts:
            doc.metadata = doc.metadata or {}
            doc.metadata.update(metadata or {})
            doc.metadata["submission_id"] = submission_id

        # Save to vectorstore
        vs.add_documents(texts)

        return True

    def add_multiple_submissions(self, submissions: List[Dict]):
        """
        Batch add multiple submissions.

        Args:
            submissions: List of dicts with keys: submission_id, content, metadata
        """
        for sub in submissions:
            self.add_submission(
                submission_id=sub['submission_id'],
                content=sub['content'],
                metadata=sub.get('metadata', {})
            )

    def query_similar_submissions(self,
                                  query: str,
                                  k: int = 4,
                                  filter_dict: Optional[Dict] = None):
        """
        Query for similar submission content.

        Args:
            query: Query text
            k: Number of results to return
            filter_dict: Metadata filters (e.g., {'assignment_id': 'assign_1', 'type': 'reference'})

        Returns:
            List of documents
        """
        vs = self.get_vectorstore()

        if filter_dict:
            results = vs.similarity_search(query, k=k, filter=filter_dict)
        else:
            results = vs.similarity_search(query, k=k)

        return results

    def get_context_for_submission(self,
                                   query: str,
                                   k: int = 3,
                                   filter_dict: Optional[Dict] = None) -> str:
        """
        Retrieve relevant context as formatted string.

        Args:
            query: Query to find relevant context
            k: Number of context chunks
            filter_dict: Metadata filters

        Returns:
            Formatted context string
        """
        docs = self.query_similar_submissions(query, k=k, filter_dict=filter_dict)
        return "\n\n".join([doc.page_content for doc in docs])

    def build_rag_chain(self, filter_dict: Optional[Dict] = None):
        """
        Build RAG chain for question answering over submissions.

        Args:
            filter_dict: Metadata filters for retrieval

        Returns:
            Runnable RAG chain
        """
        vs = self.get_vectorstore()
        search_kwargs = {'k': 4}
        if filter_dict:
            search_kwargs['filter'] = filter_dict

        retriever = vs.as_retriever(search_kwargs=search_kwargs)

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        prompt_template = """Use the context below to answer the question about student submissions. 
        If the context doesn't contain enough information, reply that you don't know.

        Context:
        {context}

        Question:
        {query}

        Answer:"""

        custom_rag_prompt = PromptTemplate.from_template(prompt_template)

        rag_chain = (
                {"context": retriever | format_docs, "query": RunnablePassthrough()}
                | custom_rag_prompt
                | self.llm
                | StrOutputParser()
        )
        return rag_chain

    def delete_submission(self, submission_id: str):
        """
        Delete a submission from vectorstore.

        Args:
            submission_id: ID of submission to delete
        """
        vs = self.get_vectorstore()
        # Delete by metadata filter
        vs.delete(where={"submission_id": submission_id})
        return True

    def list_submissions(self, filter_dict: Optional[Dict] = None) -> List[str]:
        """
        List all submission IDs in the vectorstore.

        Args:
            filter_dict: Optional metadata filter

        Returns:
            List of unique submission IDs
        """
        vs = self.get_vectorstore()
        # Get all documents
        all_docs = vs.get()

        # Extract unique submission IDs
        submission_ids = set()
        if all_docs and 'metadatas' in all_docs:
            for meta in all_docs['metadatas']:
                if meta and 'submission_id' in meta:
                    # Apply filter if provided
                    if filter_dict:
                        match = all(meta.get(k) == v for k, v in filter_dict.items())
                        if match:
                            submission_ids.add(meta['submission_id'])
                    else:
                        submission_ids.add(meta['submission_id'])

        return sorted(list(submission_ids))


# Convenience functions for backward compatibility
_default_pipeline = None


def get_pipeline(persist_directory: Optional[str] = None) -> RAGPipeline:
    """Get or create a default RAG pipeline instance."""
    global _default_pipeline
    if _default_pipeline is None:
        _default_pipeline = RAGPipeline(persist_directory=persist_directory)
    return _default_pipeline


def get_vectorstore(persist_directory: Optional[str] = None):
    """Legacy function - get vectorstore."""
    pipeline = get_pipeline(persist_directory)
    return pipeline.get_vectorstore()


def add_documents_to_vectorstore(docs: List[str], metadatas: Optional[List[Dict]] = None):
    """Legacy function - add documents to vectorstore."""
    pipeline = get_pipeline()
    vs = pipeline.get_vectorstore()
    vs.add_documents(documents=docs, metadatas=metadatas)


def query_docs(query: str, k: int = 4):
    """Legacy function - query documents."""
    pipeline = get_pipeline()
    return pipeline.query_similar_submissions(query, k=k)