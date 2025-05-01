from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('verify-email/<int:user_id>/<str:token>/', views.verify_email, name='verify_email'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<int:pk>/', views.profile_view, name='profile_detail'),
    # path('search/', views.hotel_search, name='hotel_search'),
    path('hotel/<int:pk>/', views.hotel_detail, name='hotel_detail'), 
    path('book-room/<int:room_id>/', views.book_room, name='book_room'),


    path('ajax/hotel-search/', views.ajax_hotel_search, name='ajax_hotel_search'),

    # path('hotel/<int:pk>/', views.hotel_detail, name='hotel_detail'),

    path('ajax/filter-rooms/<int:hotel_id>/', views.ajax_filter_rooms, name='ajax_filter_rooms'),
    
    path('about/', views.about, name='about'),
    # path('about/', views.about, name='about'),
]



