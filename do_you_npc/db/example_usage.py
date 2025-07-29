"""Example usage of the database models and CRUD operations."""

from do_you_npc.db.database import db_config, get_db_session
from do_you_npc.db.crud import PersonaCRUD, PromptCRUD, TagCRUD


def example_usage():
    """Demonstrate basic database operations."""
    
    # Create tables
    print("Creating database tables...")
    db_config.create_tables()
    
    # Get a database session
    with next(get_db_session()) as session:
        # Create some tags (or get existing ones)
        print("\nCreating/getting tags...")
        warrior_tag = TagCRUD.get_by_name(session, "warrior")
        if not warrior_tag:
            warrior_tag = TagCRUD.create(session, "warrior", "A skilled combatant specialized in melee weapons")
        
        magic_tag = TagCRUD.get_by_name(session, "magic")
        if not magic_tag:
            magic_tag = TagCRUD.create(session, "magic", "Possesses magical abilities and knowledge")
        
        noble_tag = TagCRUD.get_by_name(session, "noble")
        if not noble_tag:
            noble_tag = TagCRUD.create(session, "noble", "Of aristocratic birth with political connections")
        
        # Create some prompts (or get existing ones)
        print("Creating/getting prompts...")
        dialogue_prompt = PromptCRUD.get_by_name(session, "dialogue_generation")
        if not dialogue_prompt:
            dialogue_prompt = PromptCRUD.create(
                session, 
                "dialogue_generation", 
                "Generate natural dialogue for this character based on their personality and backstory."
            )
        
        action_prompt = PromptCRUD.get_by_name(session, "action_generation")
        if not action_prompt:
            action_prompt = PromptCRUD.create(
                session,
                "action_generation",
                "Determine what actions this character would take in the given scenario."
            )
        
        # Create a persona with tags (or get existing one)
        print("Creating/getting persona...")
        persona = PersonaCRUD.get_by_name(session, "Sir Aldric the Bold")
        if not persona:
            persona = PersonaCRUD.create(
                session,
                name="Sir Aldric the Bold",
                backstory="A noble knight who lost his lands in a war and now serves as a mercenary",
                personality="Honorable but pragmatic, struggles with maintaining his ideals while earning coin",
                tags=[warrior_tag, noble_tag]
            )
        
        # Demonstrate reading operations
        print(f"\nRetrieved persona: {persona.name}")
        print(f"Backstory: {persona.backstory}")
        print(f"Personality: {persona.personality}")
        print(f"Tags: {[tag.name for tag in persona.tags]}")
        
        # Show all entities
        print(f"\nAll personas: {[p.name for p in PersonaCRUD.get_all(session)]}")
        print(f"All prompts: {[p.name for p in PromptCRUD.get_all(session)]}")
        print(f"All tags: {[t.name for t in TagCRUD.get_all(session)]}")
        
        # Update example
        print("\nUpdating persona...")
        updated_persona = PersonaCRUD.update(
            session, 
            persona.id, 
            personality="Honorable but pragmatic, increasingly bitter about his fall from grace"
        )
        print(f"Updated personality: {updated_persona.personality}")


if __name__ == "__main__":
    example_usage()