import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from django.templatetags.static import static
from django.urls import reverse_lazy
import dj_database_url

# 1. Load Environment Variables
load_dotenv()

# Build paths - Pathlib ka use (Sabse Safe)
BASE_DIR = Path(__file__).resolve().parent.parent

# --- DEBUGGING PRINTS (Logs mein dikhenge) ---
# Ye batayega ki server par folders kahan hain
print("="*50)
print(f"DEBUG: BASE_DIR is: {BASE_DIR}")
print(f"DEBUG: Looking for static in: {BASE_DIR / 'static'}")
print(f"DEBUG: Does static folder exist?: {(BASE_DIR / 'static').exists()}")
print("="*50)
# ---------------------------------------------

# 2. SECRET KEY
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key-change-in-prod')

# 3. DEBUG LOGIC
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    # Unfold Admin
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    
    # ★ CHANGE IS HERE: Staticfiles ko Cloudinary se UPAR rakho ★
    'django.contrib.staticfiles',  
    'cloudinary_storage',        
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    
    # Apps
    'blog',
    'ckeditor',
    'cloudinary',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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


# --- STATIC FILES (THE MAIN FIX) ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise Storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Correct Pathlib Syntax
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# ★ Zabardasti Dhoondne wala Finder (Explicit) ★
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


# --- CLOUDINARY CONFIGURATION ---
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


# --- CUSTOM ADMIN SETTINGS ---
UNFOLD = {
    "SITE_TITLE": "RoyBlog Admin",
    "SITE_HEADER": "RoyBlog Dashboard",
    "SITE_URL": "/",
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


# 5. SECURITY & HTTPS SETTINGS
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    if RENDER_EXTERNAL_HOSTNAME:
        CSRF_TRUSTED_ORIGINS = [f'https://{RENDER_EXTERNAL_HOSTNAME}']
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False


    # Agar ye line nahi hai, toh add karo:
CSRF_TRUSTED_ORIGINS = ['https://bloging-news-style.onrender.com']