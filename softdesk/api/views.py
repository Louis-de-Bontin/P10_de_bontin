from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied

from rest_framework_simplejwt.authentication import JWTAuthentication

from api import serializers, exceptions, models, permissions


class CommunFuctionsMixin:
    """
    Some functions are commun for some of the view. You can find them in
    this mixin.
    """
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    def get_project(self, id, user=None):
        if user:
            return get_object_or_404(
                models.Project, id=id, contributors=user)
        else:    
            return get_object_or_404(
                models.Project, id=id)
    
    def get_user(self, label, value):
        if label == 'id':
            return get_object_or_404(models.User, id=value)
        elif label == 'username':
            return get_object_or_404(models.User, username=value)
    
    def get_issue(self, id):
        return get_object_or_404(models.Issue,
            id=id)

class SignupView(CommunFuctionsMixin, ModelViewSet):
    """
    This endpoint allow a new user to create a profile.
    An authentified user is able to have the list of the other users,
    and to have the details of one profile.
    """
    serializer_class = serializers.UserListSerializer
    detail_serializer_class = serializers.UserDetailSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.PermissionUser]

    def get_queryset(self):
        return models.User.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'create':
            return self.detail_serializer_class
        if self.action == 'list':
            return super().get_serializer_class()
    
    def perform_create(self, serializer):
        new_user = models.User()
        new_user.set_password(self.request.POST['password'])
        new_user.username = self.request.POST['username']
        new_user.email = self.request.POST['email']
        if 'first_name' in self.request.POST:
            new_user.first_name = self.request.POST['first_name']
        if 'last_name' in self.request.POST:
            new_user.last_name = self.request.POST['last_name']
        new_user.save()
        

class ProjectViewset(CommunFuctionsMixin, ModelViewSet):
    """
    This endpoint allow an authentified user to create a project, or to get the list
    of the projects on which he is contributor.
    He can also modify a project, but only if he is the author of the said project.
    """
    serializer_class = serializers.ProjectListSerializer
    detail_serializer_class = serializers.ProjectDetailSerializer

    permission_classes = [
        IsAuthenticated,
        permissions.IsProjectContributor
    ]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        self.project = models.Project.objects.filter(
            contributors=self.request.user)

        return self.project
    
    def perform_create(self, serializer):
        author = self.request.user
        project = serializer.save(author=author)

        if 'description' in self.request.POST:
            project.description = self.request.POST['description']

        models.Contributor(project=project,
            user=author, role='AUTH').save()

        return super().perform_create(serializer)
    
    def perform_update(self, serializer):
        if 'description' in self.request.POST:
            serializer.save(description=self.request.POST['description'])

        return super().perform_update(serializer)


class ContributorViewSet(CommunFuctionsMixin, ModelViewSet):
    """
    This endpoint allow a connected user to read and update the users of a
    project. All the contributor of the project can read the users attached
    to the project (id in url), but only the author can add or remove a user
    from it.
    This endpoint is a bit special, because if I want to display the list of
    user, I use a Contributor serializer, but if I want the details, I user a
    User serializer. Why ? 
    """
    serializer_class = serializers.UserListSerializer
    detail_serializer_class = serializers.UserDetailSerializer

    permission_classes = [IsAuthenticated, permissions.IsAllowedToAddUser]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        self.project = get_object_or_404(models.Project,
            id=self.kwargs['project_pk'], contributors=self.request.user)
        return models.User.objects.filter(contrib__project=self.project)
    
    def create(self, request, *args, **kwargs):
        try:
            user = self.get_user('username', self.request.POST['username'])
            project=self.get_project(self.kwargs['project_pk'], request.user)
            models.Contributor(user=user, project=project, role='CON').save()
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise exceptions.UserAlreadyInProject(
                detail={'This user already work on this project or username not in request.': 'Conflict'})
    
    def perform_destroy(self, request, *args, **kwargs):
        try:
            contrib = get_object_or_404(models.Contributor,
                project=self.get_project(self.kwargs['project_pk']),
                user=self.get_user('id', self.kwargs['pk']),
                role='CON'
                )
            contrib.delete()

            serializer = self.get_serializer(self.get_queryset(), many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            raise PermissionDenied(detail={
                'This user doesn\'t work on this project, or is author, or doesn\'t exist': 'Forbiden'})
    
    def update(self, request):
        raise MethodNotAllowed()


class IssueViewset(CommunFuctionsMixin, ModelViewSet):
    """
    This endpoint is in charge of the issues. Accessing this endpoint, the user
    access the issues related to a project. His id is in the url.
    An authenticated user can see the
    issues of the choosen project if he is one of the contributors. Respecting
    this conditions, he can also create a new issue, of modify one is he is the
    initiator of the said issue.
    """
    serializer_class = serializers.IssueListSerializer
    detail_serializer_class = serializers.IssueDetailSerializer

    permission_classes = [IsAuthenticated, permissions.IsAllowedToInterectWithIssues]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return models.Issue.objects.filter(
            project=self.get_project(self.kwargs['project_pk']))
    
    def perform_create(self, serializer):
        # Authorisation : conecté et contributor du projet
        initiator = self.request.user
        project = self.get_project(self.kwargs['project_pk'])
        serializer.save(initiator=initiator, project=project,
            assignee=self.get_assignee(serializer, initiator, project))

    def perform_update(self, serializer):
        self.issue = self.get_issue(self.kwargs['pk'])
        serializer.save(initiator=self.issue.initiator, project=self.issue.project,
            assignee=self.get_assignee(serializer, self.issue.initiator, self.issue.project))
    
    def get_assignee(self, serializer, initiator, project):
        if 'assignee' in self.request.POST:
            assignee = self.get_user('username',self.request.POST['assignee'])
            try:
                models.Contributor.objects.get(project=project, user=assignee)
                return assignee

            except:
                raise exceptions.UserNotInProject(detail={
                    'This user doesn\'t work on this project or doesn\'t exist': 'User not found'})
        
        elif self.action == 'update':
            return self.issue.assignee
        else:
            return initiator
    
    def perform_destroy(self, instance):
        """
        Quand on retire un utilisateur du projet, si il était initiateur ou assignee
        pour une issue, set blank
        """
        return super().perform_destroy(instance)


class CommentViewset(CommunFuctionsMixin, ModelViewSet):
    """
    This endpoint is in charge of the comments. All comments are related to an
    issue, so, this endpoint will manage the comments related to an issue. The
    id of the said issue is in the url.
    If the user is contributor of the project related to the issue, he is able
    to read all the comments of the issue requested.
    He is also able to create new comments if he is initator or assignee of the
    issue. And last, he can modify a comment if he is the author of it.
    """
    serializer_class = serializers.CommentListSerializer
    detail_serializer_class = serializers.CommentDetailSerializer

    permission_classes = [IsAuthenticated, permissions.IsAllowedToInteractWithComments]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return models.Comment.objects.filter(issue=self.get_issue(self.kwargs['issue_pk']))
    
    def perform_create(self, serializer):
        issue = self.get_issue(self.kwargs['issue_pk'])
        serializer.save(issue=issue, author=self.request.user)
