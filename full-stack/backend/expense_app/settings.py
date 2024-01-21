from pathlib import Path
from dotenv import load_dotenv
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# The .env file will only be loaded if the project is used without Docker.
# If Docker is used, the DJANGO_ENV environment variable will be loaded from
# the docker-compose.dev.yml or docker-compose.prod.yml files.
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Check the DJANGO_ENV environment variable
DJANGO_ENV = os.getenv('DJANGO_ENV')

print('Environment: ', os.getenv('DJANGO_ENV'))

if DJANGO_ENV == 'development':
    # Load the development .env file
    load_dotenv(os.path.join(BASE_DIR, '.env.dev'))
else:
    # Load the production .env file
    load_dotenv(os.path.join(BASE_DIR, '.env.prod'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1']

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://192.168.40.59:5173",
    "http://127.0.0.1",
    "http://0.0.0.0",
]

CORS_ALLOWED_CREDENTIALS = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',  # for cloudinary
    'django.contrib.staticfiles',
    'cloudinary',  # for cloudinary
    'rest_framework',
    'corsheaders',  # new

    'custom_commands',
    'profiles',
    'claims',
    'churches',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # new
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # new
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'expense_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'expense_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


# if 'DEVELOPMENT' in os.environ:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# else:

#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': os.getenv("POSTGRES_DB"),
#             'USER': os.getenv("POSTGRES_USER"),
#             'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
#             'HOST': 'db',  # set in docker-compose.prod.yml
#             'PORT': '5432'  # default postgres port
#         }
#     }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
 {
  'NAME':
  'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'  # new
WHITENOISE_STATIC_ROOT = BASE_DIR / 'staticfiles'  # new

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# The default file size limit is 2.5 MB. As the user can upload up to 5MB of
# images and we have to process them to create the PDF, we increased the limit.
FILE_UPLOAD_MAX_MEMORY_SIZE = 6 * 1024 * 1024  # 5 MB

CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL': os.getenv("CLOUDINARY_URL"),
}

MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

if 'DJANGO_ENV' == 'development':
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASS')
    DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')
    EMAIL_PORT = 587
    SERVER_EMAIL = os.environ.get('EMAIL_HOST_USER')

FINANCE_EMAIL = os.environ.get('FINANCE_EMAIL')

ADMINS = [('Admin', os.environ.get('EMAIL_HOST_USER'))]
