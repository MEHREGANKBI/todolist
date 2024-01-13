from django.db import models
from django.core import validators
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet


class Tag(models.Model):
    tag = models.CharField(null = False, blank = False, unique = True, max_length = 16, validators = [
        validators.MinLengthValidator(2, message='tag name must be at least 2 characters.'),
        validators.MaxLengthValidator(16, message='tag name must be less than 12 characters.'), 
        ])
    
    def __str__(self):
        return f'tag={self.tag},id={self.id}' # type: ignore
    


class CustomTaskModelManager(models.Manager):
    def get_queryset(self, is_complete = None, tag= None, user = None) -> QuerySet:
        # Parameters of this function are either lists or None.

        query_set = super().get_queryset()
        # Here comes the chained filtering
        query_set = self.__filter_by_tag(tag= tag, query_set = query_set)

        query_set = self.__filter_by_user(user= user, query_set = query_set)

        query_set = self.__filter_by_completeness(is_complete= is_complete, query_set = query_set)

        return query_set

    
    
    def __filter_by_tag(self, tag, query_set):
        return query_set


    def __filter_by_user(self,user, query_set):
        return query_set

    def __filter_by_completeness(self,is_complete, query_set):
        return query_set
    

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


    objects = CustomTaskModelManager()


    def __str__(self):
        return f'task={self.task}, is_complete={self.is_complete},\ndeadline_at={self.deadline_at}, User={self.User}, Tag={self.Tag}' # type: ignore
    



