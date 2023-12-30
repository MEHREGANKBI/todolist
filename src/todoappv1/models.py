from django.db import models

# Create your models here.
class Todolist(models.Model):
    activity_description = models.CharField(max_length=200)
    done_status = models.BooleanField()


