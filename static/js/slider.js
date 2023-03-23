const sliderItems = document.querySelectorAll('.slide');

const slideShow = () => {
    let currentSlide = 0;
    sliderItems[currentSlide].classList.add('current');
    const timerID = setInterval(() => {
        currentSlide = (currentSlide + 1) % sliderItems.length;
        if (currentSlide === 0) {
            sliderItems[sliderItems.length - 1].classList.remove('current');
        } else {
            sliderItems[currentSlide - 1].classList.remove('current');
        }
        sliderItems[currentSlide].classList.add('current');
    }, 3000)
}

if (sliderItems.length !== 0) {
    window.addEventListener("load", slideShow);
}
