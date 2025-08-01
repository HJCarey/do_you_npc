#!/usr/bin/env python3
"""Content management utility for Do You NPC text files."""

import argparse
import os
import sys
from pathlib import Path
from typing import List

from do_you_npc.vectorstore import TextFileLoader, VectorStoreManager


def list_campaigns():
    """List available campaigns."""
    manager = VectorStoreManager()
    loader = TextFileLoader(manager.source_dir)
    campaigns = loader.get_available_campaigns()
    
    if not campaigns:
        print("No campaigns found.")
        return
    
    print("Available campaigns:")
    for campaign in campaigns:
        print(f"  - {campaign}")
        tags = loader.get_available_tags(campaign)
        if tags:
            print(f"    Tags: {', '.join(tags[:5])}")
            if len(tags) > 5:
                print(f"    ... and {len(tags) - 5} more")


def list_tags(campaign: str = None):
    """List available tags for a campaign or globally."""
    manager = VectorStoreManager()
    loader = TextFileLoader(manager.source_dir)
    tags = loader.get_available_tags(campaign)
    
    if not tags:
        scope = f"campaign '{campaign}'" if campaign else "global tags"
        print(f"No tags found for {scope}.")
        return
    
    scope = f"Campaign '{campaign}'" if campaign else "Global tags"
    print(f"{scope}:")
    for tag in tags:
        print(f"  - {tag}")


def create_tag_file(tag_name: str, campaign: str = None):
    """Create a new tag file with a template."""
    manager = VectorStoreManager()
    
    if campaign:
        tag_dir = manager.source_dir / "campaigns" / campaign / "tags"
    else:
        tag_dir = manager.source_dir / "global" / "tags"
    
    tag_dir.mkdir(parents=True, exist_ok=True)
    tag_file = tag_dir / f"{tag_name}.txt"
    
    if tag_file.exists():
        print(f"Tag file already exists: {tag_file}")
        return
    
    # Create a simple template
    template = f"""# {tag_name.title()}

[Write your content for the '{tag_name}' tag here]

This content will be indexed in the vector store and made available to NPCs
who have this tag assigned to them.

Key information about {tag_name}:
- 
- 
- 

Background details:


Relationships and connections:

"""
    
    with open(tag_file, 'w') as f:
        f.write(template)
    
    print(f"Created tag file: {tag_file}")
    print(f"Edit this file to add content for the '{tag_name}' tag.")


def show_file_structure():
    """Show the current file structure."""
    manager = VectorStoreManager()
    source_dir = manager.source_dir
    
    print(f"Content directory structure: {source_dir}")
    print()
    
    if not source_dir.exists():
        print("Source directory does not exist yet.")
        return
    
    def print_tree(directory: Path, prefix: str = ""):
        """Print directory tree structure."""
        try:
            items = sorted(directory.iterdir())
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                current_prefix = "└── " if is_last else "├── "
                print(f"{prefix}{current_prefix}{item.name}")
                
                if item.is_dir() and item.name not in ['.git', '__pycache__']:
                    next_prefix = prefix + ("    " if is_last else "│   ")
                    print_tree(item, next_prefix)
        except PermissionError:
            print(f"{prefix}[Permission Denied]")
    
    print_tree(source_dir)


def update_vectorstore():
    """Update the vector store with current content."""
    manager = VectorStoreManager()
    
    print("Updating vector store...")
    vectorstore = manager.create_vectorstore(clean_start=False)
    
    if vectorstore:
        print("Vector store updated successfully!")
    else:
        print("No content found to update vector store.")


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Manage content files for Do You NPC",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage_content.py list-campaigns
  python manage_content.py list-tags
  python manage_content.py list-tags --campaign "my_campaign"
  python manage_content.py create-tag blacksmith
  python manage_content.py create-tag city_lore --campaign "my_campaign"
  python manage_content.py structure
  python manage_content.py update-vectorstore
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List campaigns
    list_campaigns_parser = subparsers.add_parser('list-campaigns', help='List available campaigns')
    
    # List tags
    list_tags_parser = subparsers.add_parser('list-tags', help='List available tags')
    list_tags_parser.add_argument('--campaign', help='Campaign name (omit for global tags)')
    
    # Create tag
    create_tag_parser = subparsers.add_parser('create-tag', help='Create a new tag file')
    create_tag_parser.add_argument('tag_name', help='Name of the tag to create')
    create_tag_parser.add_argument('--campaign', help='Campaign name (omit for global tag)')
    
    # Show structure
    structure_parser = subparsers.add_parser('structure', help='Show file structure')
    
    # Update vectorstore
    update_parser = subparsers.add_parser('update-vectorstore', help='Update vector store')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'list-campaigns':
            list_campaigns()
        elif args.command == 'list-tags':
            list_tags(args.campaign)
        elif args.command == 'create-tag':
            create_tag_file(args.tag_name, args.campaign)
        elif args.command == 'structure':
            show_file_structure()
        elif args.command == 'update-vectorstore':
            update_vectorstore()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()