from .base import * #noqa
from .base import env

SECRET_KEY = env(
    'DJANGO_SECRET_KEY',
    default='-g1lANNSqpO4H1-hxdt6kV8PxTVj7126SfIIArAAyabCsDnHNhc',)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:9090']

# EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='mailhog')
EMAIL_PORT = env('EMAIL_PORT')
DEFAULT_FROM_EMAIL = 'support@azubisc.site'
DOMAIN = env('DOMAIN')
SITE_NAME = 'Azubi SHopping Cart '