from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .validators import *
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username' , 'password' ]

class UserGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username' ]

class TagGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag']

    
class TaskGETSerializer(serializers.ModelSerializer):
    Tag_id = TagGETSerializer()
    User_id = UserGETSerializer()
    class Meta:
        model = Task
        fields = ['id', 'task', 'is_complete', 'deadline_at', 'Tag_id', 'User_id']
    

class TaskPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['task', 'is_complete', 'deadline_']

class POSTSerializer(serializers.Serializer):
    Tag_id = TagGETSerializer()
    User_id = UserGETSerializer()

    task = TaskPOSTSerializer()
    is_complete = TaskPOSTSerializer()
    deadline_at = TaskPOSTSerializer()



# class PUTTodolistSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(required = True, min_value = 0,
#                                    validators = [todolist_id_exists_validator])
#     class Meta:
#         model = Todolist
#         fields = ['id','done_status']


# class DELETETodolistSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(required = True, min_value = 0,
#                                    validators = [todolist_id_exists_validator])
#     class Meta:
#         model = Todolist
#         fields = ['id']