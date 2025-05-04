const searchInput = document.getElementById('searchInput');
const resultsContainer = document.getElementById('default-hotels');
const searchTitle = document.getElementById('searchTitle');
const selectedHotels = document.getElementById('selected-hotels');

searchInput.addEventListener('input', function () {
    const query = searchInput.value.trim();

    fetch(`/ajax/hotel-search/?location=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            resultsContainer.innerHTML = '';

            if (!query) {
                searchTitle.innerHTML = '';
                resultsContainer.innerHTML = '';
                return;
            }

            if (data.hotels.length === 0) {
                resultsContainer.innerHTML = '<p>No results found.</p>';
                return;
            }

            searchTitle.innerHTML = 'Search Result for "' + query + '"';
            data.hotels.forEach(hotel => {
                const hotelCard = `
            <div class="col-md-4">
              <div class="card h-100 shadow-sm border-0 rounded-4 overflow-hidden">
                <div class="position-relative">
                  <img src="${hotel.image_url}" class="card-img-top" alt="${hotel.name}" style="height: 250px; object-fit: cover;">
                </div>
                <div class="position-absolute top-0 end-0 m-3">
                  <span class="badge rounded-pill text-bg-primary fw-bold">
                    <i class="fas fa-star me-1"></i>${ hotel.rating }
                  </span>
                </div>
                <div class="card-body d-flex flex-column" style="height: 40vh;">
                  <h5 class="card-title">${hotel.name}</h5>
                  <h6 class="card-subtitle text-muted mb-2">${hotel.location}</h6>
                  <p class="card-text">${hotel.description}</p>
                  <p class="card-text">Contact: ${hotel.contact_number}</p>
                  <div class="mt-auto">
                    <a href="/hotel/hotel/${hotel.id}/" class="btn btn-primary w-100 rounded-pill">View Details</a>
                  </div>
                </div>
              </div>
            </div>
          `;
                resultsContainer.innerHTML += hotelCard;
            });

        });
});
// animate on scroll
AOS.init({
  duration: 2000,
  once: false
});


var swiper = new Swiper(".slide-swp", {
  pagination: {
      el: ".swiper-pagination",
      dynamicBullests:true,
      clickable:true
  },
  autoplay:{
      delay:4000,
  },
  loop:true,
});


// Initialize Swiper for Selected Hotels
var swiper = new Swiper(".slide-product", {
  slidesPerView: 3,
  spaceBetween: 20,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev"
  },
  autoplay: {
    delay: 4000,
  },
  loop: true,
  breakpoints: {
    1200: {
      slidesPerView: 3,
      spaceBetween: 20
    },
    1000: {
      slidesPerView: 3,
      spaceBetween: 20
    },
    700: {
      slidesPerView: 2,
      spaceBetween: 15
    },
    0: {
      slidesPerView: 1,
      spaceBetween: 10
    }
  }
});