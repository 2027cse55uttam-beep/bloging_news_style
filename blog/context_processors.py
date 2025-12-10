from .models import Category

def common_data(request):
    # Saari categories fetch karein taaki Navbar mein dikha sakein
    return {
        'all_categories': Category.objects.all()
    }