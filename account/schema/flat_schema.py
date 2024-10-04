from ninja import Schema
from typing import Optional

from account.schema.block_schema import BlockResponseSchema
from account.schema.community_schema import CommunityOutSchema
from account.schema.user_schema import UserProfileResponseSchema

# Create schema for Flat
class FlatCreateSchema(Schema):
    flat_number: str
    meter_no: str
    block_id: int  # The ID of the Block
    community_id: int  # The ID of the Community
    user_id: Optional[int] = None  # Optional: ID of the User (owner/tenant)

# Update schema for Flat
class FlatUpdateSchema(Schema):
    flat_number: Optional[str] = None
    meter_no: Optional[str] = None
    block_id: Optional[int] = None
    community_id: Optional[int] = None
    user_id: Optional[int] = None

# Response schema for Flat
class FlatResponseSchema(Schema):
    flat_number: str
    meter_no: str
    block:Optional[BlockResponseSchema]=None
    community:Optional[CommunityOutSchema]
    user: Optional[UserProfileResponseSchema] = None
