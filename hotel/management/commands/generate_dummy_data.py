import os
import random
from datetime import datetime, timedelta
from django.conf import settings
from django.core.management.base import BaseCommand
from hotel.models import User, Hotel, Room, Booking
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'graduation_project.settings')
django.setup()

class Command(BaseCommand):
    help = 'Generate dummy data for models'

    def handle(self, *args, **kwargs):
        # Generate Users
        for i in range(10):
            User.objects.create_user(
                email=f'user{i}@example.com',
                username=f'user{i}',
                password='password123',
                phone_number=f'012345678{i}',
                date_of_birth=datetime.now() - timedelta(days=random.randint(7000, 20000)),
                gender=random.choice(['Male', 'Female']),
                is_verified=random.choice([True, False])
            )

        # Generate Hotels
        for i in range(5):
            hotel_image_path = os.path.join(settings.MEDIA_ROOT, 'hotel_images', random.choice([
                '01-grecotel-hotel-resorts-the-dolli-athens-1024x1536.webp',
                '1535639.jpg',
                '1718957715688-26316a3442d27400e8a6919f75237573.webp',
                '17289763798403_dji202406251708220027denhancednr.jpg',
                '665ca4ee2e65dd395f803b35_65ce62f8e2c055ca6dede665_Hotel20Panama8120Faranda20(2).png',
                '6718b6820112355ec0cc585c_BHC_facade.jpg',
                '67ffa86527bc4.jpg',
                '7286-10-4-23piscina-al-anochecer-2.webp',
                'beatriz-toledo-exterior-11.jpg',
                'CHOUCHOU HD nov21-© Nicolas Anetson-98.webp'
            ]))

            hotel = Hotel.objects.create(
                contact_number=f'0111234567{i}',
                name=f'Hotel {i}',
                location=f'Location {i}',
                description=f'This is a description for Hotel {i}.',
                rating=round(random.uniform(3.0, 5.0), 2),
                image=f'hotel_images/{os.path.basename(hotel_image_path)}'  # Add hotel image
            )

            # Generate Rooms for each Hotel
            for j in range(10):
                room_image_path = os.path.join(settings.MEDIA_ROOT, 'room_images', random.choice([
                    '01-grecotel-hotel-resorts-the-dolli-athens-1024x1536.webp',
                    '1535639.jpg',
                    '1718957715688-26316a3442d27400e8a6919f75237573.webp',
                    '17289763798403_dji202406251708220027denhancednr.jpg',
                    '665ca4ee2e65dd395f803b35_65ce62f8e2c055ca6dede665_Hotel20Panama8120Faranda20(2).png',
                    '6718b6820112355ec0cc585c_BHC_facade.jpg',
                    '67ffa86527bc4.jpg',
                    '7286-10-4-23piscina-al-anochecer-2.webp',
                    'beatriz-toledo-exterior-11.jpg',
                    'CHOUCHOU HD nov21-© Nicolas Anetson-98.webp'
                ]))

                Room.objects.create(
                    hotel=hotel,
                    room_number=f'{i}{j}',
                    room_type=random.choice(['Single', 'Double', 'Suite']),
                    price_per_night=round(random.uniform(50, 500), 2),
                    availability=random.choice([True, False]),
                    amenities='Wi-Fi, TV, AC',
                    room_image=f'room_images/{os.path.basename(room_image_path)}'  # Add room image
                )

        # Generate Bookings
        users = User.objects.all()
        rooms = Room.objects.all()
        for i in range(20):
            room = random.choice(rooms)
            user = random.choice(users)
            check_in_date = datetime.now().date() + timedelta(days=random.randint(1, 30))
            check_out_date = check_in_date + timedelta(days=random.randint(1, 5))
            total_price = room.price_per_night * (check_out_date - check_in_date).days

            Booking.objects.create(
                room=room,
                user=user,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                total_price=total_price
            )

        self.stdout.write(self.style.SUCCESS('Dummy data generated successfully!'))