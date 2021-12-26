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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api import views


router = routers.SimpleRouter()
router.register('projects', views.ProjectViewset, basename='projects')
router.register('signup', views.SignupView, basename='signup')

project_rooter = routers.NestedSimpleRouter(router, 'projects', lookup='project')
project_rooter.register('issues', views.IssueViewset, basename='issues')
project_rooter.register('users', views.ContributorViewSet, basename='users')

issue_router = routers.NestedSimpleRouter(project_rooter, 'issues', lookup='issue')
issue_router.register('comments', views.CommentViewset, basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api/', include(project_rooter.urls)),
    path('api/', include(issue_router.urls))
]
