from django.db import models
from django.core.validators import MinLengthValidator

class TokenBlockList(models.Model):
    # Intentionally avoiding the unique constraint. It's unlikely for duplicate records to be made
    # and if they are made, we don't care as long as there aren't too many of them.
    # However, if we set the unique constraint, it needs to check the new token against every single
    # time a token is added i.e almost everytime someone logs out. Yikes. 
    refresh_token = models.CharField(max_length = 8192, null = False, blank = False, validators = [MinLengthValidator(64),])
