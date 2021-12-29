from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from api.models import Contributor, Project, Issue, Comment, User

class ProjectListSerializer(ModelSerializer):
    issues_count = SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'label', 'get_author', 'issues_count']
    
    def get_issues_count(self, instance):
        issues = Issue.objects.filter(project = instance)
        return len(issues)


class ProjectDetailSerializer(ModelSerializer):
    issues = SerializerMethodField()
    contributions = SerializerMethodField()

    class Meta:
        model = Project
        fields = ['title', 'description', 'label', 'get_author', 'contributions', 'created_time', 'issues']

    def get_issues(self, instance):
        queryset = instance.issues.filter(project=instance.id)
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data
    
    def get_contributions(self, instance):
        queryset = Contributor.objects.filter(project=instance)
        serializer = ContributorListSerializer(queryset, many=True)
        return serializer.data


class ProjectFewInfo(ModelSerializer):

    class Meta:
        model = Project
        fields = ['title', 'id']


class IssueListSerializer(ModelSerializer):
    assignee = SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['name', 'assignee', 'priority', 'status', 'id']
    
    def get_assignee(self, instance):
        # serializer = UserListSerializer(instance.assignee)
        try:
            return instance.assignee.username
        except:
            return None


class IssueDetailSerializer(ModelSerializer):
    comments = SerializerMethodField()
    assignee = SerializerMethodField()
    initiator = SerializerMethodField()
    project_name = SerializerMethodField()

    class Meta:

        model = Issue
        fields = ['name', 'description', 'tag', 'priority', 'project_name', 'status',
            'initiator', 'assignee', 'created_time', 'comments']
    
    def get_comments(self, instance):
        queryset = instance.comments.all()
        serializer = CommentListSerializer(queryset, many=True)
        return serializer.data
    
    def get_assignee(self, instance):
        # serializer = UserListSerializer(instance.assignee)
        try:
            return instance.assignee.username
        except:
            return None

    def get_initiator(self, instance):
        # serializer = UserListSerializer(instance.initiator)
        try:
            return instance.initiator.username
        except:
            return None
    
    def get_project_name(self, instance):
        return instance.project.title


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['label', 'content', 'id']


class CommentDetailSerializer(ModelSerializer):
    author = SerializerMethodField()
    issue = SerializerMethodField()
    project = SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['label', 'content', 'id', 'author', 'issue', 'project', 'created_time']
    
    def get_author(self, instance):
        try:
            return instance.author.username
        except:
            return None

    def get_issue(self, instance):
        return instance.issue.name
    
    def get_project(self, instance):
        return instance.issue.project.title



class UserDetailSerializer(ModelSerializer):
    contribution = SerializerMethodField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'id', 'contribution']
    
    def get_contribution(self, instance):
        if type(instance) != User:
            return []

        try:
            project = Project.objects.get(id=self.context['view'].kwargs['project_pk'])
            queryset = Contributor.objects.get(user=instance, project=project)
            serializer = ContributorDetailSerializer(queryset)
        except:
            queryset = Contributor.objects.filter(user=instance)
            serializer = ContributorDetailSerializer(queryset, many=True)
        return serializer.data
        


class UserListSerializer(ModelSerializer):
    role = SerializerMethodField()
    class Meta:
        model = User
        fields = ['username', 'role', 'id']
    
    def get_role(self, instance):        
        return Contributor.objects.get(
            project=self.context['view'].kwargs['project_pk'],
            user=instance).role


class ContributorDetailSerializer(ModelSerializer):
    project = SerializerMethodField()

    class Meta:
        model = Contributor
        fields = ['project', 'role']
    
    def get_project(self, instance):
        serializer = ProjectFewInfo(instance.project)
        return serializer.data


class ContributorListSerializer(ModelSerializer):
    user = SerializerMethodField()
    user_id = SerializerMethodField()

    class Meta:
        model = Contributor
        fields = ['user', 'role', 'user_id']
    
    def get_user(self, instance):
        # serializer = UserListSerializer(instance.user)
        return instance.user.username
    
    def get_user_id(self, instance):
        return instance.user.id
