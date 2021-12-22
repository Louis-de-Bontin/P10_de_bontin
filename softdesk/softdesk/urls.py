"""softdesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework_nested import routers

from api.views import ProjectViewset, IssueViewset, CommentViewset


router = routers.SimpleRouter()
router.register('project', ProjectViewset, basename='project')

project_rooter = routers.NestedSimpleRouter(router, 'project', lookup='project')
project_rooter.register('issue', IssueViewset, basename='issue')

issue_router = routers.NestedSimpleRouter(project_rooter, 'issue', lookup='issue')
issue_router.register('comment', CommentViewset, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/', include(project_rooter.urls)),
    path('api/', include(issue_router.urls))
]
