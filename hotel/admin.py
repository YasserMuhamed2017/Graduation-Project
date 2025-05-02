from django.contrib import admin
from hotel.models import User, Hotel, Room, Booking, Review

# Register your models here.
admin.site.register(User)
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Review)
