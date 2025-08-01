"""Text file loading and processing for vector store."""

import os
from pathlib import Path
from typing import List, Dict, Any

from langchain.schema import Document


class TextFileLoader:
    """Loads and processes text files from the data source directory."""
    
    def __init__(self, source_dir: Path):
        """Initialize the loader with a source directory.
        
        Args:
            source_dir: Path to the directory containing text files
        """
        self.source_dir = Path(source_dir)
    
    def _extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract metadata from file path structure.
        
        Args:
            file_path: Path to the text file
            
        Returns:
            Dictionary containing metadata about the file
        """
        # Get relative path from source directory
        rel_path = file_path.relative_to(self.source_dir)
        parts = rel_path.parts
        
        metadata = {
            'source': str(file_path),
            'filename': file_path.name,
            'file_stem': file_path.stem,  # filename without extension
        }
        
        # Determine if it's a campaign-specific or global tag
        if parts[0] == 'campaigns' and len(parts) >= 4:
            # campaigns/[campaign_name]/tags/[tag_name].txt
            metadata['type'] = 'campaign_tag'
            metadata['campaign'] = parts[1]
            metadata['tag_name'] = file_path.stem
        elif parts[0] == 'global' and len(parts) >= 3:
            # global/tags/[tag_name].txt
            metadata['type'] = 'global_tag'
            metadata['campaign'] = None
            metadata['tag_name'] = file_path.stem
        else:
            # Unstructured file
            metadata['type'] = 'other'
            metadata['campaign'] = None
            metadata['tag_name'] = file_path.stem
        
        # Add file size and modification time
        stat = file_path.stat()
        metadata['file_size'] = stat.st_size
        metadata['modified'] = stat.st_mtime
        
        return metadata
    
    def load_document(self, file_path: Path) -> Document:
        """Load a single text file as a Document.
        
        Args:
            file_path: Path to the text file
            
        Returns:
            Document object with content and metadata
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        metadata = self._extract_metadata(file_path)
        
        return Document(
            page_content=content,
            metadata=metadata
        )
    
    def load_tag_documents(self, tag_name: str, campaign: str = None) -> List[Document]:
        """Load all documents for a specific tag.
        
        Args:
            tag_name: Name of the tag to load
            campaign: Campaign name, or None for global tags
            
        Returns:
            List of Document objects for the tag
        """
        documents = []
        
        if campaign:
            # Look in campaign-specific directory
            tag_dir = self.source_dir / "campaigns" / campaign / "tags"
        else:
            # Look in global directory
            tag_dir = self.source_dir / "global" / "tags"
        
        if not tag_dir.exists():
            return documents
        
        # Look for single file: tag_name.txt
        single_file = tag_dir / f"{tag_name}.txt"
        if single_file.exists():
            documents.append(self.load_document(single_file))
        
        # Look for directory with multiple files: tag_name/
        multi_dir = tag_dir / tag_name
        if multi_dir.exists() and multi_dir.is_dir():
            for txt_file in multi_dir.glob("*.txt"):
                documents.append(self.load_document(txt_file))
        
        return documents
    
    def load_campaign_documents(self, campaign: str) -> List[Document]:
        """Load all documents for a specific campaign.
        
        Args:
            campaign: Name of the campaign
            
        Returns:
            List of Document objects for the campaign
        """
        documents = []
        campaign_dir = self.source_dir / "campaigns" / campaign / "tags"
        
        if not campaign_dir.exists():
            return documents
        
        # Load all .txt files in the campaign tags directory
        for txt_file in campaign_dir.rglob("*.txt"):
            documents.append(self.load_document(txt_file))
        
        return documents
    
    def load_all_documents(self) -> List[Document]:
        """Load all text documents from the source directory.
        
        Returns:
            List of all Document objects found
        """
        documents = []
        
        # Load all .txt files recursively
        for txt_file in self.source_dir.rglob("*.txt"):
            try:
                documents.append(self.load_document(txt_file))
            except Exception as e:
                print(f"Error loading {txt_file}: {e}")
                continue
        
        return documents
    
    def get_available_tags(self, campaign: str = None) -> List[str]:
        """Get list of available tag names.
        
        Args:
            campaign: Campaign name, or None for global tags
            
        Returns:
            List of available tag names
        """
        tags = set()
        
        if campaign:
            tag_dir = self.source_dir / "campaigns" / campaign / "tags"
        else:
            tag_dir = self.source_dir / "global" / "tags"
        
        if not tag_dir.exists():
            return []
        
        # Find single files
        for txt_file in tag_dir.glob("*.txt"):
            tags.add(txt_file.stem)
        
        # Find directories
        for item in tag_dir.iterdir():
            if item.is_dir() and any(item.glob("*.txt")):
                tags.add(item.name)
        
        return sorted(list(tags))
    
    def get_available_campaigns(self) -> List[str]:
        """Get list of available campaign names.
        
        Returns:
            List of campaign names that have tag data
        """
        campaigns = []
        campaigns_dir = self.source_dir / "campaigns"
        
        if not campaigns_dir.exists():
            return campaigns
        
        for item in campaigns_dir.iterdir():
            if item.is_dir():
                tags_dir = item / "tags"
                if tags_dir.exists() and any(tags_dir.rglob("*.txt")):
                    campaigns.append(item.name)
        
        return sorted(campaigns)