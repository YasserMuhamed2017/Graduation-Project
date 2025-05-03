from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('verify-email/<int:user_id>/<str:token>/', views.verify_email, name='verify_email'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<int:pk>/', views.profile_view, name='profile_detail'),
    path('profile/<int:pk>/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/<int:pk>/change-password/', views.change_password_view, name='change_password'),
    path('profile/<int:pk>/delete/', views.delete_account, name='delete_account'),
    path('profile/<int:pk>/delete-confirm/', views.delete_account_confirm, name='delete_account_confirm'),
    path('hotel/<int:pk>/', views.hotel_detail, name='hotel_detail'), 
    path('hotels/', views.hotels_list, name='hotels_list'),
    path('book-room/<int:room_id>/', views.book_room, name='book_room'),
    path('ajax/hotel-search/', views.ajax_hotel_search, name='ajax_hotel_search'),
    path('ajax/filter-rooms/<int:hotel_id>/', views.ajax_filter_rooms, name='ajax_filter_rooms'),
    path('about/', views.about, name='about'),
    path('user-reservations/', views.user_reservations, name='user_reservations'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]

