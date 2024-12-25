from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from tasks.models import Task
from tasks.serializers import TaskSerializer, ProgresOverviewSerializer
from tasks.utils import get_daily_progress


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["date", "is_completed"]

    def get_queryset(self):
        return super().get_queryset().filter(project__user=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    lookup_field = "slug"

    def get_queryset(self):
        return super().get_queryset().filter(project__user=self.request.user)


class DailyProgressView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, date):
        progress = get_daily_progress(request.user, date)
        serializer = ProgresOverviewSerializer(progress)
        return Response(serializer.data)
