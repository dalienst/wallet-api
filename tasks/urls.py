from django.urls import path

from tasks.views import TaskListCreateView, TaskDetailView

urlpatterns = [
    path("", TaskListCreateView.as_view(), name="task-list-create"),
    path("<str:slug>/", TaskDetailView.as_view(), name="task-detail"),
]
