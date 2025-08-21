import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = config('SECRET_KEY', default='your-secret-key-here')  # Ensure SECRET_KEY is set in environment
DEBUG = config('DEBUG', default=False, cast=bool)  # Default to False for production safety

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'digital8hub.forum',
    'digimkt.onrender.com',
    'blog-2xuq.onrender.com',
    config('ADDITIONAL_HOST', default=''),
]
# Remove empty strings from ALLOWED_HOSTS
ALLOWED_HOSTS = [host for host in ALLOWED_HOSTS if host]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # Third party apps
    'crispy_forms',
    'django_summernote',
    'taggit',
    # Local apps
    'blog',
    'affiliate',
    'analytics',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'analytics.middleware.AnalyticsMiddleware',
]

ROOT_URLCONF = 'digital_marketing_blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'digital_marketing_blog.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': config('DATABASE_PATH', default=BASE_DIR / 'db.sqlite3'),
    }
}

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = config('TIME_ZONE', default='UTC')
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# WhiteNoise configuration
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_USE_FINDERS = True

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security settings
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)  # Enable for production
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool)
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=True, cast=bool)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Cookie security
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)  # Enable for production
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://digimkt.onrender.com',
    'https://blog-2xuq.onrender.com',
    'https://digital8hub.forum',
    'http://localhost:8000',  # Specify port for local development
    'http://127.0.0.1:8000',
]

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')  # No default to enforce setting
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')  # No default to enforce setting
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default=EMAIL_HOST_USER)
SERVER_EMAIL = config('SERVER_EMAIL', default=EMAIL_HOST_USER)

# django-allauth configuration
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # Require email verification for signup
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # Use email instead of username
ACCOUNT_SIGNUP_REDIRECT_URL = '/'
ACCOUNT_LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[Digital8Hub] '

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': config('CACHE_BACKEND', default='django.core.cache.backends.locmem.LocMemCache'),
        'LOCATION': config('CACHE_LOCATION', default='unique-snowflake'),
        'TIMEOUT': config('CACHE_TIMEOUT', default=300, cast=int),
        'OPTIONS': {
            'MAX_ENTRIES': config('CACHE_MAX_ENTRIES', default=1000, cast=int),
        }
    }
}

# SEO settings
SEO_USE_CACHE = config('SEO_USE_CACHE', default=True, cast=bool)
SEO_CACHE_PREFIX = config('SEO_CACHE_PREFIX', default='seo_cache')

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'ignore_broken_pipe': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda record: not record.exc_info or not isinstance(record.exc_info[1], BrokenPipeError),
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['ignore_broken_pipe'],
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': config('LOG_LEVEL', default='INFO'),
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': config('DJANGO_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
        'analytics': {
            'handlers': ['console', 'file'],
            'level': config('ANALYTICS_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
        'blog': {
            'handlers': ['console', 'file'],
            'level': config('BLOG_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
        'affiliate': {
            'handlers': ['console', 'file'],
            'level': config('AFFILIATE_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
    },
}

# Create logs directory
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# Affiliate settings
AFFILIATE_DISCLOSURE_TEXT = config(
    'AFFILIATE_DISCLOSURE_TEXT',
    default="This post contains affiliate links. We may earn a commission if you make a purchase through these links."
)

# Third party app settings
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Summernote configuration
SUMMERNOTE_CONFIG = {
    'summernote': {
        'width': '100%',
        'height': '400',
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'underline', 'clear']],
            ['fontname', ['fontname']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', ['table']],
            ['insert', ['link', 'picture', 'video']],
            ['view', ['fullscreen', 'codeview', 'help']],
        ],
    }
}

# Django sites framework
SITE_ID = 1

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Session settings
SESSION_COOKIE_AGE = config('SESSION_COOKIE_AGE', default=1209600, cast=int)  # 2 weeks
SESSION_SAVE_EVERY_REQUEST = config('SESSION_SAVE_EVERY_REQUEST', default=False, cast=bool)
SESSION_EXPIRE_AT_BROWSER_CLOSE = config('SESSION_EXPIRE_AT_BROWSER_CLOSE', default=False, cast=bool)

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = config('FILE_UPLOAD_MAX_MEMORY_SIZE', default=2621440, cast=int)  # 2.5 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = config('DATA_UPLOAD_MAX_MEMORY_SIZE', default=2621440, cast=int)  # 2.5 MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = config('DATA_UPLOAD_MAX_NUMBER_FIELDS', default=1000, cast=int)

# Admin settings
ADMIN_URL = config('ADMIN_URL', default='admin/')

# Performance settings
USE_L10N = False
USE_THOUSAND_SEPARATOR = True

# Taggit settings
TAGGIT_CASE_INSENSITIVE = True

# Production-specific settings
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    X_FRAME_OPTIONS = 'DENY'
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    LOGGING['root']['handlers'] = ['file']
    LOGGING['loggers']['django']['handlers'] = ['file']

# Redirects
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
