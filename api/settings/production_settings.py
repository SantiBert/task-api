from .base_settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['sbertero.pythonanywhere.com']

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000', 
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sbertero$default',
        'USER': 'sbertero',
        'PASSWORD': 'Dearrosamery1',
        'HOST': 'sbertero.mysql.pythonanywhere-services.com',
    }
}