from os import getenv

salt = getenv('DJANGO_SECRETS_SALT') 

jwt_secret = getenv('DJANGO_SECRETS_JWT')