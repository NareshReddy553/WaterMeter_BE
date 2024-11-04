from ninja import Schema
from typing import List, Optional

from account.schema.community_schema import CommunityOutSchema

class BlockWithFlatsSchema(Schema):
    block_id: int
    flats: List[int]

# Create schema for Block
class BlockCreateSchema(Schema):
    block_name: str
    description: Optional[str] = None
    community_id: int  # We will pass the community ID when creating a Block

# Update schema for Block
class BlockUpdateSchema(Schema):
    block_name: Optional[str] = None
    description: Optional[str] = None
    community_id: Optional[int] = None

# Response schema for Block
class BlockResponseSchema(Schema):
    block_name: str
    description: Optional[str]
    community: Optional[CommunityOutSchema]=None
