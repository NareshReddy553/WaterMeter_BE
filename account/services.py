# services.py
from typing import List
from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja.errors import ValidationError
from django.contrib.auth.models import Group

from account.schema.block_schema import BlockCreateSchema, BlockUpdateSchema
from account.schema.flat_schema import FlatCreateSchema, FlatUpdateSchema
from account.schema.user_schema import UserCreateSchema, UserUpdateSchema
from .models import Block, Community, Flat, UserProfile
# from .schemas import  UserCreateSchema, UserUpdateSchema
# from .utils import get_hashed_password


class UserService:
    @staticmethod
    @transaction.atomic
    def create_user(data: UserCreateSchema) -> UserProfile:
        user_data = data.model_dump(exclude_unset=True)
        # if 'email' in user_data and UserProfile.objects.filter(email=user_data['email']).exists():
        #     raise ValidationError("User with this email already exists")
        # if 'username' in user_data and UserProfile.objects.filter(username=user_data['username']).exists():
        #     raise ValidationError("User with this username already exists")

        user = UserProfile.objects.create_user(
            email=user_data.get('email', ''),
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
            phone_number=user_data.get('phone_number', ''),
            password=user_data.get('password', ''),
            is_active=user_data.get('is_active', True),
            user_type=user_data.get('user_type',''),
            community_id=user_data.get('community_id')
        )
        
        block_id=user_data.get("block_id")
        flat_id=user_data.get("flat_id")
        
        if block_id and flat_id:
            flat = get_object_or_404(Flat, id=flat_id)
            flat.block_id=block_id
            flat.user_id=user.pk
            flat.save()
        # if user.is_community_owner:
        #    group, created= Group.objects.get_or_create(name="Community Owner")
       
        return user

    @staticmethod
    @transaction.atomic
    def update_user(user_id: int, data: UserUpdateSchema) -> UserProfile:
        user = UserProfile.objects.get(pk=user_id)
        for attr, value in data.model_dump(exclude_unset=True).items():
            setattr(user, attr, value)
        user.save()
        return user

    @staticmethod
    def list_users():
        return UserProfile.objects.all()

    @staticmethod
    def get_user(user_id: int) -> UserProfile:
        return UserProfile.objects.get(pk=user_id)

    @staticmethod
    @transaction.atomic
    def delete_user(user_id: int):
        user = UserProfile.objects.get(pk=user_id)
        user.delete()


class BlockService:
    
    @staticmethod
    def create_block(payload: BlockCreateSchema):
        community = get_object_or_404(Community, id=payload.community_id)
        block = Block.objects.create(
            block_name=payload.block_name,
            description=payload.description,
            community=community
        )
        return block

    @staticmethod
    def update_block(block_id: int, payload: BlockUpdateSchema):
        block = get_object_or_404(Block, id=block_id)
        if payload.block_name:
            block.block_name = payload.block_name
        if payload.description:
            block.description = payload.description
        if payload.community_id:
            community = get_object_or_404(Community, id=payload.community_id)
            block.community = community
        block.save()
        return block

    @staticmethod
    def delete_block(block_id: int):
        block = get_object_or_404(Block, id=block_id)
        block.delete()

    @staticmethod
    def get_block(block_id: int):
        block = get_object_or_404(Block, id=block_id)
        return block

    @staticmethod
    def list_blocks():
        return Block.objects.all()
    
class FlatService:

    @staticmethod
    def create_flat(payload: FlatCreateSchema):
        block = get_object_or_404(Block, id=payload.block_id)
        community = get_object_or_404(Community, id=payload.community_id)
        user = None
        if payload.user_id:
            user = get_object_or_404(UserProfile, id=payload.user_id)
        flat = Flat.objects.create(
            flat_number=payload.flat_number,
            meter_no=payload.meter_no,
            block=block,
            community=community,
            user=user
        )
        return flat

    @staticmethod
    def update_flat(flat_id: int, payload: FlatUpdateSchema):
        flat = get_object_or_404(Flat, id=flat_id)
        if payload.flat_number:
            flat.flat_number = payload.flat_number
        if payload.meter_no:
            flat.meter_no = payload.meter_no
        if payload.block_id:
            block = get_object_or_404(Block, block_id=payload.block_id)
            flat.block = block
        if payload.community_id:
            community = get_object_or_404(Community, community_id=payload.community_id)
            flat.community = community
        if payload.user_id:
            user = get_object_or_404(UserProfile, user_id=payload.user_id)
            flat.user = user
        flat.save()
        return flat

    @staticmethod
    def delete_flat(flat_id: int):
        flat = get_object_or_404(Flat, id=flat_id)
        flat.delete()

    @staticmethod
    def get_flat(flat_id: int):
        flat = get_object_or_404(Flat, id=flat_id)
        return flat

    @staticmethod
    def list_flats():
        return Flat.objects.all()