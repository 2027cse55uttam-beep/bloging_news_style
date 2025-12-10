from django.urls import path
from . import views

urlpatterns = [
    # Homepage URL (http://127.0.0.1:8000/)
    path('', views.index, name='home'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('<slug:post_slug>/', views.post_detail, name='post_detail'),

    path('category/<slug:category_slug>/', views.category_page, name='category_page'),

]