"""Vector store management for tag content."""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from do_you_npc.vectorstore.loader import TextFileLoader


class VectorStoreManager:
    """Manages vector store creation and updates for tag content."""
    
    def __init__(self, project_root: Optional[str] = None):
        """Initialize the vector store manager.
        
        Args:
            project_root: Path to project root. If None, auto-detected.
        """
        if project_root is None:
            current_file = Path(__file__).resolve()
            project_root = current_file.parent.parent.parent
        
        self.project_root = Path(project_root)
        self.data_dir = self.project_root / "data"
        self.source_dir = self.data_dir / "source"
        self.vectorstore_dir = self.data_dir / "vectorstore"
        self.processed_dir = self.data_dir / "processed"
        
        # Ensure directories exist
        for directory in [self.data_dir, self.source_dir, self.vectorstore_dir, self.processed_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def clean_vectorstore(self) -> None:
        """Remove existing vectorstore if it exists."""
        if self.vectorstore_dir.exists():
            print(f"Removing existing vector store at: {self.vectorstore_dir}")
            shutil.rmtree(self.vectorstore_dir)
            self.vectorstore_dir.mkdir(parents=True, exist_ok=True)
    
    def get_last_updated(self) -> Optional[datetime]:
        """Get the timestamp of the last vector store update."""
        metadata_file = self.processed_dir / "last_updated.json"
        if not metadata_file.exists():
            return None
        
        try:
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                return datetime.fromisoformat(data['last_updated'])
        except (json.JSONDecodeError, KeyError, ValueError):
            return None
    
    def update_last_updated(self) -> None:
        """Update the last updated timestamp."""
        metadata_file = self.processed_dir / "last_updated.json"
        data = {
            'last_updated': datetime.now().isoformat(),
            'version': '1.0'
        }
        with open(metadata_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def needs_update(self) -> bool:
        """Check if vector store needs to be updated based on file timestamps."""
        last_updated = self.get_last_updated()
        if last_updated is None:
            return True
        
        # Check if any source files are newer than the last update
        for txt_file in self.source_dir.rglob("*.txt"):
            if datetime.fromtimestamp(txt_file.stat().st_mtime) > last_updated:
                return True
        
        return False
    
    def create_vectorstore(self, clean_start: bool = False, chunk_size: int = 1000, chunk_overlap: int = 200) -> Optional[Chroma]:
        """Create or update the vector store with tag content.
        
        Args:
            clean_start: Whether to start fresh by removing existing vectorstore
            chunk_size: Size of text chunks for embeddings
            chunk_overlap: Overlap between text chunks
            
        Returns:
            The created Chroma vectorstore or None if no documents found
        """
        if clean_start:
            self.clean_vectorstore()
        
        print(f"Loading documents from: {self.source_dir}")
        
        # Load all text files using our custom loader
        loader = TextFileLoader(self.source_dir)
        documents = loader.load_all_documents()
        
        if not documents:
            print("No text files found in the source directory!")
            return None
        
        print(f"Loaded {len(documents)} documents")
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
        )
        splits = text_splitter.split_documents(documents)
        print(f"Created {len(splits)} text chunks")
        
        # Create and persist the vectorstore
        print("Creating embeddings and vector store...")
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        
        if self.vectorstore_dir.exists() and any(self.vectorstore_dir.iterdir()):
            # Load existing vectorstore and add new documents
            vectorstore = Chroma(
                persist_directory=str(self.vectorstore_dir),
                embedding_function=embeddings
            )
            vectorstore.add_documents(splits)
        else:
            # Create new vectorstore
            vectorstore = Chroma.from_documents(
                documents=splits,
                embedding=embeddings,
                persist_directory=str(self.vectorstore_dir)
            )
        
        self.update_last_updated()
        print(f"Vector store created/updated and saved to: {self.vectorstore_dir}")
        return vectorstore
    
    def get_vectorstore(self) -> Optional[Chroma]:
        """Get the existing vectorstore, creating it if necessary."""
        if not self.vectorstore_dir.exists() or not any(self.vectorstore_dir.iterdir()):
            print("Vector store not found, creating...")
            return self.create_vectorstore()
        
        if self.needs_update():
            print("Vector store is outdated, updating...")
            return self.create_vectorstore(clean_start=False)
        
        # Load existing vectorstore
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        return Chroma(
            persist_directory=str(self.vectorstore_dir),
            embedding_function=embeddings
        )