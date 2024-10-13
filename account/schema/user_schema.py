# schemas.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from ninja_schema import ModelSchema, model_validator
# from .models import  UserProfile
from typing import List, Optional
from ninja import Schema

from django.contrib.auth import get_user_model
from ninja_schema import ModelSchema, model_validator

from account.models import UserProfile
from account.schema.community_schema import CommunityOutSchema

UserModel = get_user_model()

from ninja import Schema
from pydantic import EmailStr
from typing import Optional

class UserCreateSchema(Schema):
    password:str
    confirm_password: str
    email: EmailStr
    first_name: str
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    user_type:Optional[str]=None
    community_id: int 
    block_id:Optional[int]=None
    flat_id:Optional[int]=None

class UserProfileUpdateSchema(Schema):
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    is_active: Optional[bool] = True
    user_type:Optional[str]=None
    community_id: Optional[int]


class UserProfileResponseSchema(Schema):
    user_id: int
    email: EmailStr
    first_name: str
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: bool
    user_type:Optional[str]=None
    community: Optional[CommunityOutSchema]

# class UserCreateSchema(ModelSchema):
#     confirm_password: str
    
#     @model_validator('username')
#     def validate_unique_username(cls, value_data: str) -> str:
#         if UserModel.objects.filter(username__icontains=value_data).exists():
#             raise ValueError('Username exists')
#         return value_data   
    
    
#     @model_validator('confirm_password')
#     def passwords_match(cls, value, values):
#         password = values.data.get('password')
#         if password is not None and value != password:
#             raise ValueError('Passwords do not match')
#         return value
    
#     class Config:
#         model=UserModel
#         include=['first_name', 'last_name', 'username', 'email','password']
#         optional=['last_name','phone_number','is_active']
class UserUpdateSchema(ModelSchema):

    class Config:
        model = get_user_model()
        optional = '__all__'

class UserOutSchema(ModelSchema):
    

    class Config:
        model = UserProfile
        exclude = ['password', 'last_login']
        fields_optional = '__all__'
        
        from_attributes = True

class PasswordUpdateSchema(BaseModel):
    current_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    

class GroupSchema(Schema):
    id: int
    name: str

class UserPermissionSchema(BaseModel):
    user_id: int
    permission_ids: List[int]

class PermissionSchema(Schema):
    id: int
    name: str
    codename: str
    content_type_id: int

class UserPermissionSchema(BaseModel):
    id: int
    username: str
    email: str
    permissions: List[PermissionSchema]
class GroupUpdateSchema(Schema):
    name: str

class PermissionUpdateSchema(Schema):
    name: str
    codename: str
    content_type_id: int
    
class UserRoleAssignSchema(Schema):
    roles: List[int]
    
    
class GroupPermissionCreateschema(Schema):
    group_id:int
    permission_id:List[int]
    
class GroupPermissionResponseSchema(Schema):
    group: GroupSchema
    permissions: List[PermissionSchema]

