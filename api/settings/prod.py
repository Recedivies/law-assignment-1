"""
Configuration for deployment to GCE with Dockerfile
"""

import os

from api.settings.base import *  # noqa: F403, F401

# set SECRET_KEY for production
SECRET_KEY = os.environ.get("SECRET_KEY")

# debug has to be false in production
DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DATABASE_PROD_NAME"),
        "USER": os.environ.get("DATABASE_PROD_USERNAME"),
        "PASSWORD": os.environ.get("DATABASE_PROD_PASSWORD"),
        "HOST": os.environ.get("DATABASE_PROD_HOST"),
        "PORT": os.environ.get("DATABASE_PROD_PORT", "5432"),
        "CONN_MAX_AGE": int(os.environ.get("CONN_MAX_AGE", 0)),
    }
}
