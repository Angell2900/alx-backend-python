import os
import django
from django.conf import settings
from pathlib import Path

def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    BASE_DIR = Path(__file__).resolve().parent
    
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            BASE_DIR=BASE_DIR,
            DATABASES={
                'default': {
                    'ENGINE': os.getenv('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
                    'NAME': os.getenv('DATABASE_NAME', ':memory:'),
                    'USER': os.getenv('DATABASE_USER', ''),
                    'PASSWORD': os.getenv('DATABASE_PASSWORD', ''),
                    'HOST': os.getenv('DATABASE_HOST', ''),
                    'PORT': os.getenv('DATABASE_PORT', ''),
                }
            },
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'messaging',
                'chats',
            ],
            MIDDLEWARE=[
                'django.middleware.security.SecurityMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.middleware.common.CommonMiddleware',
                'django.middleware.csrf.CsrfViewMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
            ],
            SECRET_KEY='test-secret-key-for-pytest',
            USE_TZ=True,
        )
    
    django.setup()
