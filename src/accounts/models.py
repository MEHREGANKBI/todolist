from django.db import models

class TokenBlockList(models):
    # Intentionally avoiding the unique constraint. It's unlikely for duplicate records to be made
    # and if they are made, we don't care as long as there aren't too many of them.
    # However, if we set the unique constraint, it needs to check the new token against every single
    # time a token is added i.e almost everytime someone logs out. Yikes. 
    token = models.CharField(max_length = 8192, null = False, required = True)
