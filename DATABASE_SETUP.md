# Database Setup Guide

This guide explains how to use the PostgreSQL database setup for the Do You NPC project.

## Quick Test

To verify everything is working, run:

```bash
conda activate do_you_npc
python test_database.py
```

## Database Models

The project includes three main models:

### 1. **Persona** - Game characters/NPCs
- `name` (required): Character name
- `backstory` (required): Character background story  
- `personality` (required): Character personality description
- `tags`: List of associated Tag objects

### 2. **Prompt** - AI prompts and templates
- `name` (required): Prompt identifier
- `text_body` (required): The actual prompt text

### 3. **Tag** - Labels and categories
- `name` (required, unique): Tag name
- `text_body` (required): Tag description
- `personas`: List of personas using this tag

## Example Usage

### Running Examples

```bash
# Basic example (handles existing data)
conda activate do_you_npc
python -m do_you_npc.db.example_usage

# Clean example (starts fresh each time)
conda activate do_you_npc  
python -m do_you_npc.db.clean_example
```

### Creating Records

```python
from do_you_npc.db.database import get_db_session
from do_you_npc.db.crud import PersonaCRUD, TagCRUD

with next(get_db_session()) as session:
    # Create a tag
    warrior_tag = TagCRUD.create(session, "warrior", "Skilled fighter")
    
    # Create a persona with tags
    persona = PersonaCRUD.create(
        session,
        name="Sir Arthur",
        backstory="A noble knight on a quest",
        personality="Brave and honorable",
        tags=[warrior_tag]
    )
```

### Reading Records

```python
with next(get_db_session()) as session:
    # Get by ID
    persona = PersonaCRUD.get_by_id(session, 1)
    
    # Get by name
    persona = PersonaCRUD.get_by_name(session, "Sir Arthur")
    
    # Get all
    all_personas = PersonaCRUD.get_all(session)
```

### Updating Records

```python
with next(get_db_session()) as session:
    # Update fields
    updated = PersonaCRUD.update(
        session, 
        persona_id=1, 
        personality="Brave but world-weary"
    )
```

### Deleting Records

```python
with next(get_db_session()) as session:
    # Delete by ID
    success = PersonaCRUD.delete(session, persona_id=1)
```

## Database Configuration

The database connection is configured via environment variables in `.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=do_you_npc
DB_USER=jake
DB_PASSWORD=
```

The setup uses PostgreSQL with peer authentication for local development (no password required).

## Troubleshooting

If you encounter issues:

1. **Import errors**: Make sure you're in the conda environment: `conda activate do_you_npc`
2. **Connection errors**: Verify PostgreSQL is running: `systemctl status postgresql`
3. **Permission errors**: Check that your user can access the database: `psql -U jake -d do_you_npc -c "SELECT 1;"`

## Database Schema

The database includes these tables:
- `personas` - Character/NPC data
- `prompts` - AI prompt templates
- `tags` - Categorization labels
- `persona_tags` - Many-to-many relationship table