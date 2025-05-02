// start of dynamic backgroundImage
const bg1 = document.getElementById("bg1");
const bg2 = document.getElementById("bg2");

const images = [
    "/static/img/3.jpg",
    "/static/img/4.jpg",
    "/static/img/5.jpg",
    "/static/img/8.jpg",
    "/static/img/9.jpg",
    "/static/img/11.jpg",
];

let current = 0;
let showingBg1 = true;

function preloadImage(src) {
    const img = new Image();
    img.src = src;
}

function changeBackground() {
    const next = (current + 1) % images.length;
    preloadImage(images[next]);

    if (showingBg1) {
        bg2.style.backgroundImage = `url('${images[next]}')`;
        bg2.style.opacity = 1;
        bg1.style.opacity = 0;
    } else {
        bg1.style.backgroundImage = `url('${images[next]}')`;
        bg1.style.opacity = 1;
        bg2.style.opacity = 0;
    }

    current = next;
    showingBg1 = !showingBg1;
}

// Initialize first image
bg1.style.backgroundImage = `url('${images[0]}')`;

setInterval(changeBackground, 5000);

// end of dynamic backgroundImage

// animate on scroll
AOS.init({
    duration: 2000,
    once: false
  });