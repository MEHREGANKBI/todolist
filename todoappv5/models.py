from django.db import models
from django.core import validators
from django.contrib.auth import get_user_model


class Tag(models.Model):
    tag = models.CharField(null = False, blank = False, unique = True, max_length = 16, validators = [
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

    Tag = models.ForeignKey(Tag, models.SET_NULL, null = True, blank = True) # creates Tag and Tag_id orm fields.
    User = models.ForeignKey(get_user_model(), models.CASCADE, null = False, blank = False)