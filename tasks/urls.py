from django.urls import path

from tasks.views import TaskListCreateView, TaskDetailView, DailyProgressView

urlpatterns = [
    path("", TaskListCreateView.as_view(), name="task-list-create"),
    path("<str:slug>/", TaskDetailView.as_view(), name="task-detail"),
    path("progress/", DailyProgressView.as_view(), name="task-progress"),
]
