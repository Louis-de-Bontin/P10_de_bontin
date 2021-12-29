from django.views.generic import base
from rest_framework.permissions import BasePermission
from rest_framework.generics import get_object_or_404
from api import models


class MixinContributor:
    message = 'You are not contributor of this project.'

    def is_contributor(self, view, request):
        project = get_object_or_404(models.Project,
            id=view.kwargs['project_pk'], contributors=request.user)
        contributions = project.contributions.get_queryset()

        for contrib in contributions:
            if request.user == contrib.user:
                return True
        return False


class PermissionUser(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        if request.method == 'GET' and request.user.is_authenticated:
            return True
        return False
        

class IsProjectContributor(MixinContributor, BasePermission):
    """
    True if the user is author of the project for any actions.
    True if the user is contributor and the method is GET.
    """
    message = 'You must be author of this project to perform this action.'

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True
        return self.is_contributor(view, request) and request.method == 'GET'


class IsAllowedToAddUser(MixinContributor, BasePermission):
    def has_permission(self, request, view):
        
        if view.action == 'create':
            return self.has_object_permission(request, view)

        return self.is_contributor(view, request)

    def has_object_permission(self, request, view, obj=None):
        self.message = 'You must be author of this project to perform this action.'
        project = get_object_or_404(models.Project,
            id=view.kwargs['project_pk'], contributors=request.user)
        return request.user == project.author


class IsAllowedToInterectWithIssues(MixinContributor, BasePermission):
    def has_permission(self, request, view):
        return self.is_contributor(view, request)
    
    def has_object_permission(self, request, view, obj=None):
        if request.method == 'GET':
            return True

        self.message = 'You must be initiator, assignee to this issue or author of the project to perform this action.'
        project = get_object_or_404(models.Project,
            id=view.kwargs['project_pk'], contributors=request.user)
        issue = get_object_or_404(models.Issue, id=view.kwargs['pk'])
        if request.user == project.author:
            return True
        if request.user == issue.initiator or request.user == issue.assignee:
            return True


class IsAllowedToInteractWithComments(MixinContributor, BasePermission):
    def has_permission(self, request, view):
        self.is_contributor(view, request)
        return self.is_contributor(view, request)
    
    def has_object_permission(self, request, view, obj):
        self.message = 'You must be the author of the comment to perform this action.'
        if request.method == 'GET':
            return True
        if obj.author == request.user:
            return True
        return False 
