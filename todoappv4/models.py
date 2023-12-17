from django.db import models
from django.core import validators


# Create your models here.
class User(models.Model):
    username = models.CharField(null = False, blank = False, unique = True, max_length = 12,validators = [
        validators.MinLengthValidator(4, message='Username must be at least 4 characters.'),
        validators.MaxLengthValidator(12, message='Username must be less than 12 characters.'),
        ])
    password = models.CharField(null = False, blank = False, max_length = 256)



class Tag(models.Model):
    

    tag = models.CharField(null = False, blank = False, max_length = 16, validators = [
        validators.MinLengthValidator(2, message='tag name must be at least 2 characters.'),
        validators.MaxLengthValidator(16, message='tag name must be less than 12 characters.'), 
        ])
    

class Task(models.Model):
    task = models.CharField(null = False, blank = False, max_length = 128, validators= [
        validators.MinLengthValidator(4, message= 'task description must be at least 4 characters.'),
        validators.MaxLengthValidator(128, message= 'task description must be less than 128 charatacters.')
    ])

    is_complete = models.BooleanField(null = False, blank = False)

    created_at = models.DateTimeField(auto_now_add = True)
    modified_at = models.DateTimeField(auto_now = True)
    deadline_at = models.DateTimeField(null = False, blank = False)

    Tag_id = models.ForeignKey(Tag, models.SET_NULL, null = True, blank = True)
    User_id = models.ForeignKey(User, models.CASCADE, null = False, blank = False)