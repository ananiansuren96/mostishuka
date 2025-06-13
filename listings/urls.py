from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_listing, name='add_listing'),
    path('listing/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('category/<slug:category_slug>/', views.category_list, name='category_list'),
]
