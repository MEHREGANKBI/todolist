#from django.shortcuts import render
from django.shortcuts import get_object_or_404
#from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
#from django.views import View
from django.http import Http404, JsonResponse
from rest_framework.views import APIView

from .models import Todolist
from .serializers import *
from .responses import response_dict
from .view_helpers import get_todolist_data

class TodolistCRUDView(APIView):

    def get(self, request, type_param):
        type_param = type_param.strip().upper()
        response_status = None

        response_dict['result'], response_dict['message'], response_status = get_todolist_data(type_param) # type: ignore
        
        return JsonResponse(response_dict, safe= False, status= response_status) 

    

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
            ret_val = {'usage_error' : 'Both keys id and done_status are mandatory.'}
            return Response(ret_val, status= status.HTTP_400_BAD_REQUEST)
        
        except ValueError:
            ret_val = {'usage_error' : 'Invalid value for id.',
                       'value_received' : request.data['id'].__str__()}
            return Response(ret_val, status= status.HTTP_400_BAD_REQUEST)
        
        # This will allow integer 0 or 1 to be passed as values for the done_status key.
        done_status_valid_values = [False, True, "true", "false"]
        if received_done_status not in done_status_valid_values:
            ret_val = {"usage_error" : "Invalid value for <done_status>. Must be either JSON's true OR false"}
            return Response(ret_val, status= status.HTTP_400_BAD_REQUEST)
        
        try:
            obj_of_id = get_object_or_404(Todolist, id = received_id)
            if received_done_status.__str__().lower() == 'true':
                upate_done_status = True
            else:
                upate_done_status = False
            obj_of_id.done_status = upate_done_status
            obj_of_id.save()
        except Http404:
            ret_val = {'error404' : "The <id> you asked for was not found."}
            
    
        ret_val = { "message" : "Your PUT request was received with no ERRORS" , 
                   "id": received_id,
                   "done_status" : received_done_status.__str__()}
        return Response(ret_val , status = status.HTTP_200_OK)