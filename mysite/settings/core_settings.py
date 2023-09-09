from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'mysite.herokuapp.com']


AUTH_USER_MODEL='account.UserBase'
LOGIN_URL='account_:login'
#LOGIN_REDIRECT_URL='vendor_:vendor_admin_'
LOGIN_REDIRECT_URL='account_:dashboard'
LOGOUT_REDIRECT_URL='account_:login'

"""
from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = list(default_headers) + [
    'X-Amz-Date',
    'Access-Control-Request-Headers',
    'Access-Control-Allow-Headers',
    'Access-Control-Allow-Origin',
    'XMLHttpRequest',
]

=========================================================
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SAMESITE = 'None'
CORS_ALLOW_CREDENTIALS = True
SameSite = 'None'


CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    'mywebsite.ngrok.io',
    'authorization.proj.io'
)

SESSION_COOKIE_DOMAIN=".proj.com"

==============================================================


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 40
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# CSRF_COOKIE_NAME = "XSRF-TOKEN"

ROOT_URLCONF = 'server.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bigbasket',
        'USER': 'naresh',
        'PASSWORD': 'naresh',
        'HOST': 'localhost'
        # 'PORT': '',
    }
}
============================================================
from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = list(default_headers) + [
    'X-Amz-Date',
    'Access-Control-Request-Headers',
    'Access-Control-Allow-Headers',
    'Access-Control-Allow-Origin',
    'XMLHttpRequest',
]
CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CSRF_USE_SESSIONS = False
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = None

SESSION_COOKIE_HTTPONLY = True 
SESSION_COOKIE_SAMESITE = None

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
=======================================================

header("Set-Cookie: cross-site-cookie=whatever; SameSite=None; Secure");


browser  send django a page request
django request  all Session ID & Session Data from db
django  send browser d page requested Session ID
browser store this in cookie and send back Session ID & Session Data
django match this id with data for  that Session ID in db
django send data back to browser only when page is refressh
set up see
"""
#86400 is equal to 1day before a account session is erased
SESSION_COOKIE_AGE = 86400
CART_SESSION_ID = 'cart'

SUBCRIPTION_TIMEOUT = 3


# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_HOST_USER = 'my sendgrid username'
# EMAIL_HOST_PASSWORD = 'my sendgrid password'
EMAIL_HOST = 'smtp.gmail.net'
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USER_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# if i want django to email me  whenenver there a 500 internal server error
# DEFAULT_EMAIL_FROM = 'interiorstore <noreply@megabright007.com'
# OR 
# DEFAULT_EMAIL_FROM = 'megabright007@gmail.com'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.core',
    'apps.vendor',
    'apps.account',
    'apps.product',
    'apps.cart',
    'apps.chats',
    'apps.order',
    'apps.checkout',
    'apps.communication',
    'rest_framework',
    'crispy_forms',
    'apps.product.templatetags.namify',
    'mptt',
    'channels',
    #'paystack',
]
#PAYSTACK_PUBLIC_KEY = os.environ.get('PAYSTACK_PUBLIC_KEY')
#PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY')

PAYSTACK_PUBLIC_KEY  = os.getenv("PAYSTACK_PUBLIC_KEY")
PAYSTACK_SECRET_KEY  = os.getenv("PAYSTACK_SECRET_KEY")


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

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
                'apps.product.context_processors.menu_categories',
                'apps.cart.context_processors.cart',
                'apps.communication.context_processors.messages_number',
                'apps.checkout.context_processors.get_address',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'
ASGI_APPLICATION = 'mysite.asgi.application'
#ASGI_APPLICATION = 'mysite.routing.application'


REDIS_HOST = "localhost"
REDIS_PORT = 6379


"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mysiteDB',
        'USER': 'postgres',
        "PASSWORD": 'guht9876',
        "HOST": 'localhost',
        "PORT": '5432',
    }
}


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS=[
    BASE_DIR / 'static'
]
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MPTT_ADMIN_LEVEL_INDENT = 20



# cd C:\Users\BRIGHT\PycharmProjects\pythonProject\game
# C:\Users\BRIGHT\PycharmProjects\pythonProject\game\Scripts\activate
#1) cd C:\Users\BRIGHT\PycharmProjects\pythonProject\game\mysite
#2) cd C:\Users\BRIGHT\PycharmProjects\pythonProject\game\travel
#3) cd C:\Users\BRIGHT\PycharmProjects\pythonProject\game\restaurant
#3) cd C:\Users\BRIGHT\PycharmProjects\pythonProject\game\BrightMusic
# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver
# python manage.py createsuperuser
# guht9876 2@2.com admin
# python manage.py makemigrations --check
# django-admin startproject mysite
# django-admin startapp
#{{ i.title | truncatechars:30}}

# password_reset_form
# password_reset_confirm
# orderplaced
# edit_login
# register
# login
# base
# account.views line: 420, 435, 487




"""
https://itzone.com.vn/en/article/django-channels-for-example-updating-the-users-online-real-time-status-online/

https://www.w3schools.com/howto/howto_js_image_magnifier_glass.asp

https://www.codingforentrepreneurs.com/blog/how-to-create-a-custom-django-user-model

203cb4 436ad3 162279   1943a3  405691 1820b4

9eafe5 a1a7f2 1b20a7 2b4897
1:02 delivery choices 
1:26 delivery adress

First name:John
Last name:Doe
Email ID:sb-wa28s8166785@personal.example.com
System Generated Password:IEQb$t9a
Password:Change password
Note: If your system generated password is changed, your new password will not be displayed because of one-way password encryption.
Phone Number:4089429161
Account type:Personal
Account ID:DUHWFVTBS9U9C
Status:Verified
Country:US


First name:bright
Last name:orji
Email ID:megabright007@gmail.com
Password:Change password
Phone Number:4686788567
Account type:Business
Account ID:598T8MUXJPTBN
Status:Unverified
Country:SE
=============================================================
Platform Partner App - 5317773589128768491
Sandbox Business Account:sb-3w3or8166766@business.example.com
client id:AeC1oKpCdxpyVpQPkmJ44tFm49oxb2DSL6CT0LjgItaZY2Zqq0kVXOM-OZlUIL0vUkzJ_RCQzTKipGRU
secret key:EEWzYjbGIv3VbUVW4IQgLT7lw6GGXfWdFC-JKfOh2GVXMe9jPKXePUz2SeB5ttsADSXgNOKto7jkWtL1


Sandbox Business Account:megabright007@gmail.com
client id:ARu-_pPT7to2ublMfXlzrhpsL9Xlye694JATZR3RBYPU3bQbmhqdTpkDvmq9KZleBmP0g5qGRYafWfRq
secret key:EBrknqFpM_6j_XE6JzZdtaG9vo19BCRBbqm6cYoT3hekIN1h9o93Zef2vpnELgJE2eESK3k-U3HuArqk
pip install paypal-checkout-serversdk
"""

"""when user suscribes
when user suscription finishes 
when user has message 
when user likes
when user comment

all admin activity 






version: '3.8'
services:
  cache:
    image: redis:6.2-alpine
    restart: always
    ports:
      - '6379:6379'
    command: redis-server --save 20 1 --loglevel warning --requirepass eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81
    volumes: 
      - cache:/data
volumes:
  cache:
    driver: local
    
    
    
version: "3.2"
services:

 redis:
    image: "redis:alpine"

    command: redis-server --requirepass sOmE_sEcUrE_pAsS

    ports:
     - "6379:6379"

    volumes:
     - $PWD/redis-data:/var/lib/redis
      - $PWD/redis.conf:/usr/local/etc/redis/redis.conf

    environment:
     - REDIS_REPLICATION_MODE=master

    networks:
      node_net:
        ipv4_address: 172.28.1.4

# networking for the Redis container
networks:
  node_net:
    ipam:
      driver: default
      config:
        - subnet: 172.28.0.0/16
"""
#Test Secret Key = sk_test_8c231ece81620c5dfe92377a418f6165acec884d
#Test Public Key = pk_test_1bd3d130cbb6f84a90e8cdb0e13a82a659ebbedc