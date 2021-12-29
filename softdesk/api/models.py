from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    first_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)
    email = models.EmailField(max_length=128)
    password = models.CharField(max_length=128)


class Project(models.Model):

    class Label(models.TextChoices):
        BACKEND = 'BE'
        FRONTEND = 'FE'
        IOS = 'IOS'
        ANDROID = 'AN'

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=8192, blank=True)
    label = models.CharField(choices=Label.choices, max_length=128)
    # Set null because the creator of the project can leave it without canceling the project
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='author')
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Contributor', symmetrical=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_author(self):
        try:
            return self.author.username
        except:
            return None


class Contributor(models.Model):
    class Role(models.TextChoices):
        CONTRIBOTOR = 'CON'
        AUTHOR = 'AUTH'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contrib')
    role = models.CharField(choices=Role.choices, default='AUTH', max_length=10)

    class Meta:
        unique_together = ('project', 'user')


class Issue(models.Model):
    class Priority(models.TextChoices):
        HIGH = 'H'
        NORMAL = 'N'
        LOW = 'L'
    
    class Balise(models.TextChoices):
        BUG = 'BUG'
        IMPROVEMENT = 'IMP'
        TASK = 'TASK'

    class Status(models.TextChoices):
        DONE = 'DONE'
        PROCESSING = 'PRO'
        TO_DO = 'TODO'

    name = models.CharField(max_length=128)
    description = models.TextField(max_length=8192, blank=True)
    balise = models.CharField(choices=Balise.choices, default='TASK', max_length=4)
    priority = models.CharField(choices=Priority.choices, default='L', max_length=1)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    status = models.CharField(choices=Status.choices, default='TODO', max_length=4)
    initiator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='Initiator')
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='Assignee')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Comment(models.Model):

    label = models.CharField(max_length=128)
    content = models.TextField(max_length=8192, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.label
