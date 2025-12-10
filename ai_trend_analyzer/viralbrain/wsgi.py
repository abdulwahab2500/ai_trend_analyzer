import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'viralbrain.settings')

application = get_wsgi_application()
app = application  # Expose 'app' for Vercel
