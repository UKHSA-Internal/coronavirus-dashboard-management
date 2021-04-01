from django.core.wsgi import get_wsgi_application

from os import environ


environ.setdefault('DJANGO_SETTINGS_MODULE', 'administration.settings')

app = get_wsgi_application()
