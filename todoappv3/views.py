from django.shortcuts import get_object_or_404
from rest_framework import status
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
            response_dict['message'] = serialized_data.errors # type: ignore
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
        
        except Http404:
            response_dict['result'] = 'ERROR!'
            response_dict['message'] = 'Object with the given id was not found!'
            response_status = status.HTTP_404_NOT_FOUND


        return JsonResponse(response_dict, safe= False, status = response_status)
        

    def put(self, request):
        response_status = None

        deserialized_data = PUTTodolistSerializer(data= request.data)

        if deserialized_data.is_valid():
            # since both id and done_status are validated, we won't face errors in the 3 following lines.
            update_obj = Todolist.objects.get(id=deserialized_data.validated_data['id']) # type: ignore
            update_obj.done_status = deserialized_data.validated_data['done_status'] # type: ignore
            update_obj.save()
            response_dict['result'] = 'SUCCESS!'
            response_dict['message'] = 'Your update request was completed without errors.'
            response_status = status.HTTP_200_OK

        else:
            response_dict['result'] = 'ERROR!'
            response_dict['message'] = deserialized_data.errors # type: ignore
            response_status = status.HTTP_400_BAD_REQUEST
        
        return JsonResponse(response_dict, safe= False, status= response_status)
