from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.models import Project, Issue, Comment
from api.serializers import (ProjectListSerializer, ProjectDetailSerializer,
    IssueListSerializer, IssueDetailSerializer, CommentListSerializer)


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serialize_class = ProjectDetailSerializer

    def get_queryset(self):
        return Project.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serialize_class
        return super().get_serializer_class()


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
