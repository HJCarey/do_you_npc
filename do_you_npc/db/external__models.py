from datetime import datetime
from typing import List, Optional, Union

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from beholder_ai.game.skills.models import Skill, SkillProficiency


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


# Mapping table for Character-Campaign relationships
character_campaigns = Table(
    "character_campaigns",
    Base.metadata,
    Column("character_id", Integer, ForeignKey("characters.id"), primary_key=True),
    Column("campaign_id", Integer, ForeignKey("campaigns.id"), primary_key=True),
    Column("active", Boolean, default=True),
    Column("joined_at", DateTime, nullable=False, default=datetime.utcnow),
)


# Mapping table for NPC-Campaign relationships
npc_campaigns = Table(
    "npc_campaigns",
    Base.metadata,
    Column("npc_id", Integer, ForeignKey("npcs.id"), primary_key=True),
    Column("campaign_id", Integer, ForeignKey("campaigns.id"), primary_key=True),
    Column("active", Boolean, default=True),
    Column("joined_at", DateTime, nullable=False, default=datetime.utcnow),
)


# Mapping table for Creature-Campaign relationships
creature_campaigns = Table(
    "creature_campaigns",
    Base.metadata,
    Column("creature_id", Integer, ForeignKey("creatures.id"), primary_key=True),
    Column("campaign_id", Integer, ForeignKey("campaigns.id"), primary_key=True),
    Column("active", Boolean, default=True),
    Column("joined_at", DateTime, nullable=False, default=datetime.utcnow),
)


# New mapping tables for adventure modules
character_modules = Table(
    "character_modules",
    Base.metadata,
    Column("character_id", Integer, ForeignKey("characters.id"), primary_key=True),
    Column("module_id", Integer, ForeignKey("adventure_modules.id"), primary_key=True),
    Column("active", Boolean, default=True),
    Column("joined_at", DateTime, nullable=False, default=datetime.utcnow),
)

npc_modules = Table(
    "npc_modules",
    Base.metadata,
    Column("npc_id", Integer, ForeignKey("npcs.id"), primary_key=True),
    Column("module_id", Integer, ForeignKey("adventure_modules.id"), primary_key=True),
    Column("active", Boolean, default=True),
    Column("joined_at", DateTime, nullable=False, default=datetime.utcnow),
)

creature_modules = Table(
    "creature_modules",
    Base.metadata,
    Column("creature_id", Integer, ForeignKey("creatures.id"), primary_key=True),
    Column("module_id", Integer, ForeignKey("adventure_modules.id"), primary_key=True),
    Column("active", Boolean, default=True),
    Column("joined_at", DateTime, nullable=False, default=datetime.utcnow),
)


# Create location_modules association table
location_modules = Table(
    "location_modules",
    Base.metadata,
    Column("location_id", Integer, ForeignKey("locations.id"), primary_key=True),
    Column("module_id", Integer, ForeignKey("adventure_modules.id"), primary_key=True),
    Column("active", Boolean, default=True),
    Column("joined_at", DateTime, nullable=False, default=datetime.utcnow),
)


# Encounter association tables
encounter_npcs = Table(
    "encounter_npcs",
    Base.metadata,
    Column(
        "encounter_id", Integer, ForeignKey("adventure_encounters.id"), primary_key=True
    ),
    Column("npc_id", Integer, ForeignKey("npcs.id"), primary_key=True),
    Column("role", String(50)),
    Column("active", Boolean, nullable=False, default=True),
    Column("joined_at", DateTime, nullable=False, default=datetime.utcnow),
)

encounter_creatures = Table(
    "encounter_creatures",
    Base.metadata,
    Column(
        "encounter_id", Integer, ForeignKey("adventure_encounters.id"), primary_key=True
    ),
    Column("creature_id", Integer, ForeignKey("creatures.id"), primary_key=True),
    Column("quantity", Integer, nullable=False, default=1),
    Column("role", String(50)),
    Column("active", Boolean, nullable=False, default=True),
    Column("joined_at", DateTime, nullable=False, default=datetime.utcnow),
)

# Session association tables
session_characters = Table(
    "session_characters",
    Base.metadata,
    Column("session_id", Integer, ForeignKey("game_sessions.id"), primary_key=True),
    Column("character_id", Integer, ForeignKey("characters.id"), primary_key=True),
    Column("is_active", Boolean, default=True),
    Column("current_hp", Integer, nullable=True),
    Column("temp_hp", Integer, nullable=True),
    Column("conditions", String(200), nullable=True),  # JSON list of active conditions
    Column("joined_at", DateTime, nullable=False, default=datetime.utcnow),
)

session_encounters = Table(
    "session_encounters",
    Base.metadata,
    Column("session_id", Integer, ForeignKey("game_sessions.id"), primary_key=True),
    Column(
        "encounter_id", Integer, ForeignKey("adventure_encounters.id"), primary_key=True
    ),
    Column(
        "status", String(20), nullable=False, default="pending"
    ),  # pending, active, completed
    Column("initiative_order", Text, nullable=True),  # JSON list of initiative order
    Column("round_count", Integer, default=0),
    Column("started_at", DateTime, nullable=True),
    Column("completed_at", DateTime, nullable=True),
)


class Campaign(Base):
    """Campaign model representing a D&D campaign."""

    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="planning",  # planning, active, completed, archived
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    characters: Mapped[List["Character"]] = relationship(
        secondary=character_campaigns, back_populates="campaigns"
    )
    npcs: Mapped[List["NPC"]] = relationship(
        secondary=npc_campaigns, back_populates="campaigns"
    )
    creatures: Mapped[List["Creature"]] = relationship(
        secondary=creature_campaigns, back_populates="campaigns"
    )
    world: Mapped["CampaignWorld"] = relationship(
        back_populates="campaign", uselist=False
    )
    adventure_modules: Mapped[List["AdventureModule"]] = relationship(
        back_populates="campaign"
    )
    game_sessions: Mapped[List["GameSession"]] = relationship(back_populates="campaign")


class CampaignWorld(Base):
    """Model for storing campaign world information."""

    __tablename__ = "campaign_worlds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaigns.id"), unique=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    campaign: Mapped["Campaign"] = relationship(back_populates="world")
    regions: Mapped[List["Region"]] = relationship(back_populates="world")
    factions: Mapped[List["Faction"]] = relationship(back_populates="world")
    world_events: Mapped[List["WorldEvent"]] = relationship(back_populates="world")
    lore_entries: Mapped[List["LoreEntry"]] = relationship(back_populates="world")


class Region(Base):
    """Model for geographical/political regions in a campaign world."""

    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    world_id: Mapped[int] = mapped_column(ForeignKey("campaign_worlds.id"))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    region_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # kingdom, wilderness, city-state, etc.
    climate: Mapped[Optional[str]] = mapped_column(String(50))
    population: Mapped[Optional[int]] = mapped_column(Integer)
    government: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    world: Mapped["CampaignWorld"] = relationship(back_populates="regions")
    locations: Mapped[List["Location"]] = relationship(back_populates="region")


class Faction(Base):
    """Model for organizations and groups in the campaign world."""

    __tablename__ = "factions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    world_id: Mapped[int] = mapped_column(ForeignKey("campaign_worlds.id"))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    faction_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # guild, religion, government, etc.
    influence: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # local, regional, global
    alignment: Mapped[Optional[str]] = mapped_column(String(50))
    goals: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    world: Mapped["CampaignWorld"] = relationship(back_populates="factions")


class WorldEvent(Base):
    """Model for major events in the campaign world."""

    __tablename__ = "world_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    world_id: Mapped[int] = mapped_column(ForeignKey("campaign_worlds.id"))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    event_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # historical, ongoing, prophecy
    significance: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # local, regional, global
    timeline_position: Mapped[Optional[str]] = mapped_column(
        String(100)
    )  # When it occurred/occurs
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    world: Mapped["CampaignWorld"] = relationship(back_populates="world_events")


class LoreEntry(Base):
    """Model for cultural and historical information about the campaign world."""

    __tablename__ = "lore_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    world_id: Mapped[int] = mapped_column(ForeignKey("campaign_worlds.id"))
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # culture, history, magic, religion, etc.
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    world: Mapped["CampaignWorld"] = relationship(back_populates="lore_entries")


class Location(Base):
    """Model for specific locations in the campaign world."""

    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    region_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("regions.id"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    location_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # dungeon, town, landmark, etc.
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    region: Mapped[Optional["Region"]] = relationship(back_populates="locations")
    adventure_modules: Mapped[List["AdventureModule"]] = relationship(
        secondary=location_modules, back_populates="locations"
    )


class AdventureModule(Base):
    """Model for adventure modules within a campaign."""

    __tablename__ = "adventure_modules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaigns.id"))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="planning",  # planning, active, completed
    )
    level_range: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # e.g., "1-4", "5-10"
    difficulty_rating: Mapped[str] = mapped_column(String(20), nullable=False)
    recommended_party_size: Mapped[int] = mapped_column(Integer, nullable=False)
    recommended_classes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    hook: Mapped[str] = mapped_column(Text, nullable=False)
    antagonist_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    story_arc: Mapped[str] = mapped_column(Text, nullable=False)
    climax: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    campaign: Mapped["Campaign"] = relationship(back_populates="adventure_modules")
    characters: Mapped[List["Character"]] = relationship(secondary=character_modules)
    npcs: Mapped[List["NPC"]] = relationship(secondary=npc_modules)
    creatures: Mapped[List["Creature"]] = relationship(secondary=creature_modules)
    locations: Mapped[List["Location"]] = relationship(
        secondary=location_modules, back_populates="adventure_modules"
    )
    storylines: Mapped[List["StorylineElement"]] = relationship(
        back_populates="adventure_module"
    )
    objectives: Mapped[List["Objective"]] = relationship(
        back_populates="adventure_module"
    )
    game_sessions: Mapped[List["GameSession"]] = relationship(
        back_populates="adventure"
    )
    encounters: Mapped[List["Encounter"]] = relationship(
        back_populates="adventure_module"
    )


class StorylineElement(Base):
    """Model for storyline elements within an adventure module."""

    __tablename__ = "storyline_elements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("adventure_modules.id"))
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    element_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # plot_hook, event, revelation, etc.
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending"
    )  # pending, active, completed, failed
    sequence: Mapped[Optional[int]] = mapped_column(
        Integer
    )  # Optional ordering of elements
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    adventure_module: Mapped["AdventureModule"] = relationship(
        back_populates="storylines"
    )


class Objective(Base):
    """Model for objectives/quests within an adventure module."""

    __tablename__ = "objectives"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("adventure_modules.id"))
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    objective_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # main_quest, side_quest, secret
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending"
    )  # pending, active, completed, failed
    prerequisites: Mapped[Optional[str]] = mapped_column(
        Text
    )  # JSON string of prerequisite objective IDs
    rewards: Mapped[Optional[str]] = mapped_column(Text)  # Description of rewards
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    adventure_module: Mapped["AdventureModule"] = relationship(
        back_populates="objectives"
    )


class Stats(Base):
    """Stats model for tracking player and NPC ability scores and other stats."""

    __tablename__ = "stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    character_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("characters.id"), nullable=True
    )
    npc_id: Mapped[Optional[int]] = mapped_column(ForeignKey("npcs.id"), nullable=True)
    creature_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("creatures.id"), nullable=True
    )
    is_current: Mapped[bool] = mapped_column(Boolean, default=True)

    # Ability Scores
    strength: Mapped[int] = mapped_column(Integer, nullable=False)
    dexterity: Mapped[int] = mapped_column(Integer, nullable=False)
    constitution: Mapped[int] = mapped_column(Integer, nullable=False)
    intelligence: Mapped[int] = mapped_column(Integer, nullable=False)
    wisdom: Mapped[int] = mapped_column(Integer, nullable=False)
    charisma: Mapped[int] = mapped_column(Integer, nullable=False)

    # Derived Stats
    max_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    current_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    temporary_hp: Mapped[int] = mapped_column(Integer, default=0)
    armor_class: Mapped[int] = mapped_column(Integer, nullable=False)
    speed: Mapped[int] = mapped_column(Integer, nullable=False)
    initiative: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    proficiency_bonus: Mapped[int] = mapped_column(Integer, nullable=False)

    # Saving Throws (proficiency flags)
    strength_save_prof: Mapped[bool] = mapped_column(Boolean, default=False)
    dexterity_save_prof: Mapped[bool] = mapped_column(Boolean, default=False)
    constitution_save_prof: Mapped[bool] = mapped_column(Boolean, default=False)
    intelligence_save_prof: Mapped[bool] = mapped_column(Boolean, default=False)
    wisdom_save_prof: Mapped[bool] = mapped_column(Boolean, default=False)
    charisma_save_prof: Mapped[bool] = mapped_column(Boolean, default=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    character = relationship("Character", back_populates="stats")
    npc = relationship("NPC", back_populates="stats")
    creature = relationship("Creature", back_populates="stats")


class CharacterSkills(Base):
    """Character skill proficiencies."""

    __tablename__ = "character_skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    character_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("characters.id", ondelete="CASCADE")
    )
    skill: Mapped[str] = mapped_column(String(50), nullable=False)
    is_proficient: Mapped[bool] = mapped_column(Boolean, default=False)
    has_expertise: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    character: Mapped["Character"] = relationship("Character", back_populates="skills")


class Character(Base):
    """Character model representing a player character.

    Characters can be controlled either by human players or by AI.
    The is_ai_controlled flag determines how character actions and
    responses are handled, but all other character functionality
    remains identical regardless of control type.
    """

    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    race: Mapped[str] = mapped_column(String(50), nullable=False)
    character_class: Mapped[str] = mapped_column(String(50), nullable=False)
    character_subclass: Mapped[str] = mapped_column(String(50), nullable=True)
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    background: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_template: Mapped[bool] = mapped_column(Boolean, default=False)
    is_ai_controlled: Mapped[bool] = mapped_column(Boolean, default=False)
    personality_prompt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # New fields
    character_hooks: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True
    )  # Stored as JSON list
    roleplay_traits: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True
    )  # Personality, ideals, bonds, flaws
    notes: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True
    )  # General character notes
    last_edited: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    campaigns: Mapped[List["Campaign"]] = relationship(
        secondary=character_campaigns, back_populates="characters"
    )
    stats: Mapped[List["Stats"]] = relationship(
        back_populates="character", order_by="desc(Stats.created_at)"
    )
    game_sessions: Mapped[List["GameSession"]] = relationship(
        secondary="session_characters", back_populates="active_characters"
    )

    # Add skills relationship
    skills: Mapped[List["CharacterSkills"]] = relationship(
        "CharacterSkills", back_populates="character", cascade="all, delete-orphan"
    )

    @property
    def current_stats(self) -> Optional["Stats"]:
        """Get the current stats for the character."""
        return next((stats for stats in self.stats if stats.is_current), None)

    def get_skill_proficiencies(self) -> List[SkillProficiency]:
        """Get all skill proficiencies for the character.

        Returns:
            List[SkillProficiency]: List of all skill proficiencies
        """
        proficiencies = []
        for skill_record in self.skills:
            try:
                skill = Skill[skill_record.skill]
                proficiencies.append(
                    SkillProficiency(
                        skill=skill,
                        is_proficient=skill_record.is_proficient,
                        has_expertise=skill_record.has_expertise,
                    )
                )
            except KeyError:
                continue  # Skip invalid skills
        return proficiencies

    def is_proficient_in(self, skill: Union[Skill, str]) -> bool:
        """Check if the character is proficient in a skill.

        Args:
            skill: The skill to check (can be Skill enum or string name)

        Returns:
            bool: Whether the character is proficient in the skill
        """
        if isinstance(skill, str):
            try:
                skill = Skill[skill.upper()]
            except KeyError:
                return False

        skill_record = next((s for s in self.skills if s.skill == skill.name), None)
        return skill_record.is_proficient if skill_record else False

    def has_expertise_in(self, skill: Union[Skill, str]) -> bool:
        """Check if the character has expertise in a skill.

        Args:
            skill: The skill to check (can be Skill enum or string name)

        Returns:
            bool: Whether the character has expertise in the skill
        """
        if isinstance(skill, str):
            try:
                skill = Skill[skill.upper()]
            except KeyError:
                return False

        skill_record = next((s for s in self.skills if s.skill == skill.name), None)
        return skill_record.has_expertise if skill_record else False

    def set_skill_proficiency(
        self, skill: Union[Skill, str], is_proficient: bool, has_expertise: bool = False
    ) -> None:
        """Set a character's proficiency in a skill.

        Args:
            skill: The skill to set (can be Skill enum or string name)
            is_proficient: Whether the character is proficient
            has_expertise: Whether the character has expertise
        """
        if isinstance(skill, str):
            try:
                skill = Skill[skill.upper()]
            except KeyError:
                raise ValueError(f"Invalid skill name: {skill}")

        skill_record = next((s for s in self.skills if s.skill == skill.name), None)

        if skill_record:
            skill_record.is_proficient = is_proficient
            skill_record.has_expertise = has_expertise
            skill_record.updated_at = datetime.utcnow()
        else:
            # Create new skill record if it doesn't exist
            self.skills.append(
                CharacterSkills(
                    skill=skill.name,
                    is_proficient=is_proficient,
                    has_expertise=has_expertise,
                )
            )


class NPC(Base):
    """NPC model representing non-player characters."""

    __tablename__ = "npcs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    role: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    race: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    character_class: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_template: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    campaigns: Mapped[List["Campaign"]] = relationship(
        secondary=npc_campaigns, back_populates="npcs"
    )
    stats: Mapped[List["Stats"]] = relationship(
        back_populates="npc", order_by="desc(Stats.created_at)"
    )
    encounters: Mapped[List["Encounter"]] = relationship(
        secondary="encounter_npcs", back_populates="npcs"
    )

    @property
    def current_stats(self) -> Optional["Stats"]:
        """Get the current stats for the NPC."""
        return next((stats for stats in self.stats if stats.is_current), None)


class Creature(Base):
    """Creature model.

    This class is to represent enemies/monsters/etc that don't require full
    character build-out.
    """

    __tablename__ = "creatures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    role: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    is_template: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    campaigns: Mapped[List["Campaign"]] = relationship(
        secondary=creature_campaigns, back_populates="creatures"
    )
    stats: Mapped[List["Stats"]] = relationship(
        back_populates="creature", order_by="desc(Stats.created_at)"
    )
    encounters: Mapped[List["Encounter"]] = relationship(
        secondary="encounter_creatures", back_populates="creatures"
    )

    @property
    def current_stats(self) -> Optional["Stats"]:
        """Get the current stats for the creature."""
        return next((stats for stats in self.stats if stats.is_current), None)


class GameSession(Base):
    """Model for managing active game sessions."""

    __tablename__ = "game_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaigns.id"))
    adventure_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("adventure_modules.id"), nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="planning",  # planning, active, paused, completed
    )
    current_scene: Mapped[str] = mapped_column(Text, nullable=True)
    session_log: Mapped[str] = mapped_column(
        Text, nullable=True
    )  # JSON list of interactions
    session_state: Mapped[str] = mapped_column(Text, nullable=True)  # JSON game state
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    campaign: Mapped["Campaign"] = relationship(back_populates="game_sessions")
    adventure: Mapped[Optional["AdventureModule"]] = relationship(
        back_populates="game_sessions"
    )
    active_characters: Mapped[List["Character"]] = relationship(
        secondary="session_characters",
        back_populates="game_sessions",
        primaryjoin="and_(GameSession.id == session_characters.c.session_id, "
        "session_characters.c.is_active == True)",
        secondaryjoin="Character.id == session_characters.c.character_id",
    )
    active_encounters: Mapped[List["Encounter"]] = relationship(
        secondary="session_encounters", back_populates="game_sessions"
    )


class Encounter(Base):
    """Model for managing game encounters."""

    __tablename__ = "adventure_encounters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    adventure_id: Mapped[int] = mapped_column(ForeignKey("adventure_modules.id"))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    encounter_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # combat, social, puzzle, etc.
    difficulty: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # easy, medium, hard
    location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    setup: Mapped[str] = mapped_column(Text, nullable=False)
    objectives: Mapped[str] = mapped_column(Text, nullable=False)
    rewards: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sequence_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    adventure_module: Mapped["AdventureModule"] = relationship(
        back_populates="encounters"
    )
    game_sessions: Mapped[List["GameSession"]] = relationship(
        secondary="session_encounters", back_populates="active_encounters"
    )
    creatures: Mapped[List["Creature"]] = relationship(
        secondary="encounter_creatures", back_populates="encounters"
    )
    npcs: Mapped[List["NPC"]] = relationship(
        secondary="encounter_npcs", back_populates="encounters"
    )
