from account.schema.authUserSchemas import AuthUserWithRolesPermissionsSchema
from ninja_extra import ControllerBase, api_controller, route
from ninja_extra.permissions import IsAuthenticated, IsAdminUser
# from account.backends import JWTAuth
from ninja.errors import ValidationError

# from account.permissions import UserWithPermission


# from .schemas import  PasswordUpdateSchema, UserCreateSchema, UserPermissionSchema, UserRoleAssignSchema, UserUpdateSchema, UserOutSchema
# from .services import UserService
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
from ninja.responses import Response
# from .models import   UserProfile
# from .schemas import (
#     UserCreateSchema,
#     UserUpdateSchema,
#     UserOutSchema,
# )
# from .services import UserService
from ninja_jwt.authentication import JWTAuth
from django.contrib.auth.models import Group, Permission
# from account.schemas import GroupSchema, PermissionSchema, UserUpdateSchema, GroupUpdateSchema, PermissionUpdateSchema
from django.contrib.auth import get_user_model
from ninja_extra.exceptions import PermissionDenied

from account.models import UserProfile
from account.permission import UserWithPermission
from account.schema.user_schema import GroupPermissionCreateschema, GroupPermissionResponseSchema, GroupSchema, GroupUpdateSchema, PasswordUpdateSchema, PermissionSchema, PermissionUpdateSchema, UserCreateSchema, UserOutSchema, UserPermissionSchema, UserRoleAssignSchema, UserUpdateSchema
from account.services import UserService
from django.forms.models import model_to_dict
from django.db.models import Q

UserModel = get_user_model()

@api_controller("/user",tags=["user"],permissions=[IsAuthenticated],auth=JWTAuth())
class UserController:
    @route.post("", response={200: UserOutSchema, 400: dict}, url_name="create",permissions=[UserWithPermission('account.add_userprofile')])
    def create_user(self,request, data: UserCreateSchema):
        """
        Create a new user.
        """
        try:
            user = UserService.create_user(data)
            if request.user.is_superuser:
                # Assign the community owner/admin role to the new user
                admin_group, created = Group.objects.get_or_create(name='Community Admin') 
                
                # Assign all permissions to the admin group if it was just created
                if created:
                    all_permissions = Permission.objects.all()
                    admin_group.permissions.set(all_permissions)

                user.groups.add(admin_group)
            return user
        except Exception as e:
            return 400, {"error": str(e)}
        
    @route.get("", response=PageNumberPaginationExtra.get_response_schema(UserOutSchema), url_name="list",permissions=[UserWithPermission('account.view_userprofile')])
    @paginate(PageNumberPaginationExtra)
    def list_users(self):
        """
        List all users.
        """
        return UserService.list_users()

    @route.get("/{int:user_id}/", response=UserOutSchema, url_name="detail",permissions=[UserWithPermission('account.view_userprofile')])
    def retrieve_user(self, user_id: int):
        """
        Get specific users.
        """
        user = UserService.get_user(user_id)
        if not user:
            return 404, dict(details="User not found")
        return user
    @route.get("/me", response={200: dict, 401: dict}, url_name="detail",permissions=[UserWithPermission('account.view_userprofile')])
    def get_authenticated_user(self,request):
        """
        Get auth user details along with his roles and permissions.
        """
        if not request.user.is_authenticated:
            return {"error": "User is not authenticated"}, 401

        # Convert user model to dict
        user = request.user
        # Fetch community data
        community_data = model_to_dict(user.community) if user.community else {}

        # Fetch user roles and their permissions
        roles = []
        for group in request.user.groups.prefetch_related('permissions').all():
            group_data = model_to_dict(group)  # Convert group model to dict
            permissions = [model_to_dict(perm) for perm in group.permissions.all()]  # Convert permissions to dicts

            roles.append({
                **group_data,  # Include all group fields
                "permissions": permissions  # Include permissions in the role
            })

        # Fetch user permissions (direct and role-based)
        permissions = list(
            Permission.objects.filter(
                Q(user=request.user) | Q(group__user=request.user)
            ).distinct().values()
        )

        # Combine everything into the final response
        return {
            "user_id":user.user_id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number":user.phone_number,
            "is_active": user.is_active,
            "community":community_data,
            "roles": roles,
            "permissions": permissions,
        }

    @route.put("/{int:user_id}", response={200: UserOutSchema, 400: dict, 404: dict}, url_name="update",permissions=[UserWithPermission('account.change_userprofile')])
    def update_user(self, user_id: int, data: UserUpdateSchema):
        """
        Update an existing user.
        """
        try:
            user = UserService.update_user(user_id, data)
            if user:
                return 200, user
            return 404, {"detail": "User not found"}
        except ValidationError as ex:
            return 400, {"detail": str(ex)}

    @route.delete("/{int:user_id}", url_name="destroy", response={204: dict},permissions=[UserWithPermission('account.delete_userprofile')])
    def delete_user(self, user_id: int):
        """
        Delete single user
        """
        UserService.delete_user(user_id)
        return 204, dict(details="User deleted")

    
    @route.post("/inactivate", response={200: dict}, url_name="inactivate_users", permissions=[UserWithPermission('account.change_userprofile')])
    def inactivate_users(self, request, user_id_list: List[int]):  
        """Inactivate users by setting is_active flag to False."""
        if not user_id_list:
            raise ValidationError({"user_id_list": "user_id_list should not be None or empty string."})
        UserProfile.objects.filter(user_id__in=user_id_list).update(is_active=False)
        return {"details": "Users inactivated successfully."}
    
    
    @route.post("/{int:user_id}/add-user-groups", response={201: str},permissions=[UserWithPermission('account.add_user_group')])
    def assign_groups_to_user(self,user_id:int, data: UserRoleAssignSchema):
        """
        Assign Roles/Groups to user
        """
        try:
            user = UserModel.objects.get(pk=user_id)
            groups = Group.objects.filter(id__in=data.roles)

            if not groups.exists():
                raise HttpError(404, "No valid roles found.")

            user.groups.set(groups)
            return "Group assigned to user successfully."   
        except UserModel.DoesNotExist:
            raise HttpError(404, "User not found.")
    
    @route.post("/del-group-users", response={204: dict}, url_name="del_group_users",permissions=[UserWithPermission('account.delete_user_group')])
    def delete_group_users(self, request, role_id: int, user_id_list: List[int]):
        """
        Delete users assigned to a particular Group.
        """
        if not user_id_list:
            return {"error": "user_id_list cannot be empty"}, 400
        # Assuming you have a ManyToMany relationship between Group and User
        group = get_object_or_404(Group, id=role_id)
        # Remove users from the group
        group.user_set.remove(*user_id_list)
        return Response(status=204)
    
    @route.post("/assign-user-permissions/",permissions=[UserWithPermission('account.add_user_permissions')])
    def assign_user_permissions(request, data: UserPermissionSchema):
        user = get_object_or_404(UserModel, id=data.user_id)
        permissions = Permission.objects.filter(id__in=data.permission_ids)
        user.user_permissions.set(permissions)
        return {"success": True}

    @route.get("/user/{user_id}", response=UserPermissionSchema,permissions=[UserWithPermission('account.get_user_permissions')])
    def get_user_permissions(request, user_id: int):
        user = get_object_or_404(UserModel, id=user_id)
        permissions = user.user_permissions.all()
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "permissions": [{"id": perm.id, "name": perm.name, "codename": perm.codename} for perm in permissions]
        }
    
    @route.post("/update-password", response={200: dict, 400: dict, 401: dict},permissions=[UserWithPermission('account.change_userprofile')])
    def update_user_password(request, payload: PasswordUpdateSchema):
        user = request.user
        if not user.check_password(payload.current_password):
            return {"error": "Current password is incorrect"}, 401
        if payload.new_password != payload.confirm_password:
            return {"error": "New password and confirmation password do not match"}, 400
        user.set_password(payload.new_password)
        user.save()
        return {"Details": "Password updated successfully"}
    
@api_controller("/groups", permissions=[IsAuthenticated],auth=JWTAuth())
class GroupController:
    
    @route.get("", response=List[GroupSchema])
    def list_groups(self, request):
        """
        List of Groups
        """
        groups = Group.objects.all()
        return groups

    @route.get("/{int:group_id}", response=GroupSchema)
    def get_group(self, request, group_id: int):
        """
        Get single Group
        """
        group = Group.objects.get(id=group_id)
        return group
    
    @route.post("", response=GroupSchema)
    def create_group(self, request, group: GroupUpdateSchema):
        """
        Create Group
        """
        group_instance = Group.objects.create(name=str(group.name).capitalize())
        return group_instance
    
    @route.put("/{int:group_id}", response=GroupSchema)
    def update_group(self, request, group_id: int, group: GroupUpdateSchema):
        """
        Update the Group
        """
        group_instance = Group.objects.get(id=group_id)
        group_instance.name = group.name
        group_instance.save()
        return group_instance
    
    @route.delete("/groups/{group_id}")
    def delete_group(self, request, group_id: int):
        """
        Delete the Group
        """
        group_instance = Group.objects.get(id=group_id)
        group_instance.delete()
        return {"success": True}
    
@api_controller("/permissions", permissions=[IsAuthenticated], auth=JWTAuth())
class PermissionController:
    @route.get("", response=List[PermissionSchema])
    def list_permissions(self, request):
        """
        List of Permissions
        """
        permissions = Permission.objects.all()
        return permissions

    @route.get("/{int:permission_id}", response=PermissionSchema)
    def get_permission(self, request, permission_id: int):
        """
        Get permissions
        """
        permission = Permission.objects.get(id=permission_id)
        return permission

    @route.post("", response=PermissionSchema)
    def create_permission(self, request, permission: PermissionUpdateSchema):
        """
        Create Permissions
        """
        permission_instance = Permission.objects.create(
            name=permission.name,
            codename=permission.codename,
            content_type_id=permission.content_type_id
        )
        return permission_instance

    @route.put("/{int:permission_id}", response=PermissionSchema)
    def update_permission(self, request, permission_id: int, permission: PermissionUpdateSchema):
        """
        Update Permissions
        """
        permission_instance = Permission.objects.get(id=permission_id)
        permission_instance.name = permission.name
        permission_instance.codename = permission.codename
        permission_instance.content_type_id = permission.content_type_id
        permission_instance.save()
        return permission_instance

    @route.delete("/{int:permission_id}")
    def delete_permission(self, request, permission_id: int):
        """
        Delete Permissions
        """
        permission_instance = Permission.objects.get(id=permission_id)
        permission_instance.delete()
        return {"success": True}
  
@api_controller("/grouppermission", permissions=[IsAuthenticated],auth=JWTAuth())
class GroupPermissionController:
    
    @route.get("", response=List[GroupPermissionResponseSchema])  # Update response type to include permissions
    def list_grouppermission(self, request):
        """
        List of all the group permission
        """
        groups = Group.objects.prefetch_related('permissions').all()  # Prefetch permissions to optimize queries
        return [
            {
                "group": GroupSchema.from_orm(group),  # Convert group to schema
                "permissions": [PermissionSchema.from_orm(perm) for perm in group.permissions.all()]  # Convert permissions to schema
            }
            for group in groups
        ]    
        
    @route.post("", response={200:bool, 400: dict, 401: dict})
    def create_group_permission(self, request, payload: GroupPermissionCreateschema):
        """
        Create Permissions
        """
        # Get or create a group
        group = get_object_or_404(Group,id=payload.group_id)

        # Retrieve a specific permission
        permissions = Permission.objects.filter(id__in=payload.permission_id)

        # Add the permission to the group
        group.permissions.add(*permissions)
    #     return {
    #     "group": GroupSchema(id=group.id, name=group.name),
    #     "permissions": [
    #         PermissionSchema(
    #             id=perm.id,
    #             name=perm.name,
    #             codename=perm.codename
    #         ) for perm in permissions
    #     ]
    # }
        return True


