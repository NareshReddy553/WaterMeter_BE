from ninja_extra import ControllerBase, api_controller, route
from ninja_extra.permissions import IsAuthenticated, IsAdminUser
# from account.backends import JWTAuth
from ninja.errors import ValidationError

# from account.permissions import UserWithPermission
from account.models import Community
from account.permission import UserWithPermission
from account.schema.community_schema import CommunityCreateSchema, CommunityOutSchema, CommunityUpdateSchema


# from .schema import  PasswordUpdateSchema, UserCreateSchema, UserPermissionSchema, UserRoleAssignSchema, UserUpdateSchema, UserOutSchema
# from .services import CommunityService, UserService
from ninja_extra.pagination import (
    PageNumberPaginationExtra,
    paginate,
)

from ninja_extra import api_controller, route
from django.shortcuts import get_object_or_404
from typing import List
from django.db.models import Q
from ninja.errors import ValidationError
from ninja.errors import HttpError
from ninja_extra.exceptions import PermissionDenied
from ninja.responses import Response

from account.models import   UserProfile
# from .schema import (
#     UserCreateSchema,
#     UserUpdateSchema,
#     UserOutSchema,
# )
# from .services import UserService
from ninja_jwt.authentication import JWTAuth
from django.contrib.auth.models import Group, Permission
# from account.schema import GroupSchema, PermissionSchema, GroupUpdateSchema, PermissionUpdateSchema
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404




@api_controller("/community", tags=["Community"],permissions=[IsAuthenticated], auth=JWTAuth())
class CommunityController:
    @route.post("", response={200: CommunityOutSchema, 400: dict}, url_name="create",permissions=[UserWithPermission('account.add_community')])
    def create_community(self,request, data: CommunityCreateSchema):
        """
        Create a new community.
        """
        if request.user.is_superuser:
            try:
                community = Community.objects.create(**data.dict())
                return community
            except ValidationError as ex:
                return 400, dict(details=str(ex))
        else:
            raise PermissionDenied("You do not have permission to create a community.")

    @route.get("", response=PageNumberPaginationExtra.get_response_schema(CommunityOutSchema), url_name="list",permissions=[UserWithPermission('account.view_community')])
    @paginate(PageNumberPaginationExtra)
    def list_users(self):
        """
        List all users.
        """
        communities = Community.objects.filter(is_active=True)
        return communities

    @route.get("/{int:community_id}/", response=CommunityOutSchema, url_name="detail",permissions=[UserWithPermission('account.view_community')])
    def retrieve_community(self, community_id : int):
        """
        Get specific users.
        """     
        community = get_object_or_404(Community, id=community_id)
        return community

    @route.put("/{int:community_id}", response={200: CommunityOutSchema, 400: dict, 404: dict}, url_name="update",permissions=[UserWithPermission('account.change_community')])
    def update_community(self, community_id: int, data: CommunityUpdateSchema):
        """
        Update an existing user.
        """
        try:
            community = get_object_or_404(Community, id=community_id)
            for attr, value in data.dict(exclude_unset=True).items():
                setattr(community, attr, value)
            community.save()
            return community
        except ValidationError as ex:
            return 400, {"detail": str(ex)}

    @route.delete("/{int:community_id}", url_name="destroy", response={204: dict},permissions=[UserWithPermission('account.delete_community')])
    def delete_user(self, community_id: int):
        """
        Delete single user
        """
        community = get_object_or_404(Community, id=community_id)
        community.delete()
        return 204, dict(details="User deleted")

    
