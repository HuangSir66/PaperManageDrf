"""PaperManageDRF URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path

from django.urls import path, re_path
from api import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("api/student",views.StudentView)
router.register('api/teacher',views.TeacherView)
router.register('api/topic',views.TopicView)
# router.register('api/topiclist',views.TopicListView)
urlpatterns = [
    # path('api/student/', views.StudentView.as_view()),
    # re_path('api/student/(?P<pk>\d+)', views.StudentView.as_view()),
    # path("api/student/", views.StudentView.as_view({
    #     "get": "list",
    #     "post": "create"
    # })),
    # re_path("api/student/(?P<pk>\d+)$", views.StudentView.as_view({
    #     "get": "retrieve",
    #     "put": "update",
    #     "delete": "delete",
    # })),
    # path('api/teacher/', views.TeacherView.as_view()),
    # re_path('api/teacher/(?P<pk>\d+)', views.TeacherDetailView.as_view()),
    path('api/login/', views.LoginView.as_view()),
    path('api/check-teacher/',views.CheckTeacherExistsAPIView.as_view())
]
urlpatterns += router.urls