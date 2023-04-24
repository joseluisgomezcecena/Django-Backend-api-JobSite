from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.getAllJobs, name="jobs"),
    path('jobs/<str:pk>/', views.getJob, name="job"),
    path('jobs/new/', views.createJob, name="create-job"),
    path('jobs/update/<str:pk>/', views.updateJob, name="update-job"),
    path('jobs/delete/<str:pk>/', views.deleteJob, name="delete-job"),

    path('stats/<str:topic>/', views.getTopicStats, name="stats"),
]
