window.addEventListener('load', () => {
    const slider = document.querySelector('.slider');
    const slides = document.querySelectorAll('.slide');
    const prevButton = document.querySelector('.prev');
    const nextButton = document.querySelector('.next');
    const textContents = document.querySelectorAll('.text-content');

    let counter = 0;

    const slideWidth = document.querySelector('.slider-container').clientWidth;

    function updateTextContent() {
        textContents.forEach((content, index) => {
            content.classList.toggle('active', index === counter);
        });
    }

    nextButton.addEventListener('click', () => {
        counter = (counter + 1) % slides.length; // Увеличиваем counter
        slide();
        updateTextContent();
    });

    prevButton.addEventListener('click', () => {
        counter = (counter - 1 + slides.length) % slides.length; // Уменьшаем counter
        slide();
        updateTextContent();
    });

    function slide() {
        const translateX = -slideWidth * counter; // Вычисляем смещение
        slider.style.transform = `translateX(${translateX}px)`; // Применяем смещение
    }

    updateTextContent(); // Инициализируем текст
});