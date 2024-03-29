from rest_framework.views import APIView
from rest_framework import status 
from django.http import JsonResponse
from rest_framework.exceptions import ParseError, PermissionDenied
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import UserCreationSerializer, TokenBlockListSerializer, RefreshTokenSerializer
from response_factory.default_responses import make_success_response



class SignupView(APIView):

    def post(self,request):

        deserialized_data = UserCreationSerializer(data= request.data)

        if deserialized_data.is_valid():
            deserialized_data.save()

            response_dict, response_status = make_success_response(result='Your account was created. You can sign in now.')

        else:
            raise ParseError(deserialized_data.errors.__str__())

        return JsonResponse(response_dict, safe= False, status = response_status)
    



class LogOutView(APIView):

    def post(self,request):
        deserialized_data = TokenBlockListSerializer(data= request.data)

        if deserialized_data.is_valid():
            deserialized_data.save()
            response_dict, response_status = make_success_response(result=deserialized_data.validated_data)
        
        else:
            raise ParseError(deserialized_data.errors.__str__())
        
        
        return JsonResponse(response_dict, safe= False, status= response_status)
    



class RefreshTokenWrapper(TokenRefreshView):
    def post(self, request):
        deserialized_refresh_token = RefreshTokenSerializer(data= request.data)

        # This serializer validates both the parsing errors and blocklisting errors.
        if deserialized_refresh_token.is_valid():
            refresh_view_return =  super().post(request=request)
            response_dict, response_status = make_success_response(result= refresh_view_return.data)
        else:
            raise PermissionDenied(deserialized_refresh_token.errors.__str__())
        
        return JsonResponse(response_dict, safe= False, status = response_status)
                
            