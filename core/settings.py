import os
from pathlib import Path
from dotenv import load_dotenv
from django.templatetags.static import static
from django.urls import reverse_lazy
import dj_database_url

# 1. Load Environment Variables
load_dotenv()

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. SECRET KEY
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key-change-in-prod')

# 3. DEBUG LOGIC (Automatic)
# Agar Render par hai to DEBUG False hoga, Local laptop par True hoga
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    # Unfold Admin Apps (Sabse Upar)
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    
    'cloudinary_storage',      # Storage pehle aana chahiye
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'blog',
    'ckeditor',
    'cloudinary',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <--- WhiteNoise 2nd position par (Correct)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.context_processors.common_data',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# 4. DATABASE CONFIGURATION
# Render par PostgreSQL automatic connect hoga, Local par SQLite
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600
    )
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- STATIC FILES (CSS/JS) ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# ★ FIXED: "Manifest" hata diya taaki missing files ki wajah se crash na ho
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# --- CLOUDINARY CONFIGURATION (Images) ---
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'), 
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'), 
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET')
}

MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


# --- CKEDITOR CONFIGURATION ---
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Maximize',],
        ],
        'width': 'auto',
    },
}

SILENCED_SYSTEM_CHECKS = ['ckeditor.W001']


# --- CUSTOM ADMIN SETTINGS (Django Unfold) ---
UNFOLD = {
    "SITE_TITLE": "RoyBlog Admin",
    "SITE_HEADER": "RoyBlog Dashboard",
    "SITE_URL": "/",
    # Icons configuration
    "SITE_ICON": {
        "light": lambda request: static("images/favicon.png"),
        "dark": lambda request: static("images/favicon.png"),
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Navigation",
                "separator": True,
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": "Go to Site",
                        "icon": "web",
                        "link": "/",
                    },
                ],
            },
        ],
    },
}


# 5. SECURITY & HTTPS SETTINGS (Logic Added)
# Agar Production (Render) par hain, toh Security Tight karo
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Render Domain ko trust karo (Login Fix)
    if RENDER_EXTERNAL_HOSTNAME:
        CSRF_TRUSTED_ORIGINS = [f'https://{RENDER_EXTERNAL_HOSTNAME}']
else:
    # Localhost settings
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False



    # --- DEBUGGING (Add at the bottom of settings.py) ---
print("="*50)
print(f"DEBUG: BASE_DIR is: {BASE_DIR}")
print(f"DEBUG: Static folder check: {BASE_DIR / 'static'}")
print(f"DEBUG: Folder exists?: {os.path.exists(BASE_DIR / 'static')}")
print("="*50)