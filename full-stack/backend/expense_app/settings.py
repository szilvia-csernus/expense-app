from pathlib import Path
from dotenv import load_dotenv
import os
import dj_database_url
# import django_heroku  # for Heroku deployment


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# The .env file will only be loaded if the project is used without Docker.
# If Docker is used, the DJANGO_ENV environment variable will be loaded from
# the docker-compose.dev.yml or docker-compose.prod.yml files.
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') == 'True'

# This is a list of strings representing the host/domain names that Django
# can serve. This is a security measure to prevent HTTP Host header attacks.
ALLOWED_HOSTS = [os.getenv("BACKEND_HOST")]

# This is a list of origins that are authorized to make cross-origin requests.
# Cross-Origin Resource Sharing (CORS) is a mechanism that allows many
# resources (e.g., fonts, JavaScript, etc.) on a web page to be requested from
# another domain outside the domain from which the resource originated.
CORS_ALLOWED_ORIGINS = [
    os.getenv("FRONTEND_URL")
]

# This setting was needed because the admin panel is proxy_routed to the
# frontend, and sending requests from here back to the backend are seen
# as cross-site-requests.
CSRF_TRUSTED_ORIGINS = [os.getenv("FRONTEND_URL")]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',  # for cloudinary
    'cloudinary',  # for cloudinary
    'rest_framework',
    'corsheaders',  # new

    'custom_commands',
    'profiles',
    'cost_centers',
    'claims',
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


if 'DEVELOPMENT' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

else:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL', ''))
    }

    # This config was used for Docker container-based postgres database.
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql',
    #         'NAME': os.getenv("POSTGRES_DB"),
    #         'USER': os.getenv("POSTGRES_USER"),
    #         'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
    #         'HOST': os.getenv("POSTGRES_HOST"),
    #         'PORT': '5432'  # default postgres port
    #     }
    # }


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
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )  # has to be a tuple

# STATIC_ROOT = '/staticfiles/'  # for AWS deployment
STATIC_ROOT = BASE_DIR / 'staticfiles'  # for Heroku deployment

# for Heroku deployment
# STATICFILES_STORAGE =
#   'whitenoise.storage.CompressedManifestStaticFilesStorage'

# WHITENOISE_STATIC_ROOT = BASE_DIR / 'staticfiles/'  # for Heroku deployment

# django_heroku.settings(locals())  # for Heroku deployment

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# The default file size limit is 2.5 MB. As the user can upload up to 5MB of
# images and we have to process them to create the PDF, we increased the limit.
FILE_UPLOAD_MAX_MEMORY_SIZE = 6 * 1024 * 1024  # 6 MB

CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL': os.getenv("CLOUDINARY_URL"),
}

MEDIA_URL = '/media/'

# This is only for the admin-uploaded files. (The logo images of the churches.)
# The user-uploaded images are not stored anywhere in the backend, they are
# being manipulated by a backend process and then sent as an email attachment.
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


ADMINS = [('Admin', os.environ.get('EMAIL_HOST_USER'))]

# Configure logging to put the logs in the console. This will be used by
# AWS's CloudWatch to collect the logs.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
