from .base import *  # noqa

DEBUG = False

# Render (like most hosts) terminates HTTPS at its proxy and forwards plain
# HTTP. Without this, SECURE_SSL_REDIRECT redirects every request forever.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
