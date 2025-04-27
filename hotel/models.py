from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=100)  # Store hashed passwords in production
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    is_admin = models.BooleanField(default=False)  # True if the user is an admin
    role = models.CharField(max_length=20, choices=[('customer', 'Customer'), ('staff', 'Staff')])
    gender = models.CharField(max_length=10)  

class Hotel(models.Model):
    contact_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2)

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=20)  # e.g., Single, Double, Suite
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    amenities = models.TextField()  # e.g., Wi-Fi, TV, AC, etc.
    room_image = models.ImageField(upload_to='room_images/', null=True, blank=True)  # Image field for room images

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)  # Automatically set the date when the booking is made
    