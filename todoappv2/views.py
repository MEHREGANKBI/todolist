#from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Todolist
#from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
#from django.views import View
from django.http import Http404
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
        ret_val = None
        received_data = request.data
        # TODO: Try to replace the try except block with a more efficient method.
        try:
            temp = received_data['done_status']
        except KeyError:
            ret_val = { "usage_error" : 'The key "done_status" must exist!'}
            return Response(ret_val, status= status.HTTP_400_BAD_REQUEST)
        
        # This will allow integer 0 or 1 to be passed as values for the done_status key.
        done_status_valid_values = [False, True, "true", "false"]
        if received_data['done_status'] not in done_status_valid_values:
            ret_val = {"usage_error" : "Invalid value!The key \"done_status\" must be either JSON true OR false"}
            return Response(ret_val, status= status.HTTP_400_BAD_REQUEST)
        
        serialized_data = TodolistSerializer(data=request.data)
        if not serialized_data.is_valid():
            ret_val = {"usage_error" : "The following errors were encountered while parsing your data.",
                       "errors" : serialized_data.errors}
            return Response(ret_val, status= status.HTTP_400_BAD_REQUEST)
        
        serialized_data.save()
        
        ret_val = { "success" : "The following data got past all validations.",
                   "validated_data" : serialized_data.validated_data}
        return Response(ret_val, status= status.HTTP_200_OK)
    

    def delete(self, request):
        ret_val = None
        received_data = request.data
        try:
            received_id = received_data['id']
            received_id = int(received_id)
            obj_of_id = get_object_or_404(Todolist, id = received_id)
            obj_of_id.delete()
        except(KeyError):
            ret_val = { "usage_error" : "key <id> is mandatory."}
            return Response(ret_val, status= status.HTTP_400_BAD_REQUEST)
        except(ValueError):
            ret_val = {"usage_error" : "invalid value for key <id>",
                       "value_received" : received_data['id'].__str__()}
            return Response(ret_val, status= status.HTTP_400_BAD_REQUEST)
        except(Http404):
            ret_val = { "error404": "The id received is not found"}
            return Response(ret_val, status= status.HTTP_404_NOT_FOUND)


        

        ret_val = { "message" : "Your DELETE request was completed with no ERRORS" ,
                   "id" : received_id.__str__() }
        return Response(ret_val , status = status.HTTP_200_OK)

    def put(self, request):
        ret_val = None
        try:
            received_id = request.data['id']
            received_id = int(received_id)
            received_done_status = request.data['done_status']
        except KeyError:

        ret_val = { "message" : "Your PUT request was received" , }
        return Response(ret_val , status = status.HTTP_200_OK)
