#!/usr/bin/env python3
"""Create vector store for Do You NPC tag content.

This script creates a vector store from text files in the data/source directory.
It's designed to work with the new vectorstore module architecture.
"""

import os
from dotenv import load_dotenv
from do_you_npc.vectorstore import VectorStoreManager


def main():
    """Create the vector store using the new management system."""
    # Load environment variables (for Google API key)
    load_dotenv()
    
    # Verify Google API key is available
    if not os.getenv("GOOGLE_API_KEY"):
        print("Warning: GOOGLE_API_KEY not found in environment variables")
        print("Make sure to set your Google API key before running this script")
        return
    
    # Initialize the vector store manager
    manager = VectorStoreManager()
    
    print("Creating vector store for Do You NPC...")
    print(f"Source directory: {manager.source_dir}")
    print(f"Vector store directory: {manager.vectorstore_dir}")
    
    # Create the vector store with a clean start
    vectorstore = manager.create_vectorstore(clean_start=True)
    
    if vectorstore:
        print("\nVector store created successfully!")
        print("\nTo add content to your vector store:")
        print(f"1. Place .txt files in: {manager.source_dir}/global/tags/")
        print(f"2. Or organize by campaign: {manager.source_dir}/campaigns/[campaign_name]/tags/")
        print("3. Run this script again to update the vector store")
    else:
        print("\nNo documents found. Add .txt files to the source directory and try again.")
        print(f"Source directory: {manager.source_dir}")


if __name__ == "__main__":
    main()
