from django.shortcuts import render
from todoappv2.models import Todolist
#from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
#from django.views import View
from rest_framework.views import APIView
from .serializers import TodolistSerializer
class TodolistCRUDView(APIView):

    def get(self, request):
        ret_val = { "message" : "Your GET request was received" , 
                    "request.query_params" : request.query_params.__str__() ,
                    "request.data" : request.data.__str__(),
                    "request.POST" : request.POST.__str__(),
                    "reuqest.GET" : request.GET.__str__(),
                    "dir(request)" : dir(request).__str__(),
                    }
        return Response(ret_val , status = status.HTTP_200_OK)

    def post(self, request):
        serializer = TodolistSerializer(data = request.data)
        ret_val  = { "message" : "data deserialization was successful", }
        if not serializer.is_valid():
            ret_val = serializer.errors
            return Response(ret_val , status = status.HTTP_400_BAD_REQUEST)
        Todolist.objects.create(**serializer.validated_data)
        return Response(ret_val, status = status.HTTP_200_OK)
    def delete(self, request):
        ret_val = { "message" : "Your DELETE request was received" , }
        return Response(ret_val , status = status.HTTP_200_OK)

    def put(self, request):
        ret_val = { "message" : "Your PUT request was received" , }
        return Response(ret_val , status = status.HTTP_200_OK)
