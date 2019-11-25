import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '3$zc7zn#v==*r2ukiezqv39g2im4zf!2%53f+h0rga&*=&(7l5'


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'easyturk',
    'import_export',
]


TEMPLATES = [
    {
       'BACKEND': 'django.template.backends.jinja2.Jinja2',
       'DIRS': [os.path.join(BASE_DIR, 'templates')],
       'APP_DIRS': True,
       'OPTIONS': {
         'environment': 'templates.jinja2.environment'
       },
     },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]