# Settings file to be used exclusively to collect static files.
#
# WARNING:
# This file should not be used to test or deploy the app.

from pathlib import Path
from secrets import token_urlsafe

BASE_DIR = Path(__file__).resolve().parent.parent

ENVIRONMENT = "DEVELOPMENT"
ETL_STORAGE = ""

# Set something random - just so it's present.
SECRET_KEY = token_urlsafe(48)

ALLOWED_HOSTS = [
    '*'
]

DISALLOWED_USER_AGENTS = []


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
            'admin.LogEntry',
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


# -------------------------------------------------------------------
# STATIC FILES
# -------------------------------------------------------------------

STATIC_ROOT = BASE_DIR.joinpath('static_private')
STATIC_URL = "/static/"

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

