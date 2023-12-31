from django.shortcuts import get_object_or_404
from rest_framework import status
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from redis import Redis
from os import getenv

from .serializers import *
from .responses import response_dict
from .view_helpers import *


class TaskView(APIView):
    permission_classes = [IsAuthenticated]

    def blocklist_check_decorator(func):
        def blocklist_wrapper(self, request,*args, **kwargs):
            redis_obj = Redis(host=getenv('DJANGO_REDIS_HOST'), port= 6379, decode_responses= True)
            if redis_obj.exists(request.auth.__str__()):
                raise Http404
            else:
                return func(self,request,*args,**kwargs)
        
        return blocklist_wrapper


    def get_user_tasks(self,username, type_param):
        user_obj = get_user_model().objects.get(username = username)
        user_queryset = Task.objects.filter(User = user_obj).select_related('Tag', 'User')

        if type_param == 'ALL':
            pass
        elif type_param == 'DONE':
            user_queryset = user_queryset.filter(is_complete = True)
        elif type_param == 'UNDONE':
            user_queryset = user_queryset.filter(is_complete = False)

        # now we will check whether or not after the filtering process, we have any data left to send to the client. 
        if user_queryset.exists():
            serilized_user_data = TaskGETSerializer(user_queryset, many = True)
            response_result = serilized_user_data.data
            response_status = status.HTTP_200_OK
            response_message = 'SUCCESS...'
        else:
            response_status = status.HTTP_404_NOT_FOUND
            response_message = 'ERROR...'
            response_result = 'You currently don\'t have any tasks.'

        return response_message, response_result, response_status

    @blocklist_check_decorator
    def get(self, request, type_param):
        type_param = type_param.strip().upper()
        valid_type_params = ['ALL', 'DONE', 'UNDONE']
        response_status = None
        username = request.user.username

        if type_param in valid_type_params:
            response_dict['message'], response_dict['result'], response_status = self.get_user_tasks(username,type_param) # type: ignore
        else:
            response_dict['message'] = 'ERROR...'
            response_dict['result'] = 'Invalid filter.'
            response_status = status.HTTP_400_BAD_REQUEST

        return JsonResponse(response_dict, safe= False, status= response_status)


    
    @blocklist_check_decorator
    def post(self, request):
        response_status = None
        user_obj = request.user
        # If the json is not valid, it'll send an automatic response, the pattern of which is not the same as my responses. 
        deserialized_data = POSTSerializer(data= request.data)

        if deserialized_data.is_valid():
            deserialized_data.save(user_obj= user_obj)
            response_dict['message'] =  'SUCCESS!'
            response_dict['result'] = 'Your task was successfully created.'
            response_status = status.HTTP_200_OK

        else:
            response_dict['message'] = "ERROR!"
            response_dict['result'] = deserialized_data.errors # type: ignore
            response_status = status.HTTP_400_BAD_REQUEST

        return JsonResponse(response_dict, safe= False, status =response_status)
    
    @blocklist_check_decorator
    def delete(self, request, id_param):
        response_status = None
        user_obj = request.user
        # now we check if the task with the given id is owned by the user whose username is in the token.
        if task_exists(id_param) and user_owns_task(user_obj, id_param):
                task_obj = Task.objects.get(id = id_param)
                task_obj.delete()
                response_status = status.HTTP_200_OK
                response_dict['message'] = 'SUCCESS...'
                response_dict['result'] = 'The task was successfully removed.'
        else:
                response_status = status.HTTP_404_NOT_FOUND
                response_dict['message'] = 'ERROR...'
                response_dict['result'] = 'Task not found.'
        

        return JsonResponse(response_dict, safe= False, status= response_status)
                
    @blocklist_check_decorator
    def put(self, request):
        response_status = None
        user_obj = request.user
        deserialized_data = PUTTaskSerializer(data= request.data)

        #this serializer will check if the task exists too so we don't have to check seperately.
        if deserialized_data.is_valid() and user_owns_task(user_obj, deserialized_data.validated_data['id']): # type: ignore
            deserialized_data.save()
            response_status = status.HTTP_200_OK
            response_dict['message'] = 'SUCCESS...'
            response_dict['result'] = 'The status of the task was updated successfully.' 

        else:
            response_status = status.HTTP_404_NOT_FOUND
            response_dict['message'] = 'ERROR...'
            response_dict['result'] = 'Task not found.' 
                

        return JsonResponse(response_dict, safe= False, status= response_status)




class SignupView(APIView):


    def signup(self, request):
        deserialized_data = UserCreationSerializer(data= request.data)

        if deserialized_data.is_valid():
            deserialized_data.save()

            response_status = status.HTTP_200_OK
            response_message = 'SUCCESS...'
            response_result = 'Your account was created. You can sign in now.'

        else:
            response_status = status.HTTP_400_BAD_REQUEST
            response_message = 'ERROR...'
            response_result = deserialized_data.errors

        return response_message, response_result, response_status




    def post(self,request):
        response_status = None
        
        response_dict['message'], response_dict['result'], response_status = self.signup(request) # type: ignore 

        return JsonResponse(response_dict, safe= False, status = response_status)
