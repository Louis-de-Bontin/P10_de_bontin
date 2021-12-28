from rest_framework.permissions import BasePermission
from api import models


class PermissionUser(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        if request.method == 'GET' and request.user.is_authenticated:
            return True
        return False


# class IsProjectAuthor(BasePermission):
#     message = 'You must be the author of this project to perform this action.'

#     def has_permission(self, request, view):
#         print(super().has_permission(request, view))
#         return super().has_permission(request, view)
    
#     def has_object_permission(self, request, view, obj):
#         print(obj)
#         return request.user == obj.author


class IsProjectContributor(BasePermission):
    message = 'You must be author of this project to perform this action.'

    def has_object_permission(self, request, view, obj):
        print(view.project)
        if request.method == 'GET':
            contributions = view.project.contributions.get_queryset()
            for contrib in contributions:
                if request.user == contrib.user:
                    return True
            return False
        else:
            return request.user == obj.author

class WriteComments(BasePermission):
    message = 'You are not initiator nor assignee for this issue.'

    def has_permission(self, request, view):
        # print(request.method)
        issue = models.Issue.objects.get(id=view.kwargs['issue_pk'])
        if request.user == issue.initiator or request.user == issue.assignee:
            return True
        else:
            return False