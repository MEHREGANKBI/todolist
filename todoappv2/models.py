from django.db import models

# Create your models here.
class Todolist(models.Model):
    # null=False, blank = False, 
    activity_description = models.CharField(max_length=200, unique = True)
    done_status = models.BooleanField(default = False, null= False)


