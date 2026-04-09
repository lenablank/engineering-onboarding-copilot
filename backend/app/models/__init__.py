"""
Database models for the Engineering Onboarding Copilot.
"""
from app.models.database import Base, engine, get_db
from app.models.gap import DocumentationGap

__all__ = ["Base", "engine", "get_db", "DocumentationGap"]
