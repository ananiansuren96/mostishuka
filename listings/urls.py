from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_listing, name='add_listing'),
    path('listing/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('category/<slug:category_slug>/', views.category_list, name='category_list'),

    path('listings-ajax/', views.listings_ajax, name='listings_ajax'),

    # Авторизация и регистрация
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # Новые маршруты для переписок
    path('messages/', views.conversations_list, name='conversations_list'),            # Список всех переписок текущего пользователя
    path('messages/<int:user_id>/', views.conversation_detail, name='conversation_detail'),  # Чат с конкретным пользователем
    path('messages/delete-conversation/<int:user_id>/', views.delete_conversation, name='delete_conversation'),

]
