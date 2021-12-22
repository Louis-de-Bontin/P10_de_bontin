from rest_framework.serializers import ModelSerializer, SerializerMethodField

from api.models import Contributor, Project, Issue, Comment, User


class ProjectListSerializer(ModelSerializer):
    contributors = SerializerMethodField()

    class Meta:
        model = Project
        fields = ['title', 'label', 'author', 'contributors']
    
    def get_contributors(self, instance):
        contributors = Contributor.objects.filter(project=instance)
        queryset = User.objects.filter(id__in=contributors)
        serializer = UserListSerializer(queryset, many=True)
        return serializer.data


class ProjectDetailSerializer(ModelSerializer):
    issues = SerializerMethodField()
    contributors = SerializerMethodField()

    class Meta:
        model = Project
        fields = ['title', 'description', 'label', 'author', 'contributors', 'created_time', 'issues']

    def get_issues(self, instance):
        queryset = instance.issues.filter(project=instance.id)
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data
    
    def get_contributors(self, instance):
        queryset = Contributor.objects.filter(project=instance)
        # queryset = User.objects.filter(id__in=contributors)
        serializer = ContributorListSerializer(queryset, many=True)
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
        queryset = instance.comments.all()
        serializer = CommentListSerializer(queryset, many=True)
        return serializer.data

    


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['label', 'content', 'author', 'issue', 'created_time']



class UserDetailSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class UserListSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username']


class ContributorDetailSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['project', 'user']


class ContributorListSerializer(ModelSerializer):
    user = SerializerMethodField()

    class Meta:
        model = Contributor
        fields = ['user']
    
    def get_user(self, instance):
        serializer = UserListSerializer(instance.user)
        return serializer.data
