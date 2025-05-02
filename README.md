# Star Hotels - Hotel Booking Platform

![Star Hotels Logo](media/hotel_images/hotel.webp)

## 🌟 Overview

Star Hotels is a comprehensive web-based hotel booking system built with Django that allows users to browse hotels, view room details, make reservations, and manage bookings. The platform offers a sleek, responsive UI with numerous features designed to make the hotel booking experience smooth and enjoyable.

## 📋 Features

### For Users
- **User Authentication System**
  - Registration with email verification
  - Secure login and password reset
  - Profile management with photo upload

- **Hotel Browsing**
  - View all available hotels
  - Real-time search by name and location
  - Filter by various criteria

- **Room Management**
  - Detailed room information with amenities
  - Room type filtering (Single, Double, Suite)
  - Availability calendar for each room

- **Booking System**
  - Easy booking process
  - Date range selection
  - Automatic price calculation

- **Review System**
  - Leave ratings and reviews for rooms
  - View other guests' reviews
  - Interactive star rating

- **User Dashboard**
  - View all reservations
  - Cancel upcoming bookings
  - See booking history and status

### For Administrators
- **Hotel Management**
  - Add/edit hotel details
  - Manage rooms and availability
  - View booking statistics

- **User Management**
  - View and manage users
  - Track booking history

## 🛠️ Technologies Used

- **Backend**: Django 4.x
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (default), can be configured for PostgreSQL
- **Additional Libraries**:
  - Flatpickr (for date selection)
  - Font Awesome (for icons)
  - AOS (Animate On Scroll) for UI animations

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Graduation-Project.git
   cd Graduation-Project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables** (copy from envexample.txt)
   ```bash
   cp envexample.txt .env
   ```
   Edit the `.env` file with your settings.

6. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create a superuser for admin access**
   ```bash
   python manage.py createsuperuser
   ```

8. **Generate sample data (optional)**
   ```bash
   python manage.py generate_dummy_data
   ```

9. **Run the development server**
   ```bash
   python manage.py runserver
   ```

10. **Access the website**
    - Main site: http://127.0.0.1:8000/
    - Admin panel: http://127.0.0.1:8000/admin/

## 🔍 Project Structure

```
Graduation-Project/
├── graduation_project/   # Main project settings
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL routing
│   └── wsgi.py           # WSGI configuration
│
├── hotel/                # Main app
│   ├── migrations/       # Database migrations
│   ├── static/           # Static files (CSS, JS, images)
│   │   ├── css/
│   │   ├── img/
│   │   └── js/
│   ├── templates/        # HTML templates
│   │   └── hotel/
│   ├── admin.py          # Admin site configuration
│   ├── models.py         # Database models
│   ├── urls.py           # App URL routing
│   └── views.py          # View functions
│
├── media/                # User-uploaded files
│   ├── hotel_images/
│   ├── profile_pictures/
│   └── room_images/
│
├── manage.py             # Django management script
├── requirements.txt      # Project dependencies
└── README.md            # This file
```

## 🔄 API Endpoints

- `/hotel/` - Home page with hotel listings
- `/hotel/login/` - User login
- `/hotel/register/` - User registration
- `/hotel/profile/<id>/` - User profile
- `/hotel/hotel/<id>/` - Hotel details
- `/hotel/book-room/<id>/` - Room booking
- `/hotel/user-reservations/` - User booking history
- `/hotel/about/` - About page
- `/hotel/ajax/hotel-search/` - AJAX endpoint for hotel search
- `/hotel/ajax/filter-rooms/<id>/` - AJAX endpoint for room filtering

## 📱 Responsive Design

The application is fully responsive and optimized for:
- Desktop computers
- Tablets
- Mobile devices

## 🤝 Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

Distributed under the ITI License. See `LICENSE` for more information.

## 📞 Contact

Project Team:
- Abdallah Mahany 
- Yasser Mohammed
- Mohamed Ali El Ghannam
- Fathy El Badrawy
- Omar Sadek El Azhary

Project Link: [https://github.com/YasserMuhamed2017/Graduation-Project](https://github.com/YasserMuhamed2017/Graduation-Project)

## 🙏 Acknowledgements

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)
- [Flatpickr](https://flatpickr.js.org/)
- [AOS Library](https://michalsnik.github.io/aos/)
