"""Configuración mínima de Django para pruebas (SQLite, sin red)."""
SECRET_KEY = "clave-solo-para-pruebas"
DEBUG = True
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = ["django.contrib.contenttypes", "pedidos"]
MIDDLEWARE = []
ROOT_URLCONF = "config.urls"
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
USE_TZ = True
