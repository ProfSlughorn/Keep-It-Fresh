"""
WSGI config for KeepItFresh project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import time
import logging
from django.core.wsgi import get_wsgi_application

# Set up logging to log startup time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Record the start time with higher precision
start_time = time.perf_counter()

# Set the default settings module for Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KeepItFresh.settings")

# Load the Django application
application = get_wsgi_application()

# Record the end time with higher precision
end_time = time.perf_counter()

# Calculate and log the total startup time
startup_time = end_time - start_time
logger.info(f"Django application startup time: {startup_time:.4f} seconds")
