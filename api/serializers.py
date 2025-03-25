from rest_framework import serializers
from .models import Task, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile']

class TaskSerializer(serializers.ModelSerializer):
    assigned_users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True,required=False)

    class Meta:
        model = Task
        fields = '__all__'