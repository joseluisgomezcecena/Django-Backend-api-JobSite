from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.getAllJobs, name="jobs"),
    path('jobs/<str:pk>/', views.getJob, name="job"),
    path('jobs/new/', views.createJob, name="create-job"),
    path('jobs/update/<str:pk>/', views.updateJob, name="update-job"),
    path('jobs/delete/<str:pk>/', views.deleteJob, name="delete-job"),

    path('jobs/apply/<str:pk>/', views.applyToJob, name="apply-job"),
    path('me/jobs/applied', views.getAppliedJobs, name="applied-jobs"),
    path('jobs/check/<str:pk>/', views.isApplied, name="is-applied"),
    path('me/jobs/posted', views.getCurrentUserPostedJobs, name="posted-jobs"),
    path('jobs/candidates/<str:pk>/', views.getCandidatesAppliedToJobs, name="candidates-applied"),

    path('stats/<str:topic>/', views.getTopicStats, name="stats"),
]
