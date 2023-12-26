from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from datetime import datetime, timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import (UserAttributeSimilarityValidator,
                                                     MinimumLengthValidator,
                                                     CommonPasswordValidator,
                                                     NumericPasswordValidator,
                                                     validate_password,)

from django.contrib.auth.hashers import make_password


from .validators import *
from .models import *
from .view_helpers import *
from .secrets import salt

class UserCreationSerializer(serializers.ModelSerializer):

    def validate(self, data):
        # the function below will automatically raise validationerror so no need to do it ourselves.
        pass_is_valid = validate_password(password= data['password'], user= data['username'], 
                                          password_validators= [UserAttributeSimilarityValidator(), MinimumLengthValidator(),
                                                     CommonPasswordValidator(),NumericPasswordValidator()]) # type: ignore

        return data
    

    def save(self):
        validated_data = self.validated_data
        user_obj = get_user_model()()
        user_obj.email = validated_data['email'] # type: ignore
        user_obj.username = validated_data['username'] # type: ignore
        user_obj.first_name = validated_data['first_name'] # type: ignore
        user_obj.last_name = validated_data['last_name'] # type: ignore
        user_obj.password = make_password(password= validated_data['password'], salt= salt) # type: ignore
        user_obj.save()


    
    class Meta:
        model = get_user_model()
        fields = [ 'username' , 'password', 'email' , 'first_name' , 'last_name' ]



class UserGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [ 'username' ]

class TagGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag']

    
class TaskGETSerializer(serializers.ModelSerializer):
    #Tag = TagGETSerializer()
    Tag = serializers.ReadOnlyField(source = 'Tag.tag' ,allow_null = True)
    class Meta:
        model = Task
        fields = ['id', 'task', 'is_complete', 'deadline_at', 'Tag']
    

class POSTSerializer(serializers.Serializer):
    tag = serializers.CharField(required = False, allow_null = True, allow_blank = True, max_length=16, min_length=2)

    task = serializers.CharField(required = True, allow_null = False, allow_blank = False, max_length = 128, min_length =4)
    is_complete = serializers.BooleanField(required= True, allow_null= False)
    deadline_at = serializers.IntegerField(required = True, allow_null = False, min_value = 0)

    def save(self, username):
        # user_obj = User.objects.get(username= username)
        validated_data = self.validated_data
        user_tag = validated_data.get('tag', None) # type: ignore
        validated_data['deadline_at'] = datetime.fromtimestamp(validated_data['deadline_at'], tz= timezone.utc) # type: ignore

        if user_tag == None or user_tag == '':
            task_obj = Task(task = validated_data['task'], is_complete = validated_data['is_complete'], # type: ignore
                            deadline_at = validated_data['deadline_at'], User_id = user_obj) # type: ignore
            task_obj.save()
            return "Tagless"
        else:

            # user has entered a tag that is non-empty. so we check if we need to add the tag to the tag table or not.
            if not tag_exists(validated_data['tag']): # type: ignore
                tag_obj = Tag(tag = validated_data['tag']) # type: ignore
                tag_obj.save()
            else:
                tag_obj = Tag.objects.get(tag = validated_data['tag']) # type: ignore

            task_obj = Task(task = validated_data['task'], is_complete = validated_data['is_complete'], # type: ignore
                            deadline_at = validated_data['deadline_at'], User_id = user_obj, Tag_id = tag_obj) # type: ignore
            task_obj.save()
            
        return "Tagful"


class PUTTaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required = True, min_value = 0, allow_null = False, 
                                  validators = [task_exists_validator,])
    
    def save(self):
        validated_data = self.validated_data
        task_obj = Task.objects.get(id = validated_data['id']) # type: ignore
        task_obj.is_complete = validated_data['is_complete'] # type: ignore
        task_obj.save()
        return 'The update process was completed successfully.'

    class Meta:
        model = Task
        fields = ['id', 'is_complete']
    


