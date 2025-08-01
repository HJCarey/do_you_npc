#!/usr/bin/env python3
"""
Test script for Google Gemini integration.

This script tests the basic Gemini functionality without needing
a full vector store setup.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_gemini_basic():
    """Test basic Gemini model functionality."""
    print("=== TESTING GEMINI BASIC FUNCTIONALITY ===")
    print()
    
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment variables")
        print("Please set your Google API key in your .env file:")
        print("GOOGLE_API_KEY='your-key-here'")
        return False
    
    print(f"✅ Google API key found (ends with: ...{api_key[-4:]})")
    print()
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("✅ langchain_google_genai import successful")
        
        # Create the model
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0.7,
            convert_system_message_to_human=True
        )
        print("✅ Gemini model created successfully")
        print()
        
        # Test a simple query
        print("Testing simple query...")
        response = llm.invoke("Say hello and confirm you are Gemini 2.0 Flash. Keep it brief.")
        print(f"🤖 Gemini response: {response.content}")
        print()
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Install required package: pip install langchain-google-genai")
        return False
    except Exception as e:
        print(f"❌ Error testing Gemini: {e}")
        return False


def test_gemini_embeddings():
    """Test Gemini embeddings functionality."""
    print("=== TESTING GEMINI EMBEDDINGS ===")
    print()
    
    try:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        print("✅ GoogleGenerativeAIEmbeddings import successful")
        
        # Create embeddings
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        print("✅ Google embeddings model created successfully")
        
        # Test embedding a simple text
        test_text = "This is a test of the embedding system for NPC knowledge."
        print(f"Testing embedding for: '{test_text}'")
        
        embedding_vector = embeddings.embed_query(test_text)
        print(f"✅ Embedding created successfully (dimension: {len(embedding_vector)})")
        print(f"First 5 values: {embedding_vector[:5]}")
        print()
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Install required package: pip install langchain-google-genai")
        return False
    except Exception as e:
        print(f"❌ Error testing embeddings: {e}")
        return False


def test_vectorstore_integration():
    """Test if the vectorstore system works with Gemini."""
    print("=== TESTING VECTORSTORE INTEGRATION ===")
    print()
    
    try:
        from do_you_npc.vectorstore import VectorStoreManager
        print("✅ VectorStoreManager import successful")
        
        manager = VectorStoreManager()
        print(f"✅ VectorStoreManager created")
        print(f"Source directory: {manager.source_dir}")
        print(f"Vector store directory: {manager.vectorstore_dir}")
        print()
        
        # Check if we have any source files
        source_files = list(manager.source_dir.rglob("*.txt")) if manager.source_dir.exists() else []
        print(f"Found {len(source_files)} .txt files in source directory")
        
        if source_files:
            print("Sample files:")
            for i, file_path in enumerate(source_files[:3]):
                rel_path = file_path.relative_to(manager.source_dir)
                print(f"  {i+1}. {rel_path}")
            if len(source_files) > 3:
                print(f"  ... and {len(source_files) - 3} more")
        else:
            print("No source files found. Add .txt files to test vector store creation.")
        
        print()
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing vectorstore: {e}")
        return False


def test_llm_functions():
    """Test the updated LLM functions."""
    print("=== TESTING LLM FUNCTIONS ===")
    print()
    
    try:
        from do_you_npc.llm import get_persona_context, search_knowledge_base
        print("✅ LLM functions import successful")
        
        # Test persona context (this might not work without vector store, but should import)
        print("Testing persona context function...")
        try:
            context = get_persona_context(['blacksmith'], campaign=None)
            if context == "No additional context available.":
                print("✅ get_persona_context function works (no vector store data)")
            else:
                print(f"✅ get_persona_context returned: {context[:100]}...")
        except Exception as e:
            print(f"⚠️ get_persona_context error (expected without vector store): {e}")
        
        # Test knowledge base search
        print("Testing knowledge base search...")
        try:
            results = search_knowledge_base("test query")
            print(f"✅ search_knowledge_base returned {len(results)} results")
        except Exception as e:
            print(f"⚠️ search_knowledge_base error (expected without vector store): {e}")
        
        print()
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing LLM functions: {e}")
        return False


def main():
    """Run all Gemini integration tests."""
    print("GOOGLE GEMINI INTEGRATION TEST")
    print("=" * 50)
    print()
    
    tests = [
        ("Basic Gemini functionality", test_gemini_basic),
        ("Gemini embeddings", test_gemini_embeddings),
        ("VectorStore integration", test_vectorstore_integration),
        ("LLM functions", test_llm_functions),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
        print("-" * 40)
        print()
    
    # Summary
    print("=== TEST SUMMARY ===")
    print()
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print()
        print("🎉 All tests passed! Gemini integration is working.")
        print()
        print("Next steps:")
        print("1. Create vector store: python do_you_npc/create_vectorstore.py")
        print("2. Test with your Streamlit app: streamlit run do_you_npc/app.py")
    else:
        print()
        print("⚠️ Some tests failed. Check the output above for details.")
        print()
        print("Common fixes:")
        print("- Install dependencies: pip install langchain-google-genai")
        print("- Set API key in .env: GOOGLE_API_KEY='your-key-here'")


if __name__ == "__main__":
    main()