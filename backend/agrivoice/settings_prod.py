import os
import dj_database_url
from .settings import *

DEBUG = False

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "").strip()
if not SECRET_KEY or SECRET_KEY == "your-production-secret-key-here":
    raise RuntimeError("Set a strong DJANGO_SECRET_KEY environment variable.")

def _csv_env(name):
    return [value.strip() for value in os.environ.get(name, "").split(",") if value.strip()]

allowed_hosts = _csv_env("ALLOWED_HOSTS")
for env_name in ("RENDER_EXTERNAL_HOSTNAME", "RAILWAY_PUBLIC_DOMAIN"):
    host = os.environ.get(env_name, "").strip()
    if host:
        allowed_hosts.append(host.removeprefix("https://").removeprefix("http://").rstrip("/"))
if not allowed_hosts:
    raise RuntimeError("Set ALLOWED_HOSTS to your deployed backend hostname(s).")
ALLOWED_HOSTS = list(dict.fromkeys(allowed_hosts))

DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()
if DATABASE_URL:
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=DATABASE_URL.startswith("postgres"))}
else:
    # Demo fallback only. Use a persistent PostgreSQL DATABASE_URL for production data.
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": os.environ.get("SQLITE_PATH", "/tmp/db.sqlite3")}}

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

frontend_url = os.environ.get("FRONTEND_URL", "").strip().rstrip("/")
CORS_ALLOWED_ORIGINS = [frontend_url] if frontend_url else []
CSRF_TRUSTED_ORIGINS = [frontend_url] if frontend_url else []


CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "webmaster@localhost")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
SARVAM_API_KEY = os.environ.get("SARVAM_API_KEY", "")
