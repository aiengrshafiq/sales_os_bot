# db/models.py
import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    JSON,
    ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship

# Base class for our models to inherit from
Base = declarative_base()

class Implementation(Base):
    """Represents a single Sales-OS implementation for a user/subsidiary."""
    __tablename__ = "implementations"

    id = Column(Integer, primary_key=True, index=True)
    owner_user_id = Column(String, unique=True, index=True, nullable=False) # e.g., Shafiq's Slack ID
    subsidiary_id = Column(String, nullable=False, default="metamorphic") # Pilot subsidiary
    stage = Column(String, nullable=False, default="S0") # S0=Not Started, S1, S2 etc.
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Establish a relationship to the SCP Profile
    scp_profile = relationship("SCPProfile", back_populates="implementation", uselist=False)

class SCPProfile(Base):
    """Stores the Subsidiary Context Profile (SCP) details."""
    __tablename__ = "scp_profiles"

    id = Column(Integer, primary_key=True, index=True)
    implementation_id = Column(Integer, ForeignKey("implementations.id"), nullable=False)
    profile_data = Column(JSON, nullable=False) # Stores the full SCP JSON object
    
    # Establish a back-reference from Implementation
    implementation = relationship("Implementation", back_populates="scp_profile")

class Atom(Base):
    """Stores a single Canonical Pattern Library (CPL) atom."""
    __tablename__ = "atoms"

    id = Column(Integer, primary_key=True, index=True)
    atom_id = Column(String, unique=True, index=True, nullable=False) # e.g., "BuyingZone.Ask.v1"
    intent = Column(String)
    pattern_data = Column(JSON, nullable=False) # Stores the "steps", "kpis", etc.