from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .validators import *
from .models import *

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [ 'username' , 'password' ]



# class GETTodolistSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Todolist
#         fields = ['id', 'activity_description']
#         read_only_fields = ['id', 'activity_description']


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