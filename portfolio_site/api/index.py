import os
import sys
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SITE_ROOT))
os.chdir(SITE_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio_site.settings")

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
