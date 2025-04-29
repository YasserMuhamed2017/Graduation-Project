from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
from django.contrib.auth import authenticate, logout
from hotel.models import *
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Hotel, Room
from collections import defaultdict
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.template.loader import render_to_string

# Create your views here.
def index(request):
    hotels = Hotel.objects.all()  
    return render(request, 'hotel/index.html', {'hotels': hotels})

def login_view(request):
    return render(request, 'hotel/login.html')

def register_view(request):
    if request.method == 'POST':
        # Get values manually from POST
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')

        # Basic validation
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        # Create user but inactive
        user = User.objects.create_user(
            email=email,
            username=email,  # Assuming email is used as username
            password=make_password(password1),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone,
            gender=gender,
            date_of_birth=date_of_birth
        )
        user.save()

        # Generate email verification token
        token = default_token_generator.make_token(user)

        # Build verification URL
        verification_url = request.build_absolute_uri(
            f'/hotel/verify-email/{user.pk}/{token}/'
        )

         # Create the email body with HTML content
        html_message = render_to_string('hotel/verification_email.html', {
            'verification_url': verification_url,
            'user': user
        })
        # Send verification email
        send_mail(
            'Email Verification',
            f'Click the link to verify your email: {verification_url}',
            settings.EMAIL_HOST_USER,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )

        messages.success(request, "Account created! Please verify your email.")
        return redirect('login')

    return render(request, 'hotel/register.html')

def verify_email(request, user_id, token):
    try:
        user = User.objects.get(pk=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True  # Activate the user account
            user.save()
            login(request, user)  # Log the user in immediately
            return redirect('index')  # Redirect to home page or any other page
        else:
            messages.error(request, 'Invalid or expired verification link.')
            return redirect('login')
    except User.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
        return redirect('login')
    

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # assuming you're using email as username
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        print(user) 
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect('index')  # Redirect to homepage or dashboard
            else:
                messages.error(request, 'Your account is not active. Please verify your email.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
            return redirect('login')
    else:
        return render(request, 'hotel/login.html')
    
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')  # Redirect to login page after logout

# Hotel search 

# AJAX Hotel Search
def ajax_hotel_search(request):
    query = request.GET.get('location', '').strip()
    if not query:
        return JsonResponse({'hotels': []})

    hotels = Hotel.objects.filter(
        Q(name__icontains=query) | Q(location__icontains=query)
    )

    data = []
    for hotel in hotels:
        data.append({
            'id': hotel.id,
            'name': hotel.name,
            'location': hotel.location,
            'description': hotel.description[:50] + '...',
            'contact_number': hotel.contact_number,
            'image_url': hotel.image.url if hotel.image else '',
        })

    return JsonResponse({'hotels': data})


# Hotel details
def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    rooms = hotel.rooms.all()

    selected_room_type = request.GET.get('room_type')
    selected_availability = request.GET.get('availability')

    if selected_room_type:
        rooms = rooms.filter(room_type=selected_room_type)
    if selected_availability == 'available':
        rooms = rooms.filter(availability=True)
    elif selected_availability == 'unavailable':
        rooms = rooms.filter(availability=False)

    grouped_rooms_by_type = defaultdict(list)
    if not selected_room_type:
        for room in rooms:
            grouped_rooms_by_type[room.room_type].append(room)

    context = {
        'hotel': hotel,
        'rooms': rooms,
        'selected_room_type': selected_room_type,
        'selected_availability': selected_availability,
        'grouped_rooms_by_type': dict(grouped_rooms_by_type),
    }
    return render(request, 'hotel/hotel_detail.html', context)



def ajax_filter_rooms(request, hotel_id):
    room_type = request.GET.get('room_type')
    availability = request.GET.get('availability')

    rooms = Room.objects.filter(hotel_id=hotel_id)

    if room_type:
        rooms = rooms.filter(room_type=room_type)
    if availability:
        if availability == 'available':
            rooms = rooms.filter(availability=True)
        elif availability == 'unavailable':
            rooms = rooms.filter(availability=False)

    html = render_to_string('hotel/partials/room_list.html', {'rooms': rooms})
    return JsonResponse({'html': html})



def profile_view (request,pk):
    
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone_number')
        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('profile_detail', pk=pk)
    return render(request, 'hotel/profile_detail.html')


def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    bookings = room.bookings.all()  # Get all bookings for this room
    if request.method == 'POST':
        # Handle booking logic here
        # For example, you might want to create a booking record in the database
        # and send a confirmation email to the user.
        messages.success(request, "Room booked successfully!")
        return redirect('index')  # Redirect to a success page or hotel detail page

    return render(request, 'hotel/book_room.html', {'room': room, 'bookings': bookings})

  
