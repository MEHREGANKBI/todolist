from rest_framework.views import APIView
from rest_framework import status 
from django.http import JsonResponse
from rest_framework.exceptions import ParseError

from .serializers import UserCreationSerializer



class SignupView(APIView):


    def signup(self, request):
        deserialized_data = UserCreationSerializer(data= request.data)

        if deserialized_data.is_valid():
            deserialized_data.save()

            response_status = status.HTTP_200_OK
            response_message = 'SUCCESS...'
            response_result = 'Your account was created. You can sign in now.'

        else:
            raise ParseError(deserialized_data.errors.__str__())

        return response_message, response_result, response_status




    def post(self,request):
        response_status = None
        response_dict = {}
        
        response_dict['message'], response_dict['result'], response_status = self.signup(request)  

        return JsonResponse(response_dict, safe= False, status = response_status)
    



class LogOutView(APIView):

    def post(self,request):
        pass