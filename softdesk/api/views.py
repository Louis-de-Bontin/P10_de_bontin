from django import contrib
from django.db.models.fields import PositiveBigIntegerField
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.models import Project, Issue, Comment, User, Contributor
from api.serializers import (ContributorDetailSerializer, ContributorListSerializer,
    ProjectListSerializer, ProjectDetailSerializer, IssueListSerializer,
    IssueDetailSerializer, CommentListSerializer, UserListSerializer, UserDetailSerializer)

from itertools import chain


class SignupView(ModelViewSet):
    serializer_class = UserListSerializer
    detail_serialize_class = UserDetailSerializer

    def get_queryset(self):
        print(self.request.user)
        return User.objects.all()
    
    def get_serializer_class(self):
        print(self.request.method)
        if self.action == 'retrieve':
            return self.detail_serialize_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        user = User()

        for element in request.POST:
            setattr(user, element, request.POST[element])
        
        user.save()
        return Response()


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serialize_class = ProjectDetailSerializer

    def get_queryset(self):
        return Project.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serialize_class
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        author = User.objects.get(username=request.POST['author'])

        project = Project(title=request.POST['title'],
            label=request.POST['label'], author=author)
        if 'description' in request.POST:
            project.description = request.POST['description']
        project.save()

           
        contrib = Contributor(project=project,
            user=author)
        contrib.save()   

        return Response()
    
    def update(self, request, *args, **kwargs):
        project = Project.objects.get(id=self.kwargs['pk'])

        for element in request.POST:
            if element == 'author':
                """
                On supprime l'ancien author des contributor,
                on update l'author dans projet, puis on créé
                un nouveau contributor.
                """
                Contributor.objects.filter(project=project,
                    role='AUTH').delete()

                project.author = User.objects.get(username=request.POST['author'])
                project.save()
           
                contrib = Contributor(project=project,
                    user=project.author)
                contrib.save()                   
            else:
                setattr(project, element, request.POST[element])

        project.save()
        return Response()


class IssueViewset(ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serialize_class = IssueDetailSerializer

    def get_queryset(self):
        project = Project.objects.get(id=self.kwargs['project_pk'])
        return Issue.objects.filter(project=project)
    
    def create(self, request, *args, **kwargs):
        """
        Ici je n'utilise pas de setattr car j'associe des objets.
        """
        # Pour l'initiator, il faudra le définir à l'utilisateur loggé
        # Si on ajoute un assignee qui n'est pas dans des contributeurs,
        # L'ajouter aux contributeurs
        project = Project.objects.get(id=self.kwargs['project_pk'])
        
        issue = Issue(
            name=request.POST['name'],
            priority=request.POST['priority'],
            project=project,
            status=request.POST['status']
        )

        if 'description' in request.POST:
            issue.description = request.POST['description'],
        if 'tag' in request.POST:
            issue.tag = request.POST['tag']
        if 'assignee' in request.POST:
            issue.assignee = User.objects.get(username=request.POST['assignee'])
            contribution = Contributor.objects.filter(project=project, user=issue.assignee)
            if len(contribution) == 0:
                contribution = Contributor(
                    project=project,
                    user=issue.assignee,
                    role='CON'
                ).save()

        issue.save()
        return Response()
    
    def update(self, request, *args, **kwargs):
        issue = Issue.objects.get(id=self.kwargs['pk'])
        for element in request.POST:
            if element == 'assignee':
                issue.assignee = User.objects.get(
                    username=User.objects.get(username=request.POST[element]))
            else:
                setattr(issue, element, request.POST[element])

        issue.save()
        return Response()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serialize_class
        return super().get_serializer_class()


class CommentViewset(ModelViewSet):
    serializer_class = CommentListSerializer

    def get_queryset(self):
        return Comment.objects.all()


# class UserViewset(ModelViewSet):
#     serializer_class = UserListSerializer
#     detail_serialize_class = UserDetailSerializer

#     def get_queryset(self):
#         project = Project.objects.get(id=int(self.kwargs['project_pk']))
#         print(project.contributors)
#         users = User.objects.filter(
#             id__in=Contributor.objects.filter(project=project)
#         )
#         print(users)
#         return users

#     def get_serializer_class(self):
#         if self.action == 'retrieve':
#             return self.detail_serialize_class
#         return super().get_serializer_class()


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorListSerializer
    detail_serialize_class = UserDetailSerializer

    def get_queryset(self):
        if 'pk' in self.kwargs:
            a = self.kwargs['pk'] # Je vérifis qu'il y ai un id user
            project = Project.objects.get(id=self.kwargs['project_pk'])
            user = User.objects.get(id=self.kwargs['pk'])
            contrib = Contributor.objects.filter(project=project, user=user)
            if len(contrib) > 0:
                return User
        else:
            project = Project.objects.get(id=self.kwargs['project_pk'])
            contrib = Contributor.objects.filter(project=project)

            return contrib
    
    def create(self, request, *args, **kwargs):
        project = Project.objects.get(id=self.kwargs['project_pk'])
        user = User.objects.get(username=request.POST['username'])
        contributors = Contributor.objects.filter(project=project, user=user)
        if len(contributors) == 0:
            new_contribution = Contributor(
                user=user,
                project=project,
                role='CON'
            )
            new_contribution.save()
        return Response()
    
    def destroy(self, request, *args, **kwargs):
        project = Project.objects.get(id=self.kwargs['project_pk'])
        user = User.objects.get(id=self.kwargs['pk'])
        contributors = Contributor.objects.filter(project=project, user=user)
        if len(contributors) > 0:
            contributors.delete()
        return Response()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serialize_class
        return super().get_serializer_class()
        