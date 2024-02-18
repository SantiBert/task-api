from .base_settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['http://sbertero.pythonanywhere.com/']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sbertero$default',
        'USER': 'sbertero',
        'PASSWORD': 'Dearrosamery1',
        'HOST': 'sbertero.mysql.pythonanywhere-services.com',
    }
}