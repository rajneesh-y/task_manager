from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task, User
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def tasks_by_user(self, request, user_id=None):
        
        tasks = Task.objects.filter(assigned_users__id=user_id)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'], url_path='assign')
    def assign_to_user(self, request, pk=None):
        task = self.get_object()
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        task.assigned_users.add(user)  # ManyToMany
        task.save()
        return Response({"message": "Task assigned to users successfully."}, status=status.HTTP_200_OK)