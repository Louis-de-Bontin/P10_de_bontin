from django.db import models
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from api.models import Project, Issue, Comment


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['title', 'label', 'author', 'contributor']


class ProjectDetailSerializer(ModelSerializer):
    issues = SerializerMethodField()

    class Meta:
        model = Project
        fields = ['title', 'description', 'label', 'author', 'contributor', 'created_time', 'issues']

    def get_issues(self, instance):
        queryset = instance.issues.all()
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data



class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['name', 'tag', 'priority', 'status', 'created_time']


class IssueDetailSerializer(ModelSerializer):
    comments = SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['name', 'description', 'tag', 'priority', 'project', 'status',
            'initiator', 'assignee', 'created_time', 'comments']
    
    def get_comments(self, instance):
        queryset = instance.comments.filter()
        serializer = CommentListSerializer(queryset, many=True)
        return serializer.data

    


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['label', 'content', 'author', 'issue', 'created_time']    
