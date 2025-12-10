"""
WSGI config for viralbrain project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# Add the project directory to the sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set the Django settings module to the correct settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'viralbrain.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Create the Django WSGI application
application = get_wsgi_application()

# Vercel requires the WSGI application to be exposed as 'app'
# This allows Vercel's serverless function to properly route requests
app = application
