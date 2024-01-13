from django.shortcuts import get_object_or_404
from rest_framework import status
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from redis import Redis
from os import getenv
from rest_framework.request import Request
from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework.exceptions import PermissionDenied, ParseError


from .serializers import *
from .view_helpers import *


class TaskView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def blocklist_check_decorator(func):
        def blocklist_wrapper(self, request,*args, **kwargs):
            redis_obj = Redis(host=getenv('DJANGO_REDIS_HOST'), port= 6379, decode_responses= True)
            if redis_obj.exists(request.auth.__str__()):
                raise PermissionDenied('Your client is not allowed to access this service.')
            else:
                return func(self,request,*args,**kwargs)
        
        return blocklist_wrapper


    def get_user_tasks(self,user_obj, type_param):
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
            raise Http404('You currently do not have any tasks.')

        return response_message, response_result, response_status

    @blocklist_check_decorator
    def get(self, request: type[Request], type_param: str) -> JsonResponse:
        '''
        Parameters:
            self: unused.
            request: A DRF request object. user and auth attributes are always used in this function.

        Returns: 
            JsonResponse: Contains the HTTP status of the request, and the response payload.

        Description:
            Given a valid user <Request.user> and type_param, return the tasks of that very user, filtered based on the
            type_param constraints. Otherwise, return an error with its corresponding HTTP status.
        '''
        response_dict = {}
        response_status = None

        deserialized_query_params = TaskQueryParamsSerializer(data= request.query_params)
        if deserialized_query_params.is_valid():
            pass
        
         
        else:
            raise ParseError('Invalid filter.')

        return JsonResponse(response_dict, safe= False, status= response_status)


    
    @blocklist_check_decorator
    def post(self, request):
        response_dict = {}
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
            raise ParseError(deserialized_data.errors.__str__())

        return JsonResponse(response_dict, safe= False, status =response_status)
    
    @blocklist_check_decorator
    def delete(self, request, id_param):
        response_dict = {}
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
                raise Http404('Task not found.')
        

        return JsonResponse(response_dict, safe= False, status= response_status)
                
    @blocklist_check_decorator
    def put(self, request):
        response_dict = {}
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
            raise Http404('Task not found.')
                

        return JsonResponse(response_dict, safe= False, status= response_status)

