document.addEventListener('DOMContentLoaded', function () {
    const roomType = document.getElementById('room_type');
    const availability = document.getElementById('availability');
    const hotelId = document.getElementById('hotel-id')?.value;
  
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
  