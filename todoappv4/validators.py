from django.shortcuts import get_object_or_404
from rest_framework import serializers

def todolist_id_exists_validator(id):
    try:
        get_object_or_404(Todolist, id = id)
    except:
        raise serializers.ValidationError('The id is not valid.')