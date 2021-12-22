from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.models import Project, Issue, Comment, User, Contributor
from api.serializers import (ContributorDetailSerializer, ContributorListSerializer,
    ProjectListSerializer, ProjectDetailSerializer, IssueListSerializer,
    IssueDetailSerializer, CommentListSerializer, UserListSerializer, UserDetailSerializer)


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serialize_class = ProjectDetailSerializer

    def get_queryset(self):
        return Project.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serialize_class
        return super().get_serializer_class()
    
    # Pour sauver l'author en tant que contributor lors de la création,
    # Peut être le faire ici plutot que dans les models


class IssueViewset(ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serialize_class = IssueDetailSerializer

    def get_queryset(self):
        return Issue.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serialize_class
        return super().get_serializer_class()


class CommentViewset(ModelViewSet):
    serializer_class = CommentListSerializer

    def get_queryset(self):
        return Comment.objects.all()


class UserViewset(ModelViewSet):
    serializer_class = UserListSerializer
    detail_serialize_class = UserDetailSerializer

    def get_queryset(self):
        print(self.kwargs)
        return User.objects.filter(
            id__in=Contributor.objects.filter(project=self.kwargs['project_pk'])
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serialize_class
        return super().get_serializer_class()

class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorListSerializer
    detail_serialize_class = ContributorDetailSerializer

    def get_queryset(self):
        contributors = Contributor.objects.filter(project=self.kwargs['project_pk'])
        return contributors
