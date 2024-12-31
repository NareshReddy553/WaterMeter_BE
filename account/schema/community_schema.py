# schemas.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from ninja_schema import ModelSchema, model_validator
# from .models import  UserProfile
from typing import List, Optional
from ninja import Schema

from django.contrib.auth import get_user_model
from ninja_schema import ModelSchema, model_validator

from ninja import Schema
from pydantic import Field
from typing import Optional

# Schema for creating a community
class CommunityCreateSchema(Schema):
    community_name: str = Field(..., max_length=255)
    address: str = Field(..., max_length=255)
    description: Optional[str] = None
    latitude:Optional[float]=None
    longitude:Optional[float]=None

# Schema for updating a community (partial fields)
class CommunityUpdateSchema(Schema):
    community_name: Optional[str] = Field(None, max_length=255)
    address: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    latitude:Optional[float]=None
    longitude:Optional[float]=None

# Schema for output (response) representation
class CommunityOutSchema(Schema):
    id: int
    community_name: str
    address: str
    description: Optional[str] = None
    latitude:Optional[float]=None
    longitude:Optional[float]=None
