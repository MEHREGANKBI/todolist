from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
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
        response_status = None

        # If the following json is not valid, it'll send an automatic response, the pattern 
        # of which is out of my control and is different from my unified response pattern.
        # Possible solutions: 
        # 1: validate the json before handing it to the serializer which defeats the purpose of using serializers.
        # 2: use try except on the parsing line which apparently degrades performance.
        serialized_data = TodolistSerializer(data= request.data)

        if serialized_data.is_valid():
            serialized_data.save()
            response_dict['result'] =  'SUCCESS!'
            response_dict['message'] = 'Your composition request was completed without errors!'
            response_status = status.HTTP_200_OK

        else:
            response_dict['result'] = "ERROR!"
            response_dict['message'] = serialized_data.errors
            response_status = status.HTTP_400_BAD_REQUEST

        return JsonResponse(response_dict, safe= False, status =response_status)
    

    def delete(self, request, id_param):
        response_status = None
        
        try:
            deletion_obj = get_object_or_404(Todolist, id = id_param)
            deletion_obj.delete()
            response_dict['result'] = 'SUCCESS!' 
            response_dict['message'] = 'The deletion was completed without errors!' 
            response_status = status.HTTP_200_OK
        
        except:
            response_dict['result'] = 'ERROR!'
            response_dict['message'] = 'Object with the given id was not found!'
            response_status = status.HTTP_404_NOT_FOUND


        return JsonResponse(response_dict, safe= False, status = response_status)
        

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
