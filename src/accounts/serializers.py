from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import (UserAttributeSimilarityValidator,
                                                     MinimumLengthValidator,
                                                     CommonPasswordValidator,
                                                     NumericPasswordValidator,
                                                     validate_password,)


from .secrets import salt
from .models import *

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

    class Meta:
        model = TokenBlockList
        fields = ['refresh_token', 'access_token']
