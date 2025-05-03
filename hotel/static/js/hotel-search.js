const searchInput = document.getElementById('searchInput');
const resultsContainer = document.getElementById('default-hotels');
const searchTitle = document.getElementById('searchTitle');

searchInput.addEventListener('input', function () {
    const query = searchInput.value.trim();

    fetch(`/hotel/ajax/hotel-search/?location=${encodeURIComponent(query)}`)

        .then(response => response.json())
        .then(data => {
            resultsContainer.innerHTML = '';

            if (!query) {
                searchTitle.textContent = 'All Hotels';
            } else {
                searchTitle.textContent = `Search Results for "${query}"`;
            }

            if (data.hotels.length === 0) {
                resultsContainer.innerHTML = '<p>No results found.</p>';
                return;
            }

            data.hotels.forEach(hotel => {
                const hotelCard = `
            <div class="col-md-4">
              <div class="card h-100 shadow-sm border-0 rounded-4 overflow-hidden">
                <div class="position-relative">
                  <img src="${hotel.image_url}" class="card-img-top" alt="${hotel.name}" style="height: 250px; object-fit: cover;">
                </div>
                <div class="card-body d-flex flex-column">
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