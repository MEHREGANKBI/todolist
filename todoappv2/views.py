from django.shortcuts import render
from .models import Todolist
#from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
#from django.views import View
from rest_framework.views import APIView
from .serializers import TodolistSerializer
class TodolistCRUDView(APIView):

    def get(self, request):
        model_objects = None
        serialized_objects = None
        ret_val = None
        retrieval_type = request.query_params.dict().get('type', 0)
        if not retrieval_type:
            ret_val = { "usage_error" : "Required key \"type\" was not found in the request!"}
            return Response(ret_val, status= status.HTTP_400_BAD_REQUEST)
        
        retrieval_type = retrieval_type.strip().upper()
        if retrieval_type == "ALL" :
            serialized_objects = TodolistSerializer(Todolist.objects.all(), many = True)
            ret_val = { "retrieval_type" : "ALL",
                       "payload" : [ item['activity_description'] for item in serialized_objects.data]
            }
        elif retrieval_type == "DONE" :
            serialized_objects = TodolistSerializer(Todolist.objects.filter(done_status = True), many = True)
            ret_val = {"retrieval_type" : "DONE",
                       "payload" : [ item['activity_description'] for item in serialized_objects.data],
            }
        elif retrieval_type == "UNDONE" :
            serialized_objects = TodolistSerializer(Todolist.objects.filter(done_status = False), many = True)
            ret_val = { "retrieval_type" : "UNDONE",
                       "payload" : [ item['activity_description'] for item in serialized_objects.data]
            }
        else :
            ret_val = {"usage_error" : "The value entered for \"type\" is invalid!",
                       "value received" : str(retrieval_type)}
            return Response(ret_val, status= status.HTTP_400_BAD_REQUEST)
             

        return Response(ret_val , status = status.HTTP_200_OK)
    

   def post(self, request):
    #     serializer = TodolistSerializer(data = request.data)
    #     ret_val  = { "message" : "data deserialization was successful", }
    #     if not serializer.is_valid():
    #         ret_val = serializer.errors
    #         return Response(ret_val , status = status.HTTP_400_BAD_REQUEST)
    #     Todolist.objects.create(**serializer.validated_data)
    #     return Response(ret_val, status = status.HTTP_200_OK)

    def delete(self, request):
        ret_val = { "message" : "Your DELETE request was received" , }
        return Response(ret_val , status = status.HTTP_200_OK)

    def put(self, request):
        ret_val = { "message" : "Your PUT request was received" , }
        return Response(ret_val , status = status.HTTP_200_OK)
