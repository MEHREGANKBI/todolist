from rest_framework import serializers
from .models import Todolist


class TodolistSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Todolist
        fields = [ 'id' , 'activity_description' , 'done_status']
        read_only_fields = ['id']



class GETTodolistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todolist
        fields = ['id', 'activity_description']
        read_only_fields = ['id', 'activity_description']

        