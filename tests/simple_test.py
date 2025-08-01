#!/usr/bin/env python3
"""
Simple test of the vectorstore system without requiring LLM dependencies.
This shows the file loading and organization parts of the system.
"""

import sys
from pathlib import Path

# Add the project root to Python path so we can import our modules
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_file_loading():
    """Test the text file loading system."""
    print("=== TESTING FILE LOADING SYSTEM ===")
    print()
    
    try:
        from do_you_npc.vectorstore.loader import TextFileLoader
        
        source_dir = project_root / "data" / "source"
        loader = TextFileLoader(source_dir)
        
        print(f"Source directory: {source_dir}")
        print(f"Directory exists: {source_dir.exists()}")
        print()
        
        # Test campaign discovery
        campaigns = loader.get_available_campaigns()
        print(f"Available campaigns: {campaigns}")
        
        # Test global tags
        global_tags = loader.get_available_tags(campaign=None)
        print(f"Global tags: {global_tags}")
        
        # Test campaign tags
        for campaign in campaigns:
            campaign_tags = loader.get_available_tags(campaign=campaign)
            print(f"Tags in '{campaign}': {campaign_tags}")
        
        print()
        
        # Test document loading for a global tag
        if global_tags:
            tag_name = global_tags[0]
            print(f"Loading documents for global tag '{tag_name}':")
            documents = loader.load_tag_documents(tag_name, campaign=None)
            
            for i, doc in enumerate(documents):
                print(f"  Document {i+1}:")
                print(f"    Content length: {len(doc.page_content)} characters")
                print(f"    Metadata: {doc.metadata}")
                print(f"    Content preview: {doc.page_content[:100]}...")
                print()
        
        # Test document loading for a campaign tag
        if campaigns and len(campaigns) > 0:
            campaign = campaigns[0]
            campaign_tags = loader.get_available_tags(campaign=campaign)
            if campaign_tags:
                tag_name = campaign_tags[0]
                print(f"Loading documents for campaign tag '{tag_name}' in '{campaign}':")
                documents = loader.load_tag_documents(tag_name, campaign=campaign)
                
                for i, doc in enumerate(documents):
                    print(f"  Document {i+1}:")
                    print(f"    Content length: {len(doc.page_content)} characters")
                    print(f"    Metadata: {doc.metadata}")
                    print(f"    Content preview: {doc.page_content[:100]}...")
                    print()
        
        return True
        
    except ImportError as e:
        print(f"Could not import loader: {e}")
        print("This might be because langchain isn't installed, but that's okay for this test.")
        return False
    except Exception as e:
        print(f"Error during testing: {e}")
        return False


def show_manual_file_inspection():
    """Manually inspect files without using the loader classes."""
    print("=== MANUAL FILE INSPECTION ===")
    print()
    
    source_dir = project_root / "data" / "source"
    
    if not source_dir.exists():
        print(f"Source directory doesn't exist: {source_dir}")
        print("You can create it by running the test_vectorstore_system.py script.")
        return
    
    print(f"Inspecting files in: {source_dir}")
    print()
    
    # Find all .txt files
    txt_files = list(source_dir.rglob("*.txt"))
    
    if not txt_files:
        print("No .txt files found in the source directory.")
        return
    
    for txt_file in txt_files:
        rel_path = txt_file.relative_to(source_dir)
        file_size = txt_file.stat().st_size
        
        print(f"File: {rel_path}")
        print(f"Size: {file_size} bytes")
        
        # Determine file type from path structure
        parts = rel_path.parts
        if parts[0] == 'campaigns' and len(parts) >= 4:
            print(f"Type: Campaign tag")
            print(f"Campaign: {parts[1]}")
            print(f"Tag name: {txt_file.stem}")
        elif parts[0] == 'global' and len(parts) >= 3:
            print(f"Type: Global tag")
            print(f"Tag name: {txt_file.stem}")
        else:
            print(f"Type: Other")
        
        # Show first few lines
        try:
            with open(txt_file, 'r') as f:
                lines = f.read().split('\n')
                print("First 3 lines:")
                for i, line in enumerate(lines[:3]):
                    print(f"  {i+1}: {line}")
                if len(lines) > 3:
                    print(f"  ... and {len(lines) - 3} more lines")
        except Exception as e:
            print(f"Error reading file: {e}")
        
        print("-" * 40)
        print()


def demonstrate_persona_workflow():
    """Show how this would work with a persona."""
    print("=== PERSONA WORKFLOW DEMONSTRATION ===")
    print()
    
    # Example persona data (this would come from your database)
    persona = {
        'name': 'Marta the Tavernkeeper',
        'backstory': 'Runs the Silver Swan Inn in Silverbrook City',
        'personality': 'Friendly but observant, knows everyone\'s business',
        'campaign': 'example_campaign',
        'tags': ['tavern', 'silverbrook_city', 'trade_dispute']
    }
    
    print("Example Persona from Database:")
    for key, value in persona.items():
        print(f"  {key}: {value}")
    print()
    
    print("When this persona needs to respond to a player, the system would:")
    print("1. Look up their assigned tags: ['tavern', 'silverbrook_city', 'trade_dispute']")
    print("2. For each tag, search the vector store for relevant content")
    print("3. Compress and combine the relevant information")
    print("4. Add this context to the LLM prompt")
    print()
    
    print("The resulting context might include:")
    print("- From 'tavern' tag: knowledge about running an inn, local gossip")
    print("- From 'silverbrook_city' tag: city layout, local politics, key NPCs")  
    print("- From 'trade_dispute' tag: current crisis details, key players, tensions")
    print()
    
    print("This gives Marta rich, relevant background knowledge without storing")
    print("massive amounts of text in the database persona record.")
    print()


def main():
    """Run all tests."""
    print("SIMPLE VECTORSTORE SYSTEM TEST")
    print("=" * 50)
    print()
    
    # Try the file loading system
    loader_worked = test_file_loading()
    
    if not loader_worked:
        print("Loader classes not available, falling back to manual inspection...")
        print()
        show_manual_file_inspection()
    
    demonstrate_persona_workflow()
    
    print("=== SUMMARY ===")
    print()
    print("This system provides:")
    print("✓ Organized file structure for game world content")
    print("✓ Automatic metadata extraction from file paths")
    print("✓ Campaign-specific and global content separation")
    print("✓ Integration points with your existing database models")
    print()
    
    if not loader_worked:
        print("To see the full system in action:")
        print("1. Install dependencies: pip install langchain langchain-chroma langchain-openai")
        print("2. Run the full demo: python test_vectorstore_system.py")
    else:
        print("File loading system is working! Next steps:")
        print("1. Add OpenAI API key to environment")
        print("2. Run: python test_vectorstore_system.py")
        print("3. Create vector store: python do_you_npc/__create_vectorstore.py")


if __name__ == "__main__":
    main()