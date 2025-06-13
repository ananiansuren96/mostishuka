from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_listing, name='add_listing'),
    path('category/<slug:slug>/', views.category_list, name='category_list'),
]
