import os
import django

# Django settings ko load karo
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Yahan apna Username aur Password set karo
USERNAME = "admin"
EMAIL = "admin@example.com"
PASSWORD = "AdminPassword123"  # <--- Isse login karna

def create_admin():
    if not User.objects.filter(username=USERNAME).exists():
        print(f"Creating new superuser: {USERNAME}")
        User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
        print("✅ Superuser created successfully!")
    else:
        print("⚠️ Superuser already exists. Skipping.")

if __name__ == "__main__":
    create_admin()