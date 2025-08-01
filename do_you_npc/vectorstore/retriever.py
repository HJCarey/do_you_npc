"""Query and retrieval functions for tag content."""

from typing import List, Dict, Any, Optional, Tuple

from langchain.schema import Document
from langchain_chroma import Chroma

from do_you_npc.vectorstore.manager import VectorStoreManager


class TagRetriever:
    """Handles queries and retrieval of tag content from vector store."""
    
    def __init__(self, project_root: Optional[str] = None):
        """Initialize the retriever.
        
        Args:
            project_root: Path to project root. If None, auto-detected.
        """
        self.manager = VectorStoreManager(project_root)
        self._vectorstore = None
    
    @property
    def vectorstore(self) -> Optional[Chroma]:
        """Get the vector store, loading it if necessary."""
        if self._vectorstore is None:
            self._vectorstore = self.manager.get_vectorstore()
        return self._vectorstore
    
    def refresh_vectorstore(self) -> None:
        """Force refresh of the vector store."""
        self._vectorstore = None
        self._vectorstore = self.manager.get_vectorstore()
    
    def search_tags(self, query: str, k: int = 5, campaign: str = None) -> List[Document]:
        """Search for relevant tag content based on a query.
        
        Args:
            query: Search query string
            k: Number of results to return
            campaign: Optional campaign filter
            
        Returns:
            List of relevant Document objects
        """
        if not self.vectorstore:
            return []
        
        # Build search filter if campaign is specified
        search_kwargs = {"k": k}
        if campaign:
            search_kwargs["filter"] = {"campaign": campaign}
        
        return self.vectorstore.similarity_search(query, **search_kwargs)
    
    def search_by_tag_name(self, tag_name: str, campaign: str = None, k: int = 10) -> List[Document]:
        """Search for content from a specific tag.
        
        Args:
            tag_name: Name of the tag to search for
            campaign: Optional campaign filter
            k: Number of results to return
            
        Returns:
            List of Document objects from the specified tag
        """
        if not self.vectorstore:
            return []
        
        # Build filter for tag name and optionally campaign
        filter_dict = {"tag_name": tag_name}
        if campaign:
            filter_dict["campaign"] = campaign
        
        return self.vectorstore.similarity_search(
            tag_name,  # Use tag name as query
            k=k,
            filter=filter_dict
        )
    
    def get_tag_summary(self, tag_name: str, campaign: str = None, max_length: int = 500) -> str:
        """Get a summary of a tag's content.
        
        Args:
            tag_name: Name of the tag
            campaign: Optional campaign filter
            max_length: Maximum length of summary
            
        Returns:
            Summary string of the tag's content
        """
        documents = self.search_by_tag_name(tag_name, campaign, k=3)
        
        if not documents:
            return f"No content found for tag '{tag_name}'"
        
        # Combine content from top documents
        combined_content = ""
        for doc in documents:
            combined_content += doc.page_content + "\n\n"
        
        # Truncate if too long
        if len(combined_content) > max_length:
            combined_content = combined_content[:max_length] + "..."
        
        return combined_content.strip()
    
    def get_relevant_tags_for_persona(self, persona_tags: List[str], query: str = "", 
                                    campaign: str = None, k: int = 10) -> List[Tuple[str, str]]:
        """Get relevant tag content for a persona based on their assigned tags.
        
        Args:
            persona_tags: List of tag names assigned to the persona
            query: Optional additional query context
            campaign: Campaign the persona belongs to
            k: Maximum number of content pieces to return
            
        Returns:
            List of tuples (tag_name, content) with relevant information
        """
        if not self.vectorstore:
            return []
        
        relevant_content = []
        
        # Get content for each assigned tag
        for tag_name in persona_tags:
            documents = self.search_by_tag_name(tag_name, campaign, k=2)
            for doc in documents:
                # Truncate content to reasonable length for context
                content = doc.page_content
                if len(content) > 300:
                    content = content[:300] + "..."
                relevant_content.append((tag_name, content))
        
        # If we have additional query context, search for more relevant content
        if query and len(relevant_content) < k:
            additional_docs = self.search_tags(
                query, 
                k=k - len(relevant_content), 
                campaign=campaign
            )
            for doc in additional_docs:
                tag_name = doc.metadata.get('tag_name', 'unknown')
                content = doc.page_content
                if len(content) > 300:
                    content = content[:300] + "..."
                relevant_content.append((tag_name, content))
        
        return relevant_content[:k]
    
    def get_available_tags(self, campaign: str = None) -> List[str]:
        """Get list of available tags in the vector store.
        
        Args:
            campaign: Optional campaign filter
            
        Returns:
            List of available tag names
        """
        # Use the loader to get available tags from file system
        from .loader import TextFileLoader
        loader = TextFileLoader(self.manager.source_dir)
        return loader.get_available_tags(campaign)
    
    def get_tag_metadata(self, tag_name: str, campaign: str = None) -> Dict[str, Any]:
        """Get metadata about a specific tag.
        
        Args:
            tag_name: Name of the tag
            campaign: Optional campaign filter
            
        Returns:
            Dictionary with tag metadata
        """
        documents = self.search_by_tag_name(tag_name, campaign, k=1)
        
        if not documents:
            return {}
        
        # Return metadata from the first document
        metadata = documents[0].metadata.copy()
        
        # Add content statistics
        all_docs = self.search_by_tag_name(tag_name, campaign, k=100)
        total_content = sum(len(doc.page_content) for doc in all_docs)
        
        metadata.update({
            'total_documents': len(all_docs),
            'total_content_length': total_content,
            'average_chunk_size': total_content // len(all_docs) if all_docs else 0
        })
        
        return metadata