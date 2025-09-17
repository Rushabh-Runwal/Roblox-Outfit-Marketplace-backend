"""
Shared contracts and Pydantic models for the agents package.
These models define the input/output contracts for agent communication.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class ChatIn(BaseModel):
    """Input contract for chat functionality."""
    prompt: str = Field(..., description="User prompt to the agent")
    user_id: int = Field(..., description="User ID")


class ChatOut(BaseModel):
    """Output contract for chat functionality."""
    success: bool = Field(..., description="Whether the request was successful")
    user_id: int = Field(..., description="User ID")
    reply: str = Field(..., description="Agent's reply to the user")


class RecommendIn(BaseModel):
    """Input contract for recommendation functionality."""
    theme: str = Field(..., description="Theme for outfit recommendations")
    user_id: int = Field(..., description="User ID")


class TagSpec(BaseModel):
    """Specification for tagging and filtering outfit recommendations."""
    theme: str = Field(..., description="Primary theme for the outfit")
    vibe: Optional[str] = Field(None, description="Additional vibe or mood specification")
    budget: Optional[int] = Field(None, description="Budget limit for the outfit")
    parts: Optional[List[str]] = Field(None, description="Specific parts to include in the outfit")


class CatalogItem(BaseModel):
    """Represents a single catalog item for outfits."""
    assetId: str = Field(..., description="Roblox asset ID as string")
    type: str = Field(..., description="Type of outfit item")


class RecommendOut(BaseModel):
    """Output contract for recommendation functionality."""
    success: bool = Field(..., description="Whether the request was successful")
    user_id: int = Field(..., description="User ID")
    message: str = Field(..., description="Recommendation message")
    outfit: List[CatalogItem] = Field(..., description="List of recommended outfit items")