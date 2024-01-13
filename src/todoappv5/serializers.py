from rest_framework import serializers
from datetime import datetime, timezone


from .validators import *
from .models import *
from .view_helpers import *


    
class TaskGETSerializer(serializers.ModelSerializer):
    Tag = serializers.ReadOnlyField(source = 'Tag.tag' ,allow_null = True)
    class Meta:
        model = Task
        fields = ['id', 'task', 'is_complete', 'deadline_at', 'Tag']
    

class POSTSerializer(serializers.Serializer):
    tag = serializers.CharField(required = False, allow_null = True, allow_blank = True, max_length=16, min_length=2)

    task = serializers.CharField(required = True, allow_null = False, allow_blank = False, max_length = 128, min_length =4)
    is_complete = serializers.BooleanField(required= True, allow_null= False)
    deadline_at = serializers.IntegerField(required = True, allow_null = False, min_value = 0)

    def get_tag_or_create_if_not_exists(self,tag):
        if tag_exists(tag):
            tag_obj = Tag.objects.get(tag= tag)
        else:
            tag_obj = Tag(tag = tag)
            tag_obj.save()

        return tag_obj


    def save(self, user_obj):
        validated_data = self.validated_data
        user_tag = validated_data.get('tag', None) 
        validated_data['deadline_at'] = datetime.fromtimestamp(validated_data['deadline_at'], tz= timezone.utc) 

        if user_tag == None or user_tag == '':
            task_obj = Task(task = validated_data['task'], is_complete = validated_data['is_complete'], 
                            deadline_at = validated_data['deadline_at'], User = user_obj) 
            task_obj.save()
        
        else:
            # user has entered a tag that is non-empty. so we check if we need to add the tag to the tag table or not.
            tag_obj = self.get_tag_or_create_if_not_exists(validated_data['tag']) 

            task_obj = Task(task = validated_data['task'], is_complete = validated_data['is_complete'], 
                            deadline_at = validated_data['deadline_at'], User = user_obj, Tag= tag_obj) 
            task_obj.save()
            
        return None
    
    


class PUTTaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required = True, min_value = 0, allow_null = False, 
                                  validators = [task_exists_validator,])
    
    def save(self):
        validated_data = self.validated_data
        task_obj = Task.objects.get(id = validated_data['id']) 
        task_obj.is_complete = validated_data['is_complete'] 
        task_obj.save()
        return None

    class Meta:
        model = Task
        fields = ['id', 'is_complete']
    


class TaskQueryParamsSerializer(serializers.Serializer):
    # Even though this serializer won't read from or write to the Tag model, the tag field must meet the constraints
    # of this field. so instead of defining a new charfield, we refer to the model field for validation.
    tag = serializers.ListField(child= serializers.ModelField(model_field= Tag().__meta.get_field('tag')), required= False)
    complete = serializers.BooleanField(required= False)