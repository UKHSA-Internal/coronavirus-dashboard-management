from opencensus.ext.azure.log_exporter import AzureLogHandler
from middleware.tracers.azure.exporter import Exporter as AzureExporter
from opencensus.trace import config_integration

from pathlib import Path
from sys import stdout
from os import getenv, environ
import re


config_integration.trace_integrations(['postgresql'])
config_integration.trace_integrations(['logging'])
config_integration.trace_integrations(['requests'])


BASE_DIR = Path(__file__).resolve().parent.parent

db_cstr = getenv("POSTGRES_CONNECTION_STRING")

ENVIRONMENT = getenv("API_ENV")
INSTRUMENTATION_KEY_RAW = getenv("APPINSIGHTS_INSTRUMENTATIONKEY", "")
INSTRUMENTATION_KEY = f'InstrumentationKey={INSTRUMENTATION_KEY_RAW}'
CLOUD_ROLE_NAME = getenv("WEBSITE_SITE_NAME", "Administration")
CLOUD_INSTANCE_ID = getenv("WEBSITE_INSTANCE_ID", "local")

SECRET_KEY = getenv("DJANGO_SECRET_KEY")

DEBUG = getenv("IS_DEV", "0") == "1"

BASE_DOMAIN = f"greenhouse.{getenv('URL_LOCATION')}"


if not DEBUG:
    IS_LIVE = True

    SESSION_COOKIE_HTTPONLY = True
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_DOMAIN = BASE_DOMAIN
    SESSION_COOKIE_AGE = 1800
    SESSION_COOKIE_SAMESITE = 'Strict'
    SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True

    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = BASE_DOMAIN

    SECURE_HSTS_SECONDS = 1800
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_REFERRER_POLICY = 'same-origin'

    SECURE_SSL_REDIRECT = True

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    USE_X_FORWARDED_HOST = True

    AZURE_CUSTOM_DOMAIN = getenv("URL_LOCATION", "") + '/public'


DISALLOWED_USER_AGENTS = []


# Delegated to the server
ALLOWED_HOSTS = [
    '*'
    # '0.0.0.0',
    # BASE_DOMAIN,
    # getenv("WEBSITE_HOSTNAME")
]


# Application definition
INSTALLED_APPS = [
    'admin_reorder',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'service_admin.apps.ServiceAdminConfig',
    'cms.apps.CMSConfig',
    'guardian',
    'markdownx',
    'django_admin_json_editor',
    'rest_framework',
    'reversion',
]


MIDDLEWARE = [
    'middleware.admin_reorder.ModelAdminReorder',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.tracers.django.TraceRequestMiddleware',
]


ADMIN_REORDER = (
    {
        'app': 'auth',
        'label': 'Access',
        'models': (
            'auth.User',
            'auth.Group',
        ),
    },
    {
        'app': 'service_admin',
        'label': 'References',
        'models': (
            'service_admin.MetricReference',
            'service_admin.MetricAsset',
            'service_admin.MetricETLReference',
            'service_admin.AreaReference',
        )
    },
    {
        'app': 'service_admin',
        'label': 'Data',
        'models': (
            'service_admin.ReleaseReference',
            'service_admin.ProcessedFile',
            'service_admin.TimeSeries',
        )
    },
    {
        'app': 'service_admin',
        'label': 'Notifications',
        'models': (
            'service_admin.ChangeLog',
            'service_admin.Announcement',
            'service_admin.PrivateReport',
            'service_admin.ReportRecipient',
        )
    },
    {
        'app': 'service_admin',
        'label': 'Service',
        'models': (
            'service_admin.Tag',
            'service_admin.Page',
            'service_admin.Colour',
        )
    },
    # {
    #     'app': 'service_admin',
    #     'label': 'CMS',
    #     'models': (
    #         'service_admin.Card',
    #         'service_admin.Tab',
    #         'service_admin.TabField',
    #         'service_admin.VisualisationField',
    #         'service_admin.TabulationField',
    #         'service_admin.RollingAverage',
    #         'service_admin.CustomFilterParameter',
    #         'service_admin.Highlight',
    #         'service_admin.LocationFilter',
    #     )
    # }
)

REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    # Use Django's standard `django.contrib.auth` permissions
    # and deny all access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata'
}


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

ROOT_URLCONF = 'administration.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.joinpath("templates")
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'administration.wsgi.application'
ASGI_APPLICATION = 'administration.asgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

db_cstr_pattern = re.compile(
    r'^postgres://'
    r'(?P<USER>[^:]+):?'
    r'(?P<PASSWORD>.*)?@'
    r'(?P<HOST>[^/]+)/'
    r'(?P<NAME>\w+)$',
    re.ASCII | re.VERBOSE
)

db_creds = db_cstr_pattern.search(db_cstr).groupdict()

DB_USER = getenv("Postgres_Write_Username", "")
DB_PASSWORD = getenv("Postgres_Write_Password", "")
DB_HOST = getenv("Postgres_Host", "")
DB_NAME = getenv("Postgres_Db", "")

DATABASES = {
    'default': {
        'ENGINE': 'django_multitenant.backends.postgresql',
        'SCHEMA': 'covid19',
        'DISABLE_SERVER_SIDE_CURSORS': False,
        'USER': db_creds.get("USER", DB_USER),
        'PASSWORD': db_creds.get("PASSWORD", DB_PASSWORD),
        'HOST': db_creds.get("HOST", DB_HOST),
        'NAME': db_creds.get("NAME", DB_NAME),
        # 'OPTIONS': {
        #     'options': '-c search_path=public,covid19',
        # }
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
            'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'max_similarity': 0.3,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 15,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]


# log_handler = AzureLogHandler(instrumentation_key=INSTRUMENTATION_KEY_RAW)
# log_handler.add_telemetry_processor(
#     lambda envelope: envelope.tags.update({'ai.cloud.role': CLOUD_ROLE_NAME})
# )

EXPORTER = AzureExporter(connection_string=INSTRUMENTATION_KEY)
EXPORTER.add_telemetry_processor(
    lambda envelope: envelope.tags.update({
        'ai.cloud.role': CLOUD_ROLE_NAME,
        'ai.cloud.roleInstance': CLOUD_INSTANCE_ID
    })
)

OPENCENSUS = {
    'TRACE': {
        'SAMPLER': 'opencensus.trace.samplers.AlwaysOnSampler()',
        'EXPORTER': EXPORTER,
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    "handlers": {
        "azure": {
            "level": "INFO",
            "class": "opencensus.ext.azure.log_exporter.AzureLogHandler",
            "instrumentation_key": INSTRUMENTATION_KEY_RAW
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": stdout,
        },
      },
    "loggers": {
        'django': {
            'handlers': ["azure", "console"],
            'propagate': True,
            'level': 'INFO'
        },
        'uvicorn': {
            'handlers': ["azure", "console"],
            'propagate': True,
            'level': 'INFO'
        },
        'gunicorn': {
            'handlers': ["azure", "console"],
            'propagate': True,
            'level': 'INFO'
        },
    },
}


if not DEBUG:
    CACHES = {
        "default": {
            "BACKEND": "redis_cache.ShardedRedisCache",
            "LOCATION": f'{getenv("AZURE_REDIS_HOST")}:{getenv("AZURE_REDIS_PORT")}',
            "OPTIONS": {
                "PASSWORD": getenv("AZURE_REDIS_PASSWORD"),
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
                'CONNECTION_POOL_CLASS_KWARGS': {
                    'max_connections': 10,
                    'timeout': 10,
                },
                'SERIALIZER_CLASS': 'redis_cache.serializers.PickleSerializer',
                'SERIALIZER_CLASS_KWARGS': {
                    'pickle_version': -1
                },
            },
            "KEY_PREFIX": "admin"
        }
    }


# Internationalization

LANGUAGE_CODE = 'en-GB'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

FIRST_DAY_OF_WEEK = 1  # Monday

# -------------------------------------------------------------------
# STATIC FILES
# -------------------------------------------------------------------

STATIC_URL = '/static/'

# STATIC_ROOT = BASE_DIR.joinpath('static_private')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_DIRS = [
    BASE_DIR.joinpath('static_private')
]


DEFAULT_FILE_STORAGE = 'storage.handler.AzureStorage'
STATICFILES_STORAGE = 'storage.handler.AzureStorage'


AZURE_CONNECTION_STRING = getenv("DeploymentBlobStorage")
AZURE_SSL = True
AZURE_UPLOAD_MAX_CONN = 10
AZURE_CONNECTION_TIMEOUT_SECS = 20
AZURE_BLOB_MAX_MEMORY_SIZE = '2MB'
AZURE_URL_EXPIRATION_SECS = None
AZURE_OVERWRITE_FILES = True
AZURE_LOCATION = "admin"
AZURE_CONTAINER = "static"
AZURE_CACHE_CONTROL = "public, max-age=600, s-maxage=1800"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
