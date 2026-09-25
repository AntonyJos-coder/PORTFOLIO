"""
Django settings for portfolio_site project.
"""

import os
import sys
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

try:
    import whitenoise  # noqa: F401
    HAS_WHITENOISE = True
except ImportError:
    HAS_WHITENOISE = False

# ── Paths ─────────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file (silently ignored if not present, e.g. on Render)
load_dotenv(BASE_DIR / '.env')


# ── Helpers ───────────────────────────────────────────────────────────────────

def _env_bool(name, default=False):
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _env_list(name, default=""):
    raw = os.environ.get(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


# ── Environment detection ─────────────────────────────────────────────────────

IS_RENDER = bool(os.environ.get("RENDER"))

DEBUG = _env_bool("DEBUG", default=not IS_RENDER)

# ── Security ──────────────────────────────────────────────────────────────────

SECRET_KEY = os.environ.get("SECRET_KEY") or os.environ.get("DJANGO_SECRET_KEY", "")
if not SECRET_KEY:
    if DEBUG or "collectstatic" in sys.argv:
        SECRET_KEY = "django-insecure-dev-only-change-me"
    else:
        raise ImproperlyConfigured("SECRET_KEY must be set when DEBUG is False.")

ALLOWED_HOSTS = _env_list("ALLOWED_HOSTS", "127.0.0.1,localhost")
if IS_RENDER:
    ALLOWED_HOSTS.append(".onrender.com")
    render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
    if render_host:
        ALLOWED_HOSTS.append(render_host)

CSRF_TRUSTED_ORIGINS = _env_list(
    "CSRF_TRUSTED_ORIGINS",
    "http://127.0.0.1:8000,http://localhost:8000" if DEBUG else "",
)
if IS_RENDER:
    CSRF_TRUSTED_ORIGINS.append("https://*.onrender.com")
    render_url = os.environ.get("RENDER_EXTERNAL_URL")
    if render_url:
        CSRF_TRUSTED_ORIGINS.append(render_url.rstrip("/"))


# ── Apps ──────────────────────────────────────────────────────────────────────

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'portfolio.apps.PortfolioConfig',
]


# ── Middleware ────────────────────────────────────────────────────────────────

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
]
if HAS_WHITENOISE:
    MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')
MIDDLEWARE += [
    'portfolio_site.middleware.SecurityHeadersMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portfolio_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'portfolio_site.wsgi.application'


# ── Database ──────────────────────────────────────────────────────────────────
# DATABASE_URL env var → Supabase PostgreSQL.
# Falls back to SQLite for local dev when DATABASE_URL is not set.

_DATABASE_URL = os.environ.get('DATABASE_URL')
_COLLECTING_STATIC = "collectstatic" in sys.argv

if IS_RENDER and not _DATABASE_URL and not _COLLECTING_STATIC:
    raise ImproperlyConfigured(
        "DATABASE_URL is required on Render. Set it in the Render dashboard."
    )

if _DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            _DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=_env_bool("DB_SSL_REQUIRE", default=True),
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ── Password validation ───────────────────────────────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ── Internationalisation ──────────────────────────────────────────────────────

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


# ── Static files ──────────────────────────────────────────────────────────────

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

WHITENOISE_MAX_AGE = 31536000
WHITENOISE_USE_FINDERS = DEBUG

# ── Supabase Storage (S3-compatible) ─────────────────────────────────────────
# Set SUPABASE_STORAGE_* vars in .env / Render dashboard to enable cloud media.
# Without them, local FileSystemStorage is used (fine for dev, breaks on Render).

_sb_url        = os.environ.get("SUPABASE_URL", "")           # e.g. https://xxxx.supabase.co
_sb_key        = os.environ.get("SUPABASE_SERVICE_KEY", "")   # service_role key (not anon key)
_sb_bucket     = os.environ.get("SUPABASE_BUCKET", "media")   # bucket name you created
_sb_region     = os.environ.get("SUPABASE_REGION", "ap-southeast-2")  # match your project region

_USE_SUPABASE_STORAGE = bool(_sb_url and _sb_key and _sb_bucket)

if _USE_SUPABASE_STORAGE:
    # Supabase Storage exposes an S3-compatible endpoint at:
    # https://<project-ref>.supabase.co/storage/v1/s3
    _sb_project_ref = _sb_url.replace("https://", "").split(".")[0]

    AWS_ACCESS_KEY_ID       = _sb_project_ref          # Supabase uses project ref as access key
    AWS_SECRET_ACCESS_KEY   = _sb_key
    AWS_STORAGE_BUCKET_NAME = _sb_bucket
    AWS_S3_REGION_NAME      = _sb_region
    AWS_S3_ENDPOINT_URL     = f"{_sb_url}/storage/v1/s3"
    AWS_S3_FILE_OVERWRITE   = False                    # keep original filename on re-upload
    AWS_DEFAULT_ACL         = "public-read"            # files must be public for the portfolio
    AWS_QUERYSTRING_AUTH    = False                    # serve clean URLs without signed params
    AWS_S3_CUSTOM_DOMAIN    = None                     # use Supabase CDN URL directly

    # Public URL pattern Supabase uses for objects:
    # https://<project>.supabase.co/storage/v1/object/public/<bucket>/<path>
    MEDIA_URL = f"{_sb_url}/storage/v1/object/public/{_sb_bucket}/"

if not DEBUG:
    _default_storage = (
        "storages.backends.s3boto3.S3Boto3Storage"
        if _USE_SUPABASE_STORAGE
        else "django.core.files.storage.FileSystemStorage"
    )
    STORAGES = {
        "default": {
            "BACKEND": _default_storage,
        },
        "staticfiles": {
            "BACKEND": (
                "whitenoise.storage.CompressedStaticFilesStorage"
                if HAS_WHITENOISE
                else "django.contrib.staticfiles.storage.StaticFilesStorage"
            ),
        },
    }

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ── Upload / request size limits ──────────────────────────────────────────────

DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024   # 5 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024   # 5 MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 200


# ── Cookies & browser security ────────────────────────────────────────────────

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"

if not DEBUG:
    SECURE_SSL_REDIRECT = _env_bool("SECURE_SSL_REDIRECT", default=IS_RENDER)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# ── Email (Gmail SMTP) ────────────────────────────────────────────────────────
# Set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in .env (or Render dashboard) to
# enable real email. Without them Django prints to the console (safe for dev).

_email_user = os.environ.get("EMAIL_HOST_USER", "")
_email_pass = os.environ.get("EMAIL_HOST_PASSWORD", "")

if _email_user and _email_pass:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = _email_user
    EMAIL_HOST_PASSWORD = _email_pass
    DEFAULT_FROM_EMAIL = f"Portfolio Contact <{_email_user}>"
    SERVER_EMAIL = _email_user
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    EMAIL_HOST_USER = _email_user

# Address that receives contact-form notification emails
CONTACT_NOTIFY_EMAIL = os.environ.get("CONTACT_NOTIFY_EMAIL", _email_user)


# ── Cache ─────────────────────────────────────────────────────────────────────

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "portfolio",
        "TIMEOUT": 120,
        "OPTIONS": {"MAX_ENTRIES": 256},
    }
}


# ── Logging ───────────────────────────────────────────────────────────────────

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}
