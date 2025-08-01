#!/usr/bin/env python3
"""
Test and demonstration script for the Do You NPC vector store system.

This script demonstrates the complete workflow:
1. How text files are organized and loaded
2. How the vector store system works
3. How personas get context from their tags
4. How to search the knowledge base

Run this script to see the system in action without needing OpenAI API keys.
"""

import os
from pathlib import Path

def demonstrate_file_organization():
    """Show how the file organization system works."""
    print("=== FILE ORGANIZATION SYSTEM ===")
    print()
    
    # Show the directory structure
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data" / "source"
    
    print("Directory Structure:")
    print("data/source/")
    print("├── global/tags/          # Campaign-independent content")
    print("│   ├── blacksmith.txt    # Generic blacksmith knowledge")
    print("│   ├── tavern.txt        # Generic tavern information")
    print("│   └── merchant.txt      # Generic merchant details")
    print("└── campaigns/")
    print("    └── [campaign_name]/tags/")
    print("        ├── city_name.txt      # Specific city lore")
    print("        ├── local_politics.txt # Campaign-specific politics")
    print("        └── regional_history.txt")
    print()
    
    # Show what files actually exist
    if data_dir.exists():
        print("Current files in your system:")
        for txt_file in data_dir.rglob("*.txt"):
            rel_path = txt_file.relative_to(data_dir)
            file_size = txt_file.stat().st_size
            print(f"  {rel_path} ({file_size} bytes)")
    else:
        print("Data directory doesn't exist yet - files will be created here.")
    print()


def demonstrate_text_loading():
    """Show how text files are loaded and processed."""
    print("=== TEXT FILE LOADING ===")
    print()
    
    try:
        from do_you_npc.vectorstore.loader import TextFileLoader
        
        project_root = Path(__file__).parent
        source_dir = project_root / "data" / "source"
        
        if not source_dir.exists():
            print("No source directory found. The loader would create it automatically.")
            return
        
        loader = TextFileLoader(source_dir)
        
        # Show available campaigns
        campaigns = loader.get_available_campaigns()
        print(f"Available campaigns: {campaigns}")
        
        # Show global tags
        global_tags = loader.get_available_tags(campaign=None)
        print(f"Global tags: {global_tags}")
        
        # Show campaign-specific tags
        for campaign in campaigns:
            campaign_tags = loader.get_available_tags(campaign=campaign)
            print(f"Tags for '{campaign}': {campaign_tags}")
        
        # Load a sample document if available
        if global_tags:
            documents = loader.load_tag_documents(global_tags[0])
            if documents:
                doc = documents[0]
                print(f"\nSample document metadata for '{global_tags[0]}':")
                for key, value in doc.metadata.items():
                    print(f"  {key}: {value}")
                print(f"Content preview: {doc.page_content[:200]}...")
        
    except ImportError as e:
        print(f"Could not import vectorstore modules: {e}")
        print("This is expected if langchain dependencies aren't installed yet.")
    
    print()


def demonstrate_persona_context_concept():
    """Show how persona context would work conceptually."""
    print("=== PERSONA CONTEXT CONCEPT ===")
    print()
    
    # Example persona from your database
    example_persona = {
        'name': 'Gareth the Smith',
        'backstory': 'A veteran blacksmith who fought in the border wars',
        'personality': 'Gruff but fair, values hard work and craftsmanship',
        'tags': ['blacksmith', 'silverbrook_city', 'veteran']
    }
    
    print("Example Persona:")
    for key, value in example_persona.items():
        print(f"  {key}: {value}")
    print()
    
    print("How context retrieval would work:")
    print("1. When an NPC needs to respond, we look at their assigned tags")
    print("2. For each tag, we retrieve relevant content from the vector store")
    print("3. This content is compressed and added to the LLM prompt")
    print()
    
    print("For Gareth with tags ['blacksmith', 'silverbrook_city', 'veteran']:")
    print("- 'blacksmith' tag would provide: metalworking knowledge, tools, trade connections")
    print("- 'silverbrook_city' tag would provide: local geography, politics, recent events")
    print("- 'veteran' tag would provide: military experience, war stories, combat knowledge")
    print()
    
    print("The LLM prompt would look like:")
    print("'''")
    print("You are Gareth the Smith. Your backstory: A veteran blacksmith who fought in the border wars")
    print("Your personality: Gruff but fair, values hard work and craftsmanship")
    print()
    print("Relevant knowledge you have:")
    print("**blacksmith**: [metalworking techniques, tool maintenance, etc...]")
    print("**silverbrook_city**: [city layout, recent trade disputes, etc...]")
    print("**veteran**: [military tactics, war experiences, etc...]")
    print()
    print("Respond to: 'Can you tell me about the recent troubles in the city?'")
    print("'''")
    print()


def demonstrate_workflow():
    """Show the complete intended workflow."""
    print("=== COMPLETE WORKFLOW ===")
    print()
    
    print("Step 1: Content Creation")
    print("- User creates .txt files with game world information")
    print("- Files are organized by campaign/global scope")
    print("- Example: data/source/campaigns/my_campaign/tags/important_city.txt")
    print()
    
    print("Step 2: Vector Store Creation")
    print("- Run: python do_you_npc/__create_vectorstore.py")
    print("- System reads all .txt files")
    print("- Creates embeddings and stores them in data/vectorstore/")
    print("- Tracks metadata about each piece of content")
    print()
    
    print("Step 3: Database Integration")
    print("- Personas in your database have assigned tags")
    print("- Tags in database have small 'text_body' for direct storage")
    print("- Large content for tags lives in .txt files")
    print()
    
    print("Step 4: Runtime Context Retrieval")
    print("- When NPC needs to respond, system looks at their tags")
    print("- For each tag, retrieves relevant content from vector store")
    print("- Content is automatically compressed to fit in LLM context")
    print("- NPC gets rich background knowledge without bloating database")
    print()
    
    print("Step 5: Query and Search")
    print("- Can search knowledge base: 'What do we know about trade routes?'")
    print("- Can get tag summaries: 'Summarize what blacksmiths know'")
    print("- Can filter by campaign: 'What's happening in Silverbrook City?'")
    print()


def show_example_files():
    """Show what the example files contain."""
    print("=== EXAMPLE FILES ===")
    print()
    
    project_root = Path(__file__).parent
    
    # Show blacksmith example
    blacksmith_file = project_root / "data" / "source" / "global" / "tags" / "blacksmith.txt"
    if blacksmith_file.exists():
        print("Global tag 'blacksmith.txt' contains:")
        with open(blacksmith_file) as f:
            content = f.read()
            lines = content.split('\n')
            for i, line in enumerate(lines[:10]):  # Show first 10 lines
                print(f"  {line}")
            if len(lines) > 10:
                print(f"  ... and {len(lines) - 10} more lines")
        print()
    
    # Show city example
    city_file = project_root / "data" / "source" / "campaigns" / "example_campaign" / "tags" / "silverbrook_city.txt"
    if city_file.exists():
        print("Campaign tag 'silverbrook_city.txt' contains:")
        with open(city_file) as f:
            content = f.read()
            lines = content.split('\n')
            for i, line in enumerate(lines[:8]):  # Show first 8 lines
                print(f"  {line}")
            if len(lines) > 8:
                print(f"  ... and {len(lines) - 8} more lines")
        print()


def check_dependencies():
    """Check what dependencies are available."""
    print("=== DEPENDENCY CHECK ===")
    print()
    
    dependencies = [
        ("langchain", "for text processing and chains"),
        ("langchain_chroma", "for vector store"),
        ("langchain_openai", "for OpenAI integration"),
        ("openai", "for API access"),
    ]
    
    for package, description in dependencies:
        try:
            __import__(package)
            print(f"✓ {package} - {description}")
        except ImportError:
            print(f"✗ {package} - {description} (not installed)")
    
    print()
    print("To install missing dependencies:")
    print("pip install langchain langchain-chroma langchain-openai openai")
    print()


def main():
    """Run the complete demonstration."""
    print("DO YOU NPC - VECTOR STORE SYSTEM DEMONSTRATION")
    print("=" * 60)
    print()
    
    demonstrate_file_organization()
    show_example_files()
    demonstrate_text_loading()
    demonstrate_persona_context_concept()
    demonstrate_workflow()
    check_dependencies()
    
    print("=== NEXT STEPS ===")
    print()
    print("1. Install dependencies if needed:")
    print("   pip install langchain langchain-chroma langchain-openai openai")
    print()
    print("2. Set OpenAI API key:")
    print("   export OPENAI_API_KEY='your-key-here'")
    print()
    print("3. Create vector store:")
    print("   python do_you_npc/__create_vectorstore.py")
    print()
    print("4. Try the management utility:")
    print("   python do_you_npc/manage_content.py structure")
    print("   python do_you_npc/manage_content.py list-tags")
    print()
    print("5. Add your own content:")
    print("   python do_you_npc/manage_content.py create-tag your_tag_name")


if __name__ == "__main__":
    main()