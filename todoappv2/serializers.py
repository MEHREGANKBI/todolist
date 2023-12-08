from rest_framework import serializers

class TodolistSerializer(serializers.Serializer):
    activity_description = serializers.CharField(max_length = 200)
    done_status = serializers.BooleanField()


