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

        #To return Only
        # tasks = Task.objects.filter(assigned_users__id=user_id).values('name', 'description')
        # return Response(tasks)
        
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
        # return Response(self.get_serializer(task).data)
        return Response({"message": "Task assigned to users successfully."}, status=status.HTTP_200_OK)

    # def create(self, request, *args, **kwargs):
    #     user_ids = request.data.pop("assigned_users", [])
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     task = serializer.save()

    #     if user_ids:
    #         users = User.objects.filter(id__in=user_ids)
    #         task.assigned_users.set(users)

    #     task.save()
    #     return Response(self.get_serializer(task).data, status=status.HTTP_201_CREATED)