import os
from pathlib import Path
from dotenv import load_dotenv  # <--- Import This
from django.templatetags.static import static
from django.urls import reverse_lazy
# .env file load karein (Local development ke liye)
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Ab ye .env file se key uthayega
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key-if-not-found')

# DEBUG value check
DEBUG = os.getenv('DEBUG') == 'True'

# HTTPS Problem Fix (Localhost ke liye sab False rakhein)
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",  # Advanced filters ke liye
    "unfold.contrib.forms",    # Forms sundar banane ke liye
    'cloudinary_storage',
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


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [BASE_DIR / "static"]


# --- CLOUDINARY CONFIGURATION (Images) ---
# Ab ye .env file se keys uthayega
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'), 
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'), 
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET')
}

# Media Settings
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
    "SITE_ICON": {
        "light": lambda request: static("images/favicon.png"),  # Light mode icon
        "dark": lambda request: static("images/favicon.png"),   # Dark mode icon
    },
    "SIDEBAR": {
        "show_search": True,  # Sidebar mein search bar
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