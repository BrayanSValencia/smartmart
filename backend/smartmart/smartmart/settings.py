
from pathlib import Path
from decouple import config
from datetime import timedelta
import json
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default=None)

DEBUG = config('DEBUG', default=None)

AUTH_USER_MODEL = config('AUTH_USER_MODEL', default=None)

ROOT_URLCONF =  config('ROOT_URLCONF', default=None)

WSGI_APPLICATION = config('WSGI_APPLICATION', default=None)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "business_logic",
    "integrations",
    "rest_framework",
    'rest_framework_simplejwt.token_blacklist', 
    'corsheaders'

]

MIDDLEWARE = [
    #'business_logic.views.RestrictAdmin.RestrictAdminByIPMiddleware',
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ALLOWED_HOSTS = json.loads(config("ALLOWED_HOSTS"))

CORS_ALLOWED_ORIGINS = json.loads(config('CORS_ALLOWED_ORIGINS',default=None))

TEMPLATES = [
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

#REST_FRAMEWORK = {
   # 'DEFAULT_AUTHENTICATION_CLASSES': (
  #      'rest_framework_simplejwt.authentication.JWTAuthentication',
 #   ),
#}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'business_logic.models.JWTWithAccessBlacklistAuthentication.JWTWithAccessBlacklistAuthentication',
    ],
      'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=config('ACCESS_TOKEN_LIFETIME',cast=int, default=None)),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=config('REFRESH_TOKEN_LIFETIME',cast=int, default=None)),
    'ROTATE_REFRESH_TOKENS': config('ROTATE_REFRESH_TOKENS',cast=bool, default=None),
    'BLACKLIST_AFTER_ROTATION': config('BLACKLIST_AFTER_ROTATION',cast=bool, default=None),
    'UPDATE_LAST_LOGIN': config('UPDATE_LAST_LOGIN',cast=bool, default=None),
}
#REST_FRAMEWORK = {
 #   'DEFAULT_AUTHENTICATION_CLASSES': [
  #      'knox.auth.TokenAuthentication',
   # ]
#}

#REST_KNOX = {
 #   'TOKEN_TTL': timedelta(minutes=config('TOKEN_TTL',cast=int, default=None)), 
    
#}


DATABASES = {
    'default': {
        'ENGINE': config('ENGINE', default=None),
        'NAME': config('NAME', default=None),
        'USER': config('USER', default=None),
        'PASSWORD': config('PASSWORD', default=None),
        'HOST': config('HOST', default=None),  
        'PORT': config('PORT', default=None),  
    }
}
#SMTP Credentials
EMAIL_BACKEND = config('EMAIL_BACKEND', default=None)
EMAIL_HOST = config('EMAIL_HOST', default=None)
EMAIL_PORT = config('EMAIL_PORT', default=None)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=None)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default=None)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default=None)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default=None)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
 
]

# Internationalization

LANGUAGE_CODE = config('LANGUAGE_CODE', default=None)

TIME_ZONE = config('TIME_ZONE', default=None)

USE_I18N = config('USE_I18N', default=None)

USE_TZ = config('USE_TZ', default=None)


STATIC_URL = '/static/'

#Default primary key
DEFAULT_AUTO_FIELD = config('DEFAULT_AUTO_FIELD', default=None)


