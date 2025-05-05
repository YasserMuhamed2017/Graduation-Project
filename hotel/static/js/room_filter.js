document.addEventListener('DOMContentLoaded', function () {
    const roomType = document.getElementById('room_type');
    const availability = document.getElementById('availability');
    const hotelId = document.getElementById('hotel-id')?.value;
    const roomHeader = document.getElementById('rooms'); // h4
    const resultRoomHeader = document.getElementById('result-rooms'); // h4
    const stars = document.querySelectorAll('.star-rating');
    const ratingInput = document.getElementById('rating');
    
    stars.forEach(star => {
        star.addEventListener('mouseover', function() {
            const rating = this.getAttribute('data-rating');
            highlightStars(rating);
        });
        
        star.addEventListener('mouseout', function() {
            const currentRating = ratingInput.value || 0;
            highlightStars(currentRating);
        });
        
        star.addEventListener('click', function() {
            const rating = this.getAttribute('data-rating');
            ratingInput.value = rating;
            highlightStars(rating);
        });
    });
    
    function highlightStars(rating) {
        stars.forEach(star => {
            const starRating = star.getAttribute('data-rating');
            
            if (starRating <= rating) {
                star.classList.remove('far');
                star.classList.add('fas');
                star.style.color = '#ffc107';
            } else {
                star.classList.remove('fas');
                star.classList.add('far');
                star.style.color = '';
            }
        });
    }
        
    if (roomType && availability && hotelId) {
      function fetchFilteredRooms() {
        const type = roomType.value;
        const avail = availability.value;
      
        fetch(`/ajax/filter-rooms/${hotelId}/?room_type=${type}&availability=${avail}`)
          .then(response => response.json())
          .then(data => {
            document.getElementById('filtered-rooms').innerHTML = data.html;
          
            
          });
      }

      roomType.addEventListener('change', fetchFilteredRooms);
      availability.addEventListener('change', fetchFilteredRooms);
    }
  });
  
// animate on scroll
AOS.init({
  duration: 2000,
  once: false
});


//   document.addEventListener('DOMContentLoaded', function () {
//     const roomTypeContainer = document.getElementById('room_type');
//     const availabilityContainer = document.getElementById('availability');
//     const hotelId = document.getElementById('hotel-id')?.value;
  
//     if (roomTypeContainer && availabilityContainer && hotelId) {
//       function getSelectedValue(container, name) {
//         const selected = container.querySelector(`input[name="${name}"]:checked`);
//         return selected ? selected.value : '';
//       }
  
//       function fetchFilteredRooms() {
//         const type = getSelectedValue(roomTypeContainer, 'room_type');
//         const avail = getSelectedValue(availabilityContainer, 'availability');
  
//         fetch(`/hotel/ajax/filter-rooms/${hotelId}/?room_type=${type}&availability=${avail}`)
//           .then(response => response.json())
//           .then(data => {
//             document.getElementById('filtered-rooms').innerHTML = data.html;
//           });
//       }
  
//       roomTypeContainer.addEventListener('change', fetchFilteredRooms);
//       availabilityContainer.addEventListener('change', fetchFilteredRooms);
//     }
//   });
  