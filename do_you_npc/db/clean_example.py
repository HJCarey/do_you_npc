"""Clean example usage that starts fresh each time."""

from do_you_npc.db.database import db_config, get_db_session
from do_you_npc.db.crud import PersonaCRUD, PromptCRUD, TagCRUD


def clean_example():
    """Demonstrate database operations starting with a clean slate."""
    
    print("Dropping and recreating database tables...")
    # Drop all tables and recreate them
    db_config.drop_tables()
    db_config.create_tables()
    
    # Get a database session
    with next(get_db_session()) as session:
        # Create some tags
        print("\nCreating tags...")
        warrior_tag = TagCRUD.create(session, "warrior", "A skilled combatant specialized in melee weapons")
        magic_tag = TagCRUD.create(session, "magic", "Possesses magical abilities and knowledge")
        noble_tag = TagCRUD.create(session, "noble", "Of aristocratic birth with political connections")
        
        # Create some prompts
        print("Creating prompts...")
        dialogue_prompt = PromptCRUD.create(
            session, 
            "dialogue_generation", 
            "Generate natural dialogue for this character based on their personality and backstory."
        )
        action_prompt = PromptCRUD.create(
            session,
            "action_generation",
            "Determine what actions this character would take in the given scenario."
        )
        
        # Create a persona with tags
        print("Creating persona...")
        persona = PersonaCRUD.create(
            session,
            name="Sir Aldric the Bold",
            backstory="A noble knight who lost his lands in a war and now serves as a mercenary",
            personality="Honorable but pragmatic, struggles with maintaining his ideals while earning coin",
            tags=[warrior_tag, noble_tag]
        )
        
        # Create another persona to show multiple records
        print("Creating another persona...")
        mage_persona = PersonaCRUD.create(
            session,
            name="Lyra Moonwhisper",
            backstory="A young elf who discovered her magical powers accidentally burned down her village",
            personality="Curious and eager to learn, but haunted by guilt over her past mistakes",
            tags=[magic_tag]
        )
        
        # Demonstrate reading operations
        print(f"\n=== PERSONAS ===")
        for p in PersonaCRUD.get_all(session):
            print(f"Name: {p.name}")
            print(f"Backstory: {p.backstory}")
            print(f"Personality: {p.personality}")
            print(f"Tags: {[tag.name for tag in p.tags]}")
            print("-" * 50)
        
        print(f"\n=== PROMPTS ===")
        for prompt in PromptCRUD.get_all(session):
            print(f"Name: {prompt.name}")
            print(f"Content: {prompt.text_body}")
            print("-" * 50)
        
        print(f"\n=== TAGS ===")
        for tag in TagCRUD.get_all(session):
            print(f"Name: {tag.name}")
            print(f"Description: {tag.text_body}")
            print(f"Used by personas: {[p.name for p in tag.personas]}")
            print("-" * 50)
        
        # Demonstrate update operation
        print("\n=== UPDATE EXAMPLE ===")
        updated_persona = PersonaCRUD.update(
            session, 
            persona.id, 
            personality="Honorable but pragmatic, increasingly bitter about his fall from grace"
        )
        print(f"Updated {updated_persona.name}'s personality:")
        print(f"New personality: {updated_persona.personality}")
        
        # Demonstrate deletion
        print(f"\n=== DELETE EXAMPLE ===")
        print(f"Deleting {mage_persona.name}...")
        success = PersonaCRUD.delete(session, mage_persona.id)
        print(f"Deletion successful: {success}")
        
        remaining_personas = PersonaCRUD.get_all(session)
        print(f"Remaining personas: {[p.name for p in remaining_personas]}")


if __name__ == "__main__":
    clean_example()