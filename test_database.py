#!/usr/bin/env python3
"""
Simple test script to verify database setup is working.
Run this from the project root directory: python test_database.py
"""

import sys
import os

# Add the project to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from do_you_npc.db.database import db_config, get_db_session
    from do_you_npc.db.crud import PersonaCRUD, PromptCRUD, TagCRUD
    print("✓ Successfully imported database modules")
except ImportError as e:
    print(f"✗ Failed to import database modules: {e}")
    print("Make sure you're in the conda environment: conda activate do_you_npc")
    sys.exit(1)

def test_database():
    """Test basic database operations."""
    
    try:
        # Test database connection
        print("\n--- Testing Database Connection ---")
        with next(get_db_session()) as session:
            print("✓ Database connection successful")
        
        # Ensure tables exist
        print("\n--- Creating Tables ---")
        db_config.create_tables()
        print("✓ Tables created/verified")
        
        # Test basic operations
        print("\n--- Testing CRUD Operations ---")
        with next(get_db_session()) as session:
            # Test tag creation
            tag = TagCRUD.get_by_name(session, "test_tag")
            if not tag:
                tag = TagCRUD.create(session, "test_tag", "A test tag for verification")
            print(f"✓ Tag operations working (ID: {tag.id})")
            
            # Test prompt creation
            prompt = PromptCRUD.get_by_name(session, "test_prompt")
            if not prompt:
                prompt = PromptCRUD.create(session, "test_prompt", "A test prompt for verification")
            print(f"✓ Prompt operations working (ID: {prompt.id})")
            
            # Test persona creation
            persona = PersonaCRUD.get_by_name(session, "Test Character")
            if not persona:
                persona = PersonaCRUD.create(
                    session,
                    name="Test Character",
                    backstory="A character created for testing purposes",
                    personality="Helpful and reliable",
                    tags=[tag]
                )
            print(f"✓ Persona operations working (ID: {persona.id})")
            
            # Test relationships
            print(f"✓ Persona has {len(persona.tags)} tag(s): {[t.name for t in persona.tags]}")
            print(f"✓ Tag is used by {len(tag.personas)} persona(s): {[p.name for p in tag.personas]}")
        
        print("\n🎉 All database tests passed!")
        print("Your database setup is working correctly.")
        
    except Exception as e:
        print(f"\n✗ Database test failed: {e}")
        print("\nPossible issues:")
        print("1. PostgreSQL is not running")
        print("2. Database 'do_you_npc' doesn't exist")
        print("3. User permissions are incorrect")
        print("4. .env file is missing or incorrect")
        return False
    
    return True

if __name__ == "__main__":
    print("=== Do You NPC Database Test ===")
    success = test_database()
    sys.exit(0 if success else 1)