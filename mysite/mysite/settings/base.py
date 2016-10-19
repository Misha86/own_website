with open('mysite\secret_key.txt') as f:
    SECRET_KEY = f.read().strip()


DEBUG = False

EMAIL_HOST = 'smtp.gmail.com'                # Имя хоста используемое для отправки электронных писем. По умолчанию 'localhost'
EMAIL_HOST_USER = 'yourgmail@gmail.com'      # Имя пользователя используемое при подключении к SMTP серверу указанному в EMAIL_HOST
EMAIL_HOST_PASSWORD = 'yourpassword'         # Пароль для подключения к SMTP сервера, который указан в EMAIL_HOST
EMAIL_SUBJECT_PREFIX = '[Django]'            # Префикс добавляемый к теме электронного письма
EMAIL_PORT = 587                             # Порт, используемый при подключении к SMTP серверу указанному в EMAIL_HOST.
EMAIL_USE_TLS = True                         # Указывает использовать ли TLS (защищенное) соединение с SMTP сервером. По умолчанию использует 587 порт.
EMAIL_USE_SSL = False                        # Указывает использовать ли TLS (защищенное) соединение с SMTP сервером. По умолчанию использует 465 порт.


LOGIN_URL = 'loginsys:login'                    # '/auth/login/'    It`s for @login_required().
LOGOUT_URL = 'loginsys:logout'                    # '/auth/logout/'

LOGIN_REDIRECT_URL = '/'

DEFAULT_FROM_EMAIL = 'mishaelitzem2@rambler.ru'

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
    ]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
            }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

# AUTH_USER_MODEL = 'loginsys.MyUser'


# it`s settings for cash

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
        'TIMEOUT': 600,
        'OPTIONS': {
            'MAX_ENTRIES': 20,
            'CULL_FREQUENCY': 2,
            }
    }
}

# it`s for cash all site

CACHE_MIDDLEWARE_SECONDS = 1800
CACHE_MIDDLEWARE_KEY_PREFIX = 'blog'

# SMTP backend(default) for send email

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'                # Имя хоста используемое для отправки электронных писем. По умолчанию 'localhost'
EMAIL_HOST_USER = 'yourgmail@gmail.com'      # Имя пользователя используемое при подключении к SMTP серверу указанному в EMAIL_HOST
EMAIL_HOST_PASSWORD = 'yourpassword'         # Пароль для подключения к SMTP сервера, который указан в EMAIL_HOST
EMAIL_SUBJECT_PREFIX = '[Django]'            # Префикс добавляемый к теме электронного письма
EMAIL_PORT = 587                             # Порт, используемый при подключении к SMTP серверу указанному в EMAIL_HOST.
EMAIL_USE_TLS = True                         # Указывает использовать ли TLS (защищенное) соединение с SMTP сервером. По умолчанию использует 587 порт.
EMAIL_USE_SSL = False                        # Указывает использовать ли TLS (защищенное) соединение с SMTP сервером. По умолчанию использует 465 порт.
# Обратите внимание, EMAIL_USE_TLS/EMAIL_USE_SSL взаимоисключающие, только одна настройка может быть True.

# Settings for logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
            },
        },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(BASE_DIR, 'log/debug.log'),
            },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
            },
        },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'mail_admins', 'file'],
            'level': 'DEBUG',
            'propagate': True,
            },
        },
    }

# отключить отчёты о 404 ошибке URL страницы заканчивается
import re
IGNORABLE_404_URLS = (
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$'),
)