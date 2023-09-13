from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = ["127.0.0.1", ".vercel.app", ".now.sh"]
#OR to allow all
ALLOWED_HOSTS = ["*"]

AUTH_USER_MODEL='account.UserBase'
LOGIN_URL='account_:login'
LOGIN_REDIRECT_URL='account_:dashboard'
LOGOUT_REDIRECT_URL='account_:login'

#86400 is equal to 1day before a account session is erased
SESSION_COOKIE_AGE = 86400
CART_SESSION_ID = 'cart'

SUBCRIPTION_TIMEOUT = 3


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USER_TLS = True
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
    # 'rest_framework',
    # 'crispy_forms',
    'apps.product.templatetags.namify',
    'mptt',
    'channels',
]

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

ROOT_URLCONF = 'NgStore2.urls'

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

WSGI_APPLICATION = 'NgStore2.wsgi.application'
ASGI_APPLICATION = 'NgStore2.asgi.application'
#ASGI_APPLICATION = 'NgStore2.routing.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'URL': os.getenv("DATABASE_URL"),
#         'NAME': os.getenv("PGDATABASE"),
#         'USER': os.getenv("PGUSER"),
#         "PASSWORD": os.getenv("PGPASSWORD"),
#         "HOST": os.getenv("PGHOST"),
#         "PORT": os.getenv("PGPORT"),
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': os.getenv("MSDATABASE"),
#         'USER': os.getenv("MSUSER"),
#         "PASSWORD": os.getenv("MSPASSWORD"),
#         "HOST": os.getenv("MSHOST"),
#         # "PORT": os.getenv("MSPORT"),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myRestaurant',
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
STATIC_ROOT = os.path.join(BASE_DIR, "static", "staticfiles_build", "staticfiles")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MPTT_ADMIN_LEVEL_INDENT = 20




