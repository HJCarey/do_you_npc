"""LLM utility functions and chain setup."""
from typing import List, Tuple, Optional

import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI

from do_you_npc.vectorstore import VectorStoreManager, TagRetriever


def setup_retrieval_chain():
    """Initialize the retrieval chain with existing vector store.

    Returns:
        ConversationalRetrievalChain: The initialized chain, or None if setup fails
    """
    manager = VectorStoreManager()
    vectorstore = manager.get_vectorstore()

    if not vectorstore:
        st.error(
            "Vector store not found! Please run the __create_vectorstore.py script first."
        )
        return None

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        temperature=0.7,
        convert_system_message_to_human=True
    )

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True,
    )


def get_persona_context(persona_tags: List[str], campaign: str = None, 
                       additional_query: str = "") -> str:
    """Get relevant context for a persona based on their tags.
    
    Args:
        persona_tags: List of tag names assigned to the persona
        campaign: Campaign the persona belongs to
        additional_query: Optional additional context query
        
    Returns:
        Formatted context string for the persona
    """
    retriever = TagRetriever()
    relevant_content = retriever.get_relevant_tags_for_persona(
        persona_tags=persona_tags,
        query=additional_query,
        campaign=campaign,
        k=8
    )
    
    if not relevant_content:
        return "No additional context available."
    
    # Format the context nicely
    context_parts = []
    for tag_name, content in relevant_content:
        context_parts.append(f"**{tag_name}**: {content}")
    
    return "\n\n".join(context_parts)


def search_knowledge_base(query: str, campaign: str = None, k: int = 5) -> List[Tuple[str, str]]:
    """Search the knowledge base for relevant information.
    
    Args:
        query: Search query
        campaign: Optional campaign filter
        k: Number of results to return
        
    Returns:
        List of tuples (source, content)
    """
    retriever = TagRetriever()
    documents = retriever.search_tags(query, k=k, campaign=campaign)
    
    results = []
    for doc in documents:
        source = doc.metadata.get('tag_name', 'Unknown')
        if doc.metadata.get('campaign'):
            source = f"{doc.metadata['campaign']}: {source}"
        
        content = doc.page_content
        if len(content) > 500:
            content = content[:500] + "..."
            
        results.append((source, content))
    
    return results


def process_llm_response(result: dict, show_sources: bool = True):
    """Process and display an LLM response in a standardized way.

    Args:
        result: The result dictionary from the chain
        show_sources: Whether to show source references
    """
    st.write("### Answer:")
    st.write(result["answer"])

    if show_sources and "source_documents" in result:
        with st.expander("View Source References"):
            for i, doc in enumerate(result["source_documents"], 1):
                st.write(f"**Source {i}:**")
                # Get filename by taking everything after the last slash
                source_path = doc.metadata.get('source', 'Unknown source')
                filename = source_path[source_path.rfind('/') + 1:] if '/' in source_path else source_path
                source_info = f"**From:** {filename}"
                if 'page' in doc.metadata:
                    source_info += f", Page {doc.metadata['page']}"
                st.write(source_info)
                st.write(doc.page_content)
                st.write("---")
