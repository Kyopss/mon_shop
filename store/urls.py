from django.urls import path
from . import views

app_name = 'store' # <--- TRÈS IMPORTANT

urlpatterns = [
    path('', views.product_all, name='product_all'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:category_slug>/', views.category_list, name='category'), # <--- L'URL manquante
]