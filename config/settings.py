from pathlib import Path
import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent


env = environ.Env(DEBUG=(bool, True))


environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, 'env/.settings')
)


SECRET_KEY = 'django-insecure-m%ku%95!)mw%9-%q3216@iq&mmkokh26eg7lw+rq=ppjzzm-+t'


DEBUG = True

ALLOWED_HOSTS = ['*']

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

X_FRAME_OPTIONS = 'SAMEORIGIN'

BASE_INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',

]

PROJECT_INSTALLED_APPS = [
    'accounts',
    'main',
    'introduce',
    'tech',
]

LIBRARY_INSTALLED_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.naver',
    'allauth.socialaccount.providers.kakao',
    'rest_framework',
    'debug_toolbar',
    'django_bootstrap5',
    'django_session_timeout',
    'django_summernote',
    'bootstrap4',
    'django_extensions',
]

SITE_ID = 2

SESSION_COOKIE_AGE = 1200
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_SECONDS = 1200 # One day
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD = 10 # 10초 동안 아무런 작업이 없을경우 SESSION_EXPIRE_SECONDS 시간 연산 시작
SESSION_TIMEOUT_REDIRECT = 'http://127.0.0.1:8000/accounts/login/'

INSTALLED_APPS = BASE_INSTALLED_APPS + PROJECT_INSTALLED_APPS + LIBRARY_INSTALLED_APPS

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_AUTHENICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = "TEST"
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
# EMAIL_HOST_USER = env('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', os.path.join(BASE_DIR, 'templates', 'account')],
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


STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

WSGI_APPLICATION = 'config.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

LANGUAGE_CODE = env('LANGUAGE_CODE')
TIME_ZONE = env('TIME_ZONE')

USE_I18N = True

USE_TZ = True

MEDIA_URL = 'media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.Users'

LOGIN_REDIRECT_URL = '/account/login/'
LOGOUT_REDIRECT_URL = 'account/login/'
LOGIN_URL = '/accounts/login/'

INTERNAL_IPS = [
    "127.0.0.1",
]

SUMMERNOTE_THEME = 'bs4'

# REDIS_HOST = env('REDIS_HOST')
# REDIS_PORT = env('REDIS_PORT')
# REDIS_DB = env('REDIS_DB')
