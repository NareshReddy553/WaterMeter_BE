from typing import List, Optional
from account.schema.community_schema import CommunityOutSchema
from ninja import Schema



# Schemas
class AuthUserPermissionSchema(Schema):
    codename: str
    name: str

class AuthUserRoleSchema(Schema):
    name: str
    permissions: List[AuthUserPermissionSchema]

class AuthUserWithRolesPermissionsSchema(Schema):
    user_id:int
    email: str
    first_name: str
    last_name: Optional[str]
    phone_number:Optional[str]
    is_active: bool
    community:dict
    roles: List[AuthUserRoleSchema]
    permissions: List[AuthUserPermissionSchema]