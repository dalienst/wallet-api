from django.urls import path

from projects.views import ProjectListCreateView, ProjectDetailView

urlpatterns = [
    path("", ProjectListCreateView.as_view(), name="project-list-create"),
    path("<str:slug>/", ProjectDetailView.as_view(), name="project-detail"),
]
