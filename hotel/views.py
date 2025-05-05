from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login
from django.contrib.auth import authenticate, logout
from hotel.models import *
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from .models import Hotel, Room, Review
from collections import defaultdict
from django.db.models import Q
from django.shortcuts import get_object_or_404
# Remove this import as it conflicts with your custom User model
# from django.contrib.auth.models import User
from django.http import JsonResponse
from django.template.loader import render_to_string
import os
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import  time, requests


# Create your views here.
def index(request):
    hotels = Hotel.objects.all()
    top_hotels = Hotel.objects.order_by('-rating')[:5]
    context = {'top_hotels': top_hotels , 'hotels': hotels}  
    return render(request, 'hotel/index.html', context)

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
            'rating': hotel.rating,
        })

    if not query:
        return JsonResponse({'hotels': data})

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


@login_required
def edit_profile_view(request, pk):
    user = User.objects.get(pk=pk)
    
    # Check if the logged-in user is trying to edit their own profile
    if request.user.pk != user.pk:
        messages.error(request, "You don't have permission to edit this profile.")
        return redirect('profile_detail', pk=pk)
    
    if request.method == 'POST':
        # Update user information
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone_number')
        user.gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        if date_of_birth:
            user.date_of_birth = date_of_birth
            
        if request.POST.get('bio'):
            user.bio = request.POST.get('bio')
        # Handle profile picture if provided
        if 'profile_picture' in request.FILES:
            if hasattr(user, 'profile_picture'):
                user.profile_picture = request.FILES['profile_picture']
        
        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('profile_detail', pk=pk)
    
    return render(request, 'hotel/edit_profile.html', {'user': user})


def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    bookings = room.bookings.all()  # Get all bookings for this room
    for booking in bookings:
     booking.adjusted_checkout = booking.check_out_date - timedelta(days=1)
    reviews = room.reviews.all()  # Get all reviews for this room
    
    # Process amenities to a list for better display
    room.amenities_list = [amenity.strip() for amenity in room.amenities.split(',')]
    
    if request.method == 'POST':
        # Check if it's a booking submission or review submission
        if 'check_in_date' in request.POST:
            # Handle booking logic
            check_in_date = request.POST.get('check_in_date')
            check_out_date = request.POST.get('check_out_date')
            
            # Validate dates
            if check_in_date and check_out_date:
                check_in = datetime.strptime(check_in_date, '%Y-%m-%d').date()
                check_out = datetime.strptime(check_out_date, '%Y-%m-%d').date()

                # Calculate number of days and total price
                num_days = (check_out - check_in).days
                total_price = room.price_per_night * num_days
                
                # Create booking if user is authenticated
                if request.user.is_authenticated:
                    Booking.objects.create(
                        room=room,
                        user=request.user,
                        check_in_date=check_in,
                        check_out_date=check_out,
                        total_price=total_price
                    )
                    
                    # Update room availability
                    room.availability = False
                    room.save()
                    
                    messages.success(request, "Room booked successfully!")
                    return redirect('user_reservations')
                else:
                    messages.error(request, "You need to be logged in to book a room.")
                    return redirect('login')
                    
        elif 'rating' in request.POST and 'review_text' in request.POST:
            # Handle review submission
            if request.user.is_authenticated:
                rating = request.POST.get('rating')
                review_text = request.POST.get('review_text')
                
                # Validate
                if rating and review_text:
                    # Check if user has already reviewed this room
                    existing_review = Review.objects.filter(room=room, user=request.user).first()
                    
                    if existing_review:
                        # Update existing review
                        existing_review.rating = rating
                        existing_review.comment = review_text
                        existing_review.save()
                        messages.success(request, "Your review has been updated!")
                    else:
                        # Create new review
                        Review.objects.create(
                            room=room,
                            user=request.user,
                            rating=int(rating),
                            comment=review_text
                        )
                        messages.success(request, "Thank you for your review!")
                    
                    # Refresh reviews after adding/updating
                    reviews = room.reviews.all()
                else:
                    messages.error(request, "Please provide both a rating and review text.")
            else:
                messages.error(request, "You need to be logged in to submit a review.")
                return redirect('login')
    
    context = {
        'room': room,
        'bookings': bookings,
        'reviews': reviews,
        'user_has_reviewed': request.user.is_authenticated and Review.objects.filter(room=room, user=request.user).exists()
    }
    
    return render(request, 'hotel/book_room.html', context)


# about view
def about(request):
    room_images_dir = os.path.join(settings.MEDIA_ROOT, 'room_images')
    room_images = []

    if os.path.exists(room_images_dir):
        for file_name in os.listdir(room_images_dir):
            if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                room_images.append(f'/media/room_images/{file_name}')

    return render(request, 'hotel/about.html', {'room_images': room_images})


@login_required
def change_password_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    # Check if the logged-in user is trying to change their own password
    if request.user.pk != user.pk:
        messages.error(request, "You don't have permission to change this user's password.")
        return redirect('profile_detail', pk=pk)
    
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validate input
        if not current_password or not new_password or not confirm_password:
            messages.error(request, "All password fields are required.")
            return render(request, 'hotel/change_password.html')
            
        if not check_password(current_password, user.password):
            messages.error(request, "Your current password is incorrect.")
            return render(request, 'hotel/change_password.html')
            
        if new_password != confirm_password:
            messages.error(request, "New passwords don't match.")
            return render(request, 'hotel/change_password.html')
            
        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, 'hotel/change_password.html')
            
        # Change the password
        user.password = make_password(new_password)
        user.save()
        
        messages.success(request, "Your password has been changed successfully. Please log in with your new password.")
        logout(request)  # Log the user out so they can log in with the new password
        return redirect('login')
        
    return render(request, 'hotel/change_password.html', {'user': user})

@login_required
def user_reservations(request):
    # Get all bookings for the current logged-in user
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    total_spent = sum(booking.total_price for booking in bookings)
    
    # Prepare context for the template
    context = {
        'bookings': bookings,
        'active_tab': 'reservations',
        'total_spent': total_spent,
        'now': timezone.now(),  # Add current date for comparison in template
    }
    
    return render(request, 'hotel/user_reservations.html', context)

@login_required
def cancel_booking(request, booking_id):
    # Get the booking or return 404 if not found
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Security check - ensure user can only cancel their own bookings
    if booking.user != request.user:
        messages.error(request, "You don't have permission to cancel this booking.")
        return redirect('user_reservations')
    
    # Check if the booking is in the future (can only cancel future bookings)
    if booking.check_in_date <= timezone.now().date():
        messages.error(request, "Cannot cancel a booking that has already started or completed.")
        return redirect('user_reservations')
    
    # Store booking details for confirmation message
    hotel_name = booking.room.hotel.name
    room_number = booking.room.room_number
    check_in_date = booking.check_in_date.strftime('%b %d, %Y')
    
    # Update room availability
    room = booking.room
    room.availability = True
    room.save()
    
    # Delete the booking
    booking.delete()
    
    # Notify user of successful cancellation
    messages.success(
        request, 
        f"Your booking at {hotel_name} (Room {room_number}) for {check_in_date} has been cancelled successfully."
    )
    
    return redirect('user_reservations')

@login_required
def delete_account(request, pk):
    """View function to handle account deletion."""
    user = get_object_or_404(User, pk=pk)
    
    # Check if the logged-in user is trying to delete their own account
    if request.user.pk != user.pk:
        messages.error(request, "You don't have permission to delete this account.")
        return redirect('profile_detail', pk=pk)
    
    # Prevent deletion of admin accounts through this view as an extra security measure
    if user.is_admin or user.is_superuser:
        messages.error(request, "Admin accounts cannot be deleted through this interface.")
        return redirect('profile_detail', pk=pk)
    
    if request.method == 'POST':
        # Check for confirmation
        confirmation = request.POST.get('confirmation')
        if confirmation == 'DELETE':
            # Delete related data
            # The on_delete=CASCADE should handle related objects automatically
            
            # Logout the user before deleting
            logout(request)
            
            # Delete the user account
            user.delete()
            
            messages.success(request, "Your account has been permanently deleted.")
            return redirect('index')
        else:
            messages.error(request, "Incorrect confirmation. Account was not deleted.")
            return redirect('delete_account_confirm', pk=pk)
    
    # GET request redirects to confirmation page
    return redirect('delete_account_confirm', pk=pk)

@login_required
def delete_account_confirm(request, pk):
    """Display confirmation page for account deletion."""
    user = get_object_or_404(User, pk=pk)
    
    # Check if the logged-in user is trying to delete their own account
    if request.user.pk != user.pk:
        messages.error(request, "You don't have permission to delete this account.")
        return redirect('profile_detail', pk=pk)
    
    # Prevent deletion of admin accounts
    if user.is_admin or user.is_superuser:
        messages.error(request, "Admin accounts cannot be deleted.")
        return redirect('profile_detail', pk=pk)
    
    return render(request, 'hotel/delete_account_confirm.html', {'user': user})

def hotels_list(request):
    """View function to display all hotels."""
    hotels = Hotel.objects.all()
    return render(request, 'hotel/hotels_list.html', {'hotels': hotels})


def check_availability(request):
    room_id = request.GET.get('room_id')
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    try:
        room = Room.objects.get(id=room_id)
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()

        overlapping = Booking.objects.filter(
            room=room,
            check_in_date__lt=check_out_date,
            check_out_date__gt=check_in_date,
            payment_status='Paid'
        ).exists()
        print(overlapping)
        return JsonResponse({'available': not overlapping})
    except Exception as e:
        return JsonResponse({'available': False, 'error': str(e)})
class PaymobClient:
    def __init__(self):
        self.api_key = settings.PAYMOB_API_KEY
        self.public_key = settings.PAYMOB_PUBLIC_KEY
        self.secret_key = f"Token {settings.PAYMOB_SECRET_KEY}"
        # self.card_iframe_id = settings.PAYMOB_CARD_IFRAME_ID

    def checkout(self, total_price, integration_id, booking_id):
        payload = {
        "amount": int(total_price * 100),
        "currency": "EGP",
        "payment_methods": [int(integration_id)],
        "billing_data": {
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "01066415951",
            "email": "test@example.com",
        },
        "special_reference": f"{booking_id}_{int(time.time())}",
        # "merchant_order_id": booking_id,
        "redirection_url": "http://127.0.0.1:8000/paymob/callback",
        "extras": {
            "ee": 22
        }
        }

        response = requests.post(
            "https://accept.paymob.com/v1/intention/",
            headers={
                "Content-Type": "application/json",
                "Authorization": self.secret_key,
            },
            json=payload
        )
        data = response.json()
        print("DEBUG Paymob response:", data)  # Debugging line
        if 'client_secret' in data:
            return redirect(f"https://accept.paymob.com/unifiedcheckout/?publicKey={self.public_key}&clientSecret={data['client_secret']}")
        else:
            raise Exception("Payment initiation failed. Please try again later.")

def book_rooms(request, room_id):
    if request.method == 'POST':
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        room = Room.objects.get(id=room_id)
        user = request.user
        print("DEBUG check_in:", check_in)
        print("DEBUG check_out:", check_out)
        nights = (datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days
        total_price = nights * float(room.price_per_night)
        # Check if the room is already booked for the selected dates
        overlapping_bookings = Booking.objects.filter(
            room=room,
            check_in_date__lt=check_out,
            check_out_date__gt=check_in,
            payment_status='Paid'
        )
        if overlapping_bookings.exists():
            messages.error(request, "The room is not available for the selected dates.")
            return redirect('book_room', room_id=room.pk)
        if check_out < check_in:
            messages.error(request, "Check-out date must be after check-in date.")
            return render(request, 'hotel/book_room.html', {
            'room': room,
            'check_in': check_in,
            'check_out': check_out,
            'error_message': "Check-out date must be after check-in date."
            })
        
        booking = Booking.objects.create(
            room=room,
            user=user,
            check_in_date=check_in,
            check_out_date=check_out,
            total_price=total_price
        )
        # Log the booking or use it for further processing
        print(f"Booking created: {booking}")

        
        integration_ids = {
            "paymob_card_payment": settings.PAYMOB_CARD_INTEGRATION_ID,
            "paymob_wallet_payment": settings.PAYMOB_WALLET_INTEGRATION_ID,
          
        }

        payment_method = request.POST.get('payment_method')  # Retrieve payment method from the request
        print("DEBUG payment_method:", payment_method)
        if payment_method in integration_ids:
            return PaymobClient().checkout(booking.total_price, integration_ids[payment_method], booking.pk)

        else:
            messages.error(request, "Invalid payment method selected.")
            return redirect('hotel_detail', pk=room.hotel.id)
        
        
# import hmac
# import hashlib

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def paymob_callback(request):
    data = request.POST or request.GET

    # concat_str = (
    #     data['amount_cents'] + data['created_at'] + data['currency'] + data['error_occured'] +
    #     data['has_parent_transaction'] + data['id'] + data['integration_id'] +
    #     data['is_3d_secure'] + data['is_auth'] + data['is_capture'] + data['is_refunded'] +
    #     data['is_standalone_payment'] + data['is_voided'] + data['order'] + data['owner'] +
    #     data['pending'] + data['source_data_pan'] + data['source_data_sub_type'] +
    #     data['source_data_type'] + data['success']
    # )

    # hmac_secret = settings.PAYMOB_HMAC
    # generated_hmac = hmac.new(
    #     hmac_secret.encode('utf-8'),
    #     concat_str.encode('utf-8'),
    #     hashlib.sha512
    # ).hexdigest()

    # if generated_hmac == data['hmac']:
    booking_id = data.get('merchant_order_id').split('_')[0] 
    # booking_id2 = booking_id.split('_')[0] 
    print("DEBUG type of booking_id:", booking_id)
    booking = get_object_or_404(Booking, pk=int(booking_id))

    if data['success'] == 'true':
        # booking.amount_paid = int(data['amount_cents']) / 100
        booking.payment_status = "Paid"
        # booking.transaction_id = data['id']
        booking.save()
        status = "success"
        return render(request, 'hotel/payment_status.html', {'status': status})
    else:
        # booking.payment_status = "Failed"
        booking.delete()
        status = "failed"
        return render(request, 'hotel/payment_status', {'status': status})
    # else:
    #     return HttpResponse("Invalid HMAC", status=403)
    
def custom_404_view(request, exception):
    print("DEBUG 404 error:", exception)
    print("DEBUG 404 request path:", request)
    return redirect('/')