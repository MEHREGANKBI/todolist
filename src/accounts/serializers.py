from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
import jwt
from os import getenv
from django.contrib.auth.password_validation import (UserAttributeSimilarityValidator,
                                                     MinimumLengthValidator,
                                                     CommonPasswordValidator,
                                                     NumericPasswordValidator,
                                                     validate_password,)


from .secrets import salt
from .models import *
from todolist.settings import SIMPLE_JWT, REDIS_CONNECTION

class UserCreationSerializer(serializers.ModelSerializer):

    def validate(self, data):
        # the function below will automatically raise validationerror so no need to do it ourselves.
        pass_is_valid = validate_password(password= data['password'], user= data['username'], 
                                          password_validators= [UserAttributeSimilarityValidator(), MinimumLengthValidator(),
                                                     CommonPasswordValidator(),NumericPasswordValidator()]) 

        return data
    



    def save(self):
        validated_data = self.validated_data
        user_obj = get_user_model()()
        user_obj.email = validated_data['email'] 
        user_obj.username = validated_data['username'] 
        user_obj.first_name = validated_data['first_name'] 
        user_obj.last_name = validated_data['last_name'] 
        user_obj.password = make_password(password= validated_data['password'], salt= salt) 
        user_obj.save()


    class Meta:
        model = get_user_model()
        fields = [ 'username' , 'password', 'email' , 'first_name' , 'last_name' ]




class TokenBlockListSerializer(serializers.ModelSerializer):
    access_token = serializers.CharField(write_only = True, required = True, max_length = 8192, min_length = 64)

    # Maybe it's ok if not both of the tokens are valid. for example, a valid refresh and invalid access token.
    def validate(self,data):
        access_is_valid = self.token_is_valid(jwt_token= data['access_token'])
        refresh_is_valid = self.token_is_valid(jwt_token= data['refresh_token'])

        if (not refresh_is_valid) or (not access_is_valid):
            raise serializers.ValidationError('Invalid tokens received.') 
        else:
            return data


    def token_is_valid(self,jwt_token):
        try:
            jwt.decode(jwt= jwt_token, key= SIMPLE_JWT['SIGNING_KEY'], algorithms= ['HS256',])
        except:
            return False
        else:
            return True
        

    
    def save(self):
        # So as not to fill the cache, access token keys are given a max life time of 600 seconds. more than this,
        # the access token would be expired anyway. So why keep in the cache perpetually. 
        REDIS_CONNECTION.setex(self.validated_data['access_token'] , 600,1)

        TokenBlockList.objects.create(refresh_token = self.validated_data['refresh_token'])

        return True


    class Meta:
        model = TokenBlockList
        fields = ['refresh_token', 'access_token']



class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length = 8192, min_length = 64, required = True)

    def validate(self, data):
        # Here. we'll check if the refresh token that we received exists in the blocklist table.
        token_exists_in_blocklist = TokenBlockList.objects.filter(refresh_token= data['refresh']).exists()

        if token_exists_in_blocklist:
            raise serializers.ValidationError('Your refresh token is not allowed to make access tokens.')
        else:
            return data
        
